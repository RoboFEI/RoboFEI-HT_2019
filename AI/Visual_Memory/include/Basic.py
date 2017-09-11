# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the visual memory system.
from abc import ABCMeta, abstractmethod # Used to create abstract classes.
from copy import copy # Function used to duplicate data.
import sympy as sym # Class used for manipulation of arrays and symbolic variables.

# Used class developed by RoboFEI-HT.
from Blackboard import * # Class used to manage blackboard writing and reading.
from ConfigIni import * # Class used to read the ini file from the view.

## Class to Basic
# Standard and abstract class.
class Basic(object):
	__metaclass__ = ABCMeta
	
	# ---- Variables ----
	
	## _conf
	# Variable used to instantiate class ConfigIni.
	_conf = None
	
	## _bkb
	# Variable used to instantiate class Blackboard.
	_bkb = None
	
	## Constructor Class
	# Instantiating default classes.
	@abstractmethod
	def __init__(self, obj, func):
		# Instantiating default classes
		self._conf = ConfigIni(obj, func)
		self._bkb = Blackboard( )
		
	## _end
	# Finishing classes.
	@abstractmethod
	def _end(self):
		self._conf.end( )