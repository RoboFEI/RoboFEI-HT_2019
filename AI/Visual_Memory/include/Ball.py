# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from BasicThread import * # Class responsible for implementing thread

## Class to Ball
# .
class Ball(BasicThread):
	
	# ---- Variables ----
	
	## Constructor Class
	def __init__(self, s):
		super(Ball, self).__init__(s)