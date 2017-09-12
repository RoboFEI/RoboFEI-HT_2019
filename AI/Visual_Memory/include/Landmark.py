# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from KalmanFilter import * # Class responsible for implementing kalman filter methods.

## Class to Landmark
# Class responsible for performing landmarks tracking.
class Landmark(KalmanFilter):
	
	# ---- Variables ----
	
	## Constructor Class
	def __init__(self, s):
		# Instantiating constructor for inherited class.
		super(Landmark, self).__init__(s, "Landmarks")
		
		# Creating characteristic variables for landmarks and reading.
		self._parameters.self.update
		self._parameters = self._conf.readVariables(self._parameters)
		
	## update
	# .
	def update(self, data):
		super(Landmark, self).update(data)
		
		return self._state['x']