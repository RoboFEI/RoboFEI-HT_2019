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

## Basic Class - Thread
# Class that implements similar functions between classes used thread.
class BasicThread(BasicClass, Thread):
	__metaclass__ = ABCMeta
	
	# ---- Variables ----
	
	## bkb
	# Protected variable responsible for communication with shared memory (blackboard).
	_bkb = None
	
	## Constructor Class
	@abstractmethod
	def __init__(self, name, func, arg):
		Thread.__init__(self)
		super(BasicThread, self).__init__(name, func, arg)
		self._bkb = Blackboard( )