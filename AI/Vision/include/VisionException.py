# coding: utf-8

# ---- Imports ----

import sys
sys.path.append('../include')
sys.path.append('../src')

## Class to VisionException
# Class used to handle system errors
class VisionException(Exception):
	
	## Constructor Class
	def __init__(self, numbererror, message):
		self.numbererror = numbererror
		print 'Vision System Error:', 
		if numbererror == 0:
			print 'Could not read XML file for', message, 'detection'
		elif numbererror == 1:
			print 'No connected cameras found'
		elif numbererror == 2:
			print 'Unable to connect to port'
		elif numbererror == 3:
			print 'Process kill command detected'