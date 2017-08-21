# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from KalmanFilter import * # Class responsible for implementing kalman filter

## Class to BasicThread
# .
class BasicThread(KalmanFilter):
	__metaclass__ = ABCMeta
	
	# ---- Variables ----
	
	## Constructor Class
	@abstractmethod
	def __init__(self, s):
		super(BasicThread, self).__init__(s)