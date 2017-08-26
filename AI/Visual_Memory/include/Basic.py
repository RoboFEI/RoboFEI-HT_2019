# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the visual memory system.
from abc import ABCMeta, abstractmethod # Used to create abstract classes.
from ConfigIni import * # Used to read file "config.ini".

# Used class developed by RoboFEI-HT.

## Class to Basic
# .
class Basic( ):
	__metaclass__ = ABCMeta
	
	# ---- Variables ----
	
	## Constructor Class
	@abstractmethod
	def __init__(self):
		pass