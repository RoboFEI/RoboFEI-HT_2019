# coding: utf-8

# Libraries to be used
import sys
sys.path.append('../include')
sys.path.append('../src')

import os # Library for interaction with the system
from copy import copy
import time
# from datetime import *

# Used class developed by RoboFEI-HT
from BasicThread import * # Base class with primary functions
from Servo import * # 

## Class HeadControl
# .
class HeadControl(BasicThread):
	
	# ---- Variables ----
	
	## servopan
	# .
	__servopan = 19
	
	## servotilt
	# .
	__servotilt = 20
	
	## head
	# .
	__head = None
	
	## observation
	# .
	__observation = None
	
	## Constructor Class
	def __init__(self, arg):
		super(HeadControl, self).__init__(arg, 'Head' , 'parameters')
		
		self.__observation = self.self._confini.read()
		if self.__observation is -1:
			self.__observation = {
				'frequency': 1000,
				'center_pan': 512,
				'center_tilt': 512,
			}
		
		self.__head = Servo(self.__observation['center_tilt'], self.__observation['center_pan'])
		self.start()
		
	## Constructor Class