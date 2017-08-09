# coding: utf-8

# Libraries to be used
import sys
sys.path.append('../include')
sys.path.append('../src')

import os # Library for interaction with the system.
from copy import copy # To create copies of the variables
import time # Using for time control and measurement

# Used class developed by RoboFEI-HT.
from BasicThread import * # Base class with primary functions.
from Servo import * # Class for servo control.

## Class HeadControl
# Class responsible for controlling the servos of the head using information from visual memory.
class HeadControl(BasicThread):
	
	# ---- Variables ----
	
	## motor
	# Servomotor addresses.
	__motor = {
		'Maximum Torque': 34,
		'Goal Position': 30, 
		'Present Position': 36,
	}
	
	## head
	# .
	__head = None
	
	## observation
	# .
	__observation = None
	
	## Constructor Class
	def __init__(self, arg):
		print '\33[1;33m' + '---- Initializing class HeadControl ----' + '\33[0m'
		super(HeadControl, self).__init__(arg, 'Head' , 'parameters')
		
		self.__observation = {
			'ID Pan': 19,
			'ID Tilt': 20,
			'frequency': 1000,
			'center_pan': 512,
			'center_tilt': 310,
		}
		self.__observation = self._confini.read(self.__observation)
		
		self.__head = Servo(self.__observation['center_tilt'], self.__observation['center_pan'])
		self.start()
		
	## run
	# .
	def run(self):
		self._running = True
		while self._running:
			start = time.time()
			value = self._bkb.read_int('DECISION_LOCALIZATION')
			print 'value:', value 
			if value == -999:
				self.__head.writeWord(
					self.__observation['ID Pan'],
					self.__motor['Goal Position'],
					self.__observation['center_pan']
				)
				self.__head.writeWord(
					self.__observation['ID Tilt'],
					self.__motor['Goal Position'],
					self.__observation['center_tilt']
				)
			else:
				self.__head.writeWord(
					self.__observation['ID Pan'],
					self.__motor['Goal Position'],
					self.__observation['center_pan']-(value*1023)/300
				)
				self.__head.writeWord(
					self.__observation['ID Tilt'],
					self.__motor['Goal Position'],
					self.__observation['center_tilt']
				)
			 
			self._bkb.write_float(
				'VISION_PAN_DEG',
				(self.__observation['center_pan'] - self.__head.readWord(
						self.__observation['ID Pan'],
						self.__motor['Present Position']
					)
				)*300.0/1023
			)
			
			# Frequency of update
			if start + 1.0/self.__observation['frequency'] - time.time() > 0:
				time.sleep( # Frequency of processing
					start + 1.0/self.__observation['frequency'] - time.time()
				)
	
	## finalize
	# .
	def finalize(self):
		self._running = False
		self.join()
		super(HeadControl, self).finalize(self.__observation)