# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from BasicThread import * # Class responsible for implementing thread

## Class to Robots
# .
class Robots(BasicThread):
	
	# ---- Variables ----
	
	## observation
	# .
	observation = None
	
	## Constructor Class
	def __init__(self, s, obs):
		super(Robots, self).__init__(s)
		self.observation = obs
		
	## insertObservation
	def insertObservation(self, position):
		print position