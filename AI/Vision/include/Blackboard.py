# coding: utf-8

# ---- Imports ----

# Libraries to be used
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the vision system
import configparser # Used to read ini files

# Used class developed by RoboFEI-HT
from VisionException import * # Used to handle exceptions

# Import a shared memory
sys.path.append('../Blackboard/src/')
from SharedMemory import SharedMemory

## Class to config ini
# Class used to read the ini file from the view.
class Blackboard( ):
	
	## mem
	__mem = None
	
	## bkb
	__bkb = None
	
	## Constructor Class
	def __init__(self):
		self.__bkb = SharedMemory()
		self.__mem = configparser.RawConfigParser()
		if self.__mem.read('../Control/Data/config.ini') is not [] and "Communication" in self.__mem.sections() and "no_player_robofei" in self.__mem["Communication"].keys():
			self.__mem = int(self.__mem["Communication"]["no_player_robofei"])*100
		else:
			print 'Could not read config, no robot number'
			sys.exit()
		
		self.__mem = self.__bkb.shd_constructor(self.__mem)
		
	## write_float
	def write_float(self, variable, value):
		self.__bkb.write_float(self.__mem, variable, value)
	
	## read_float
	def read_float(self, variable):
		return self.__bkb.read_float(self.__mem, variable)
	
	## write_int
	def write_int(self, variable, value):
		self.__bkb.write_int(self.__mem, variable, value)
	
	## read_int
	def read_int(self, variable):
		return self.__bkb.read_int(self.__mem, variable)