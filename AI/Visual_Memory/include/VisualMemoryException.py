# coding: utf-8

## Class to VisualMemoryException
# Class used to handle system errors
class VisualMemoryException(Exception):
	
	## Constructor Class
	def __init__(self, numbererror, message):
		self.numbererror = numbererror
		if numbererror == 5:
			print 'Solicitação encerramento de processo pela thread', message
			return
		print 'Vision System Error:', 
		if numbererror == 0:
			print message
		elif numbererror == 1:
			print 'No connected cameras found'
		elif numbererror == 2:
			print 'Unable to connect to port'
		elif numbererror == 3:
			print 'Process kill command detected'