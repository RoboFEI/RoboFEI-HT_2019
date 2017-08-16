# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from Basic import * # Class with implementations and basic variables

## Class to KalmanFilter
# .
class KalmanFilter(Basic):
	__metaclass__ = ABCMeta
	
	# ---- Variables ----
	
	## Constructor Class
	@abstractmethod
	def __init__(self):
		pass
		
	## update
	def update(self, measurements):
		return None
	
	## prediction
	def prediction(self):
		pass