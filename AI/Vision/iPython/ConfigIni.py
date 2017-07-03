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

## Class to config ini
# Class used to read the ini file from the view.
class ConfigIni( ):
	
	## Dictionary
	# Section used.
	__dictionary = None
	
	## myobject
	__myobject = None
	
	## function
	__function = None
	
	## __conf
	__conf = None
	
	## Constructor Class
	def __init__(self, obj, func):
		self.__myobject = obj
		self.__function = func
		self.__conf = configparser.RawConfigParser()
		if self.__conf.read("./data/config.ini") is not [] and (self.__myobject + " " + self.__function).upper() in self.__conf.sections():
			self.__dictionary = {}
			for key in self.__conf[(self.__myobject + " " + self.__function).upper()].keys():
				try:
					self.__dictionary[str(key)] = self.__conf.getint((self.__myobject + " " + self.__function).upper(), str(key))
					continue
				except:
					pass
		
				try:
					self.__dictionary[str(key)] = self.__conf.getfloat((self.__myobject + " " + self.__function).upper(), str(key))
					continue
				except:
					pass
		
				try:
					self.__dictionary[str(key)] = self.__conf.getboolean((self.__myobject + " " + self.__function).upper(), str(key))
					continue
				except:
					pass
		
				try:
					self.__dictionary[str(key)] = self.__conf.get((self.__myobject + " " + self.__function).upper(), str(key))
					continue
				except:
					pass
		else:
			self.__dictionary = -1
		
	## read
	def read(self):
		return self.__dictionary
	
	## finaliza
	def finaliza(self, dictionary):
		self.__dictionary = dictionary # Saving dictionary in class
		
		# Saving section parameters
		with open('./data/config.ini', 'w') as configfile:
			self.__conf[(self.__myobject + " " + self.__function).upper()] = self.__dictionary
			self.__conf.write(configfile)