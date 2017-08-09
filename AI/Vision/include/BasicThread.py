# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the vision system.
from abc import ABCMeta, abstractmethod # Used to create abstract classes
from threading import Thread, Condition, Lock # Used to create classes with thread functions

# Used class developed by RoboFEI-HT.
from BasicClass import * # Class that implements similar functions between classes.
from Blackboard import * # Class responsible for accessing shared memory.
from VisionException import * # Used to handle exceptions

## Basic Class - Thread
# Class that implements similar functions between classes used thread.
class BasicThread(BasicClass, Thread):
	__metaclass__ = ABCMeta
	
	# ---- Variables ----
	
	## bkb
	# Protected variable responsible for communication with shared memory (blackboard).
	_bkb = None
	
	## running
	_running = False
	
	## pausethread
	_pausethread = None
	
	## Constructor Class
	@abstractmethod
	def __init__(self, arg, name = None, func = None):
		
		Thread.__init__(self)
		
		if name != None and func != None:
			super(BasicThread, self).__init__(arg, name, func)
		else:
			super(BasicThread, self).__init__(arg)
		
		self._bkb = Blackboard( )
		
		self._pausethread = Condition(Lock())
		
	## pause
	def _pause(self):
		self._pausethread.acquire()
	
	## resume
	def _resume(self):
		self._pausethread.notify()
		self._pausethread.release()