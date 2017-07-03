# coding: utf-8

# ---- Imports ----

# Libraries to be used
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the vision system
from abc import ABCMeta, abstractmethod # Used to create abstract classes
from threading import Thread # Used to create classes with thread functions

# Used class developed by RoboFEI-HT
from BasicClass import * # 
from Blackboard import * # 
from VisionException import * # Used to handle exceptions
import cv2 # Library to process image
print 'BasicThread - Opencv Version:', cv2.__version__
if int((cv2.__version__).split('.')[0]) < 3:
	print "Old version of OpenCV, upgrade to version 3"
	sys.exit()

## Basic Class - Thread
# Class that implements similar functions between classes used thread.
class BasicThread(Thread, BasicClass):
	__metaclass__ = ABCMeta
	
	# ---- Variables ----
	
	## bkb
	# Protected variable responsible for communication with shared memory (blackboard).
	_bkb = None
	
	## Constructor Class
	@abstractmethod
	def __init__(self):
		print 'Instantiating Basic Class'
		self._bkb = Blackboard( )