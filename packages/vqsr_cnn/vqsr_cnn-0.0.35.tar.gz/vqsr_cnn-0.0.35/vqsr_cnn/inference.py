# Imports
import os
import sys
import h5py
import time
import json
import argparse
import numpy as np
from collections import Counter, defaultdict, namedtuple

# Keras Imports
import keras.backend as K
from keras.models import load_model


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~ Definitions ~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

dna_symbols = {'A':0, 'C':1, 'G':2, 'T':3}
inputs_indel = {'A':0, 'C':1, 'G':2, 'T':3, '*':4}

# Base calling ambiguities, See https://www.bioinformatics.org/sms/iupac.html
ambiguity_codes = {'K':[0,0,0.5,0.5], 'M':[0.5,0.5,0,0], 'R':[0.5,0,0,0.5], 'Y':[0,0.5,0.5,0], 'S':[0,0.5,0,0.5], 'W':[0.5,0,0.5,0], 
				  'B':[0,0.333,0.333,0.334], 'V':[0.333,0.333,0,0.334],'H':[0.333,0.333,0.334,0],'D':[0.333,0,0.333,0.334],
				  'X':[0.25,0.25,0.25,0.25], 'N':[0.25,0.25,0.25,0.25]}


# Annotation sets
annotations = {
	'_' : [], # Allow command line to unset annotations
	'gatk_w_qual' : ['MQ', 'DP', 'SOR', 'FS', 'QD', 'MQRankSum', 'QUAL', 'ReadPosRankSum'],
	'gatk' : ['MQ', 'DP', 'SOR', 'FS', 'QD', 'MQRankSum', 'ReadPosRankSum'],
	'annotations' : ['MQ', 'DP', 'SOR', 'FS', 'QD', 'MQRankSum', 'ReadPosRankSum'],
	'm2':['AF', 'AD_0', 'AD_1', 'MBQ', 'MFRL_0', 'MFRL_1', 'MMQ', 'MPOS'],
	'combine': ['MQ', 'DP', 'SOR', 'FS', 'QD', 'MQRankSum', 'ReadPosRankSum', 'AF', 'AD_0', 'AD_1', 'MBQ', 'MFRL_0', 'MFRL_1', 'MMQ', 'MPOS'],
	'gnomad': ['MQ', 'DP', 'SOR', 'FS', 'QD', 'MQRankSum', 'ReadPosRankSum', 'DP_MEDIAN', 'DREF_MEDIAN', 'GQ_MEDIAN', 'AB_MEDIAN'],
}

snp_indel_labels = {'NOT_SNP':0, 'NOT_INDEL':1, 'SNP':2, 'INDEL':3}


eps = 1e-7
separator_char = '\t'
Read = namedtuple("Read", "seq qual cigar first reverse mq")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~ Inference ~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def score_and_write_batch(model, file_out, fifo, batch_size, python_batch_size, use_reads):
	'''Score and write a batch of variants with a 1D CNN.

	This function is tightly coupled with the NeuralNetInference
	It requires data written to the fifo in the order given by transferToPythonViaFifo

	Arguments
		model: a keras model
		file_out: The VCF file where variants scores are written
		fifo: The fifo opened by GATK Streaming executor
		batch_size: The total number of variants available in the fifo
		python_batch_size: the number of variants to process in each inference
		use_reads : Use read data from a BAM for 2D CNNs or just reference for 1D CNNs
	'''
	annotation_batch = []
	reference_batch = []
	variant_types = []
	variant_data = []
	read_batch = []

	for i in range(batch_size):
		fifo_line = fifo.readline()
		fifo_data = fifo_line.split(separator_char)

		variant_data.append(fifo_data[0] + '\t' + fifo_data[1] + '\t' + fifo_data[2] + '\t' + fifo_data[3])
		reference_batch.append(reference_string_to_tensor(fifo_data[4]))
		annotation_batch.append(annotation_string_to_tensor(fifo_data[5]))
		variant_types.append(fifo_data[6])
		if use_reads:
			fidx = 7
			while fidx < len(fifo_data):
				read_batch.append(Read(fifo_data[fidx], fifo_data[fidx+1], fifo_data[fidx+2], fifo_data[fidx+3], fifo_data[fidx+4], fifo_data[fidx+5]))
				fidx += 6
			print('Got reads!,' f_idx)



	predictions = model.predict([np.array(reference_batch), np.array(annotation_batch)], batch_size=python_batch_size)
	indel_scores = predictions_to_indel_scores(predictions)
	snp_scores = predictions_to_snp_scores(predictions)

	for i in range(batch_size):
		if 'SNP' == variant_types[i]:
			file_out.write(variant_data[i]+'\t{0:.3f}'.format(snp_scores[i])+'\n')
		elif 'INDEL' == variant_types[i]:
			file_out.write(variant_data[i]+'\t{0:.3f}'.format(indel_scores[i])+'\n')
		else:
			file_out.write(variant_data[i]+'\t{0:.3f}'.format(snp_scores[i])+'\n')


def reference_string_to_tensor(reference):
	dna_data = np.zeros( (len(reference), len(dna_symbols)) )
	for i,b in enumerate(reference):
		if b in dna_symbols:
			dna_data[i, dna_symbols[b]] = 1.0
		elif b in ambiguity_codes:
			dna_data[i] = ambiguity_codes[b]
		else:
			print('Error! Unknown code:', b)
			continue
	return dna_data


def annotation_string_to_tensor(annotation_string):
	name_val_pairs = annotation_string.split(';')
	name_val_arrays = [p.split('=') for p in name_val_pairs]
	annotation_map = {str(p[0]).strip() : p[1] for p in name_val_arrays if len(p) > 1}
	annotation_data = np.zeros(( len(annotations['gatk']), ))
	
	for i,a in enumerate(annotations['gatk']):
		if a in annotation_map:
			annotation_data[i] = annotation_map[a]
	
	return annotation_data


def predictions_to_snp_scores(predictions):
	snp = predictions[:, snp_indel_labels['SNP']]
	not_snp = predictions[:, snp_indel_labels['NOT_SNP']]
	return np.log(eps + snp / (not_snp + eps))


def predictions_to_indel_scores(predictions):
	indel = predictions[:, snp_indel_labels['INDEL']]
	not_indel = predictions[:, snp_indel_labels['NOT_INDEL']]
	return np.log(eps + indel / (not_indel + eps))


def predictions_to_snp_indel_scores(predictions):
	snp_dict = predictions_to_snp_scores(predictions)
	indel_dict = predictions_to_indel_scores(predictions)
	return snp_dict, indel_dict


def model_from_semantics(semantics_json):
	args = parse_args()
	return set_args_and_get_model_from_semantics(args, semantics_json)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~ Arguments ~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parse_args():
	parser = argparse.ArgumentParser()

	# Tensor defining dictionaries
	parser.add_argument('--tensor_map', default='read_tensor',
						help='Key which looks up the map from tensor channels to their meaning.')
	parser.add_argument('--input_symbols', default=dna_symbols,
						help='Dict mapping input symbols to their index within input tensors.')
	parser.add_argument('--labels', default=snp_indel_labels,
						help='Dict mapping label names to their index within label tensors.')

	# Tensor defining arguments
	parser.add_argument('--batch_size', default=32, type=int,
						help='Mini batch size for stochastic gradient descent algorithms.')
	parser.add_argument('--read_limit', default=128, type=int,
						help='Maximum number of reads to load.')
	parser.add_argument('--window_size', default=128, type=int,
						help='Size of sequence window to use as input, typically centered at a variant.')
	parser.add_argument('--channels_last', default=False, dest='channels_last', action='store_true',
						help='Store the channels in the last axis of tensors, tensorflow->true, theano->false')
	parser.add_argument('--base_quality_mode', default='phot', choices=['phot', 'phred', '1hot'],
						help='How to treat base qualities, must be in [phot, phred, 1hot]')

	# Annotation arguments
	parser.add_argument('--annotations', help='Array of annotation names, initialised via annotation_set argument')
	parser.add_argument('--annotation_set', default='gatk', choices=annotations.keys(),
						help='Key which maps to an annotations list (or None for architectures that do not take annotations).')

	# Genomic area of interest
	parser.add_argument('--start_pos', default=0, type=int,
						help='Genomic position to start from, helpful for parallelization.')
	parser.add_argument('--end_pos', default=0, type=int,
						help='Genomic position to end at, helpful for parallelization.')
	parser.add_argument('--chrom', help='Specific chromosome to load, helpful for parallelization.')

	# Input files and directories: vcfs, bams, beds, hd5, fasta
	parser.add_argument('--architecture', default='',
						help='A json file specifying semantics and architecture of a neural net.')
	parser.add_argument('--bam_file',
						help='Path to a BAM file to train from or generate tensors with.')
	parser.add_argument('--train_vcf',
						help='Path to a VCF that has verified true calls from NIST, platinum genomes, etc.')
	parser.add_argument('--negative_vcf',
						help='Haplotype Caller or VQSR generated VCF with raw annotation values [and quality scores].')
	parser.add_argument('--output_vcf', default=None,
						help='Optional VCF to write to.')
	parser.add_argument('--bed_file',
						help='Bed file specifying high confidence intervals associated with args.train_vcf.')
	parser.add_argument('--dataset',
						help='Directory of tensors, must be split into test/valid/train sets with directories for each label within.')
	parser.add_argument('--reference_fasta',
						help='The reference FASTA file (e.g. HG19 or HG38).')

	# Run specific arguments
	parser.add_argument('--id', default='no_id',
						help='Identifier for this run, user-defined string to keep experiments organized.')
	parser.add_argument('--random_seed', default=12878, type=int,
						help='Random seed to use throughout run.  Always use np.random.')

	# Parse, print, set annotations and seed
	args = parser.parse_args()
	args.annotations = annotations_from_args(args)
	np.random.seed(args.random_seed)
	print('Arguments are', args)

	return args


def annotations_from_args(args):
	if args.annotation_set and args.annotation_set in annotations:
		return annotations[args.annotation_set]
	return None


def set_args_and_get_model_from_semantics(args, semantics_json):
	'''Recreate a model from a json file specifying model semantics.

	Update the args namespace from the semantics file values.
	Assert that the serialized tensor map and the recreated one are the same.

	Arguments:
		args.tensor_map: String which indicates tensor map to use or None
		args.window_size: sites included in the tensor map
		args.read_limit: Maximum reads included in the tensor map
		args.annotations: List of annotations or None
		semantics_json: Semantics json file (created with serialize_model_semantics())

	Returns:
		The Keras model
	'''
	with open(semantics_json, 'r') as infile:
		semantics = json.load(infile)

	if 'input_tensor_map' in semantics:
		args.tensor_map = semantics['input_tensor_map_name']
		args.window_size = semantics['window_size']
		args.read_limit = semantics['read_limit']
		tm = get_tensor_channel_map_from_args(args)
		assert(len(tm) == len(semantics['input_tensor_map']))
		for key in tm:
			assert(tm[key] == semantics['input_tensor_map'][key])

	if 'input_annotations' in semantics:
		args.annotations = semantics['input_annotations']

	args.labels = semantics['output_labels']

	if 'data_dir' in semantics:
		args.data_dir = semantics['data_dir']

	weight_path_hd5 = os.path.join(os.path.dirname(semantics_json),semantics['architecture'])
	model = load_model(weight_path_hd5, custom_objects=get_metric_dict(args.labels))
	model.summary()
	return model


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~ Tensor Maps ~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_tensor_channel_map_from_args(args):
	'''Return tensor mapping dict given args.tensor_map'''
	if not args.tensor_map:
		return None

	if 'read_tensor' == args.tensor_map:
		return get_tensor_channel_map_rt()
	elif '2d_mapping_quality' == args.tensor_map:
		return get_tensor_channel_map_mq()
	elif 'reference' == args.tensor_map:
		return get_tensor_channel_map_1d_dna()
	else:
		raise ValueError('Unknown tensor mapping mode:', args.tensor_map)


def get_tensor_channel_map_1d_dna():
	'''1D Reference tensor with 4 channel DNA encoding.'''
	tensor_map = {}
	for k in dna_symbols.keys():
		tensor_map[k] = dna_symbols[k]

	return tensor_map


def get_tensor_channel_map_reference_reads():
	'''Read and reference tensor with 4 channel DNA encoding.
	Plus insertions and deletions.
	'''
	tensor_map = {}
	for k in inputs_indel.keys():
		tensor_map['read_'+k] = inputs_indel[k]
	for k in inputs_indel.keys():
		tensor_map['reference_'+k] = len(inputs_indel) + inputs_indel[k]

	return tensor_map


def get_tensor_channel_map():
	'''Read and reference tensor with 4 channel DNA encoding.
	Also includes read flags.
	'''
	tensor_map = {}
	for k in inputs_indel.keys():
		tensor_map['read_'+k] = inputs_indel[k]
	for k in inputs_indel.keys():
		tensor_map['reference_'+k] = len(inputs_indel) + inputs_indel[k]
	tensor_map['flag_bit_4'] = 10
	tensor_map['flag_bit_5'] = 11
	tensor_map['flag_bit_6'] = 12
	tensor_map['flag_bit_7'] = 13
	return tensor_map


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~ Metrics ~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def precision(y_true, y_pred):
	'''Calculates the precision, a metric for multi-label classification of
	how many selected items are relevant.
	'''
	true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
	predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
	precision = true_positives / (predicted_positives + K.epsilon())
	return precision


def recall(y_true, y_pred):
	'''Calculates the recall, a metric for multi-label classification of
	how many relevant items are selected.
	'''
	true_positives = K.sum(K.round(K.clip(y_true*y_pred, 0, 1)))
	possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
	recall = true_positives / (possible_positives + K.epsilon())
	return recall


def per_class_recall(labels):
	recall_fxns = []

	for label_key in labels:
		label_idx = labels[label_key]
		string_fxn = 'def '+ label_key + '_recall(y_true, y_pred):\n'
		string_fxn += '\ttrue_positives = K.sum(K.round(K.clip(y_true*y_pred, 0, 1)), axis=0)\n'
		string_fxn += '\tpossible_positives = K.sum(K.round(K.clip(y_true, 0, 1)), axis=0)\n'
		string_fxn += '\treturn true_positives['+str(label_idx)+'] / (possible_positives['+str(label_idx)+'] + K.epsilon())\n'

		exec(string_fxn)
		recall_fxn = eval(label_key + '_recall')
		recall_fxns.append(recall_fxn)

	return recall_fxns


def per_class_precision(labels):
	precision_fxns = []

	for label_key in labels:
		label_idx = labels[label_key]
		string_fxn = 'def '+ label_key + '_precision(y_true, y_pred):\n'
		string_fxn += '\ttrue_positives = K.sum(K.round(K.clip(y_true*y_pred, 0, 1)), axis=0)\n'
		string_fxn += '\tpredicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)), axis=0)\n'
		string_fxn += '\treturn true_positives['+str(label_idx)+'] / (predicted_positives['+str(label_idx)+'] + K.epsilon())\n'

		exec(string_fxn)
		precision_fxn = eval(label_key + '_precision')
		precision_fxns.append(precision_fxn)

	return precision_fxns


def get_metric_dict(labels=snp_indel_labels):
	metrics = {'precision':precision, 'recall':recall}
	precision_fxns = per_class_precision(labels)
	recall_fxns = per_class_recall(labels)
	for i,label_key in enumerate(labels.keys()):
		metrics[label_key+'_precision'] = precision_fxns[i]
		metrics[label_key+'_recall'] = recall_fxns[i]

	return metrics