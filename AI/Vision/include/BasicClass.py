# coding: utf-8

# ---- Imports ----

# Libraries to be used
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the vision system
from abc import ABCMeta, abstractmethod # Used to create abstract classes
import cv2 # Library to process image
print 'BasicClass - Opencv Version:', cv2.__version__
if int((cv2.__version__).split('.')[0]) < 3:
	print "Old version of OpenCV, upgrade to version 3"
	sys.exit()

# Used class developed by RoboFEI-HT
from VisionException import * # Used to handle exceptions
from ConfigIni import * # Used to read config vision

## Basic Class
# Class that implements similar functions between classes
class BasicClass( ):
	__metaclass__ = ABCMeta
	
	# ---- Variables ----
	
	## confini
	_confini = None
	
	## args
	# Execution parameters.
	_args = None
	
	## Constructor class
	@abstractmethod
	def __init__(self, name, func, arg):
		print 'Instantiating Basic Class'
		self._args = arg
		self._confini = ConfigIni(name, func)
		
	## finalize
	def finalize(self, dictionary):
		self._confini.finalize(dictionary)