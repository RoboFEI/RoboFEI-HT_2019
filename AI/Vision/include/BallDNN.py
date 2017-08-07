# coding: utf-8

# ---- Imports ----

# Libraries to be used
import sys
import numpy as np
import time
import os
import tempfile
import tarfile
from google.protobuf import text_format
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the vision system
import caffe
from caffe.proto import caffe_pb2  # noqa

# Used class developed by RoboFEI-HT
sys.path.append('../../Blackboard/src') # debug-iPython
from BasicThread import * # 
from ColorSegmentation import * # 
from Morphology import * #

class BallDNN(BasicThread):
	
	# ---- Variables ----
	
	## observation
	# .
	__observation = None
	
	## net
	__net = None
	
	## transformer
	__transformer = None
	
	## mean_file
	__mean_file = None
	
	## labels
	__labels = None
	
	def __read_labels(self, labels_file):
		"""
		Returns a list of strings
		Arguments:
		labels_file -- path to a .txt file
		"""
		if not labels_file:
			print 'WARNING: No labels file provided. Results will be difficult to interpret.'
			return None
	
		labels = []
		with open(labels_file) as infile:
			for line in infile:
				label = line.strip()
				if label:
					labels.append(label)
		assert len(labels), 'No labels found'
		return labels
	
	## get_transformer
	def __get_transformer(self, deploy_file, mean_file=None):
		"""
		Returns an instance of caffe.io.Transformer
		Arguments:
		deploy_file -- path to a .prototxt file
		Keyword arguments:
		mean_file -- path to a .binaryproto file (optional)
		"""
		network = caffe_pb2.NetParameter()
		with open(deploy_file) as infile:
			text_format.Merge(infile.read(), network)
	
		if network.input_shape:
			dims = network.input_shape[0].dim
		else:
			dims = network.input_dim[:4]
	
		t = caffe.io.Transformer(inputs={'data': dims})
		t.set_transpose('data', (2, 0, 1))  # transpose to (channels, height, width)
	
		# color images
		if dims[1] == 3:
			# channel swap
			t.set_channel_swap('data', (2, 1, 0))
	
		if mean_file:
			# set mean pixel
			with open(mean_file, 'rb') as infile:
				blob = caffe_pb2.BlobProto()
				blob.MergeFromString(infile.read())
				if blob.HasField('shape'):
					blob_dims = blob.shape
					assert len(blob_dims) == 4, 'Shape should have 4 dimensions - shape is "%s"' % blob.shape
				elif blob.HasField('num') and blob.HasField('channels') and					 blob.HasField('height') and blob.HasField('width'):
					blob_dims = (blob.num, blob.channels, blob.height, blob.width)
				else:
					raise ValueError('blob does not provide shape or 4d dimensions')
				pixel = np.reshape(blob.data, blob_dims[1:]).mean(1).mean(1)
				t.set_mean('data', pixel)
	
		return t
	
	## get_net
	def __get_net(self, caffemodel, deploy_file, use_gpu=True):
		"""
		Returns an instance of caffe.Net
		Arguments:
		caffemodel -- path to a .caffemodel file
		deploy_file -- path to a .prototxt file
		Keyword arguments:
		use_gpu -- if True, use the GPU for inference
		"""
		if use_gpu:
			caffe.set_mode_gpu()
	
		# load a new model
		return caffe.Net(deploy_file, caffemodel, caffe.TEST)
	
	## unzip_archive
	def __unzip_archive(self, archive):
		"""
		Unzips an archive into a temporary directory
		Returns a link to that directory
		Arguments:
		archive -- the path to an archive file
		"""
		assert os.path.exists(archive), 'File not found - %s' % archive
	
		tmpdir = os.path.join(tempfile.gettempdir(), os.path.basename(archive))
		assert tmpdir != archive  # That wouldn't work out
	
		if os.path.exists(tmpdir):
			# files are already extracted
			pass
		else:
			if tarfile.is_tarfile(archive):
				print 'Extracting tarfile ...'
				with tarfile.open(archive) as tf:
					tf.extractall(path=tmpdir)
			elif zipfile.is_zipfile(archive):
				print 'Extracting zipfile ...'
				with zipfile.ZipFile(archive) as zf:
					zf.extractall(path=tmpdir)
			else:
				raise ValueError('Unknown file type for %s' % os.path.basename(archive))
		return tmpdir
	
	def __init__(self, arg):
		print 'Initiating class Ball DNN'
		super(BallDNN, self).__init__(arg, 'Ball', 'DNN')
		
		self.__observation = self._confini.read()
		if self.__observation is -1:
			self.__observation = {
				'x_esquerdo': 280,
				'x_centro_esquerdo': 320,
				'x_centro': 465,
				'x_centro_direito': 645,
				'x_direito': 703,
		
				'y_chute': 549,
				'y_longe': 220,
				
				'white': 200,
				
				'max_count': 10,
				
				'file DNN': 'ball.tar.gz'
			}
		
		tmpdir = self.__unzip_archive('./Data/' + self.__observation['file DNN'])
		caffemodel = None
		deploy_file = None
		labels_file = None
		for filename in os.listdir(tmpdir):
			full_path = os.path.join(tmpdir, filename)
			if filename.endswith('.caffemodel'):
				caffemodel = full_path
			elif filename == 'deploy.prototxt':
				deploy_file = full_path
			elif filename.endswith('.binaryproto'):
				self.__mean_file = full_path
			elif filename == 'labels.txt':
				labels_file = full_path
			else:
				print 'Unknown file:', filename
		
		assert caffemodel is not None, 'Caffe model file not found'
		assert deploy_file is not None, 'Deploy file not found'
		
		self.__net = self.__get_net(caffemodel, deploy_file, use_gpu=False)
		# __transformer = __get_transformer(deploy_file, __mean_file)
		# __, channels, height, width = __transformer.inputs['data']
		# __labels = __read_labels(labels_file)
		
		####	#create index from label to use in decicion action
		# number_label =  dict(zip(__labels, range(len(__labels))))