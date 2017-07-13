# coding: utf-8

# ---- Imports ----

# Libraries to be used
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the vision system

# Used class developed by RoboFEI-HT
from BasicClass import * # 
from VisionException import * # Used to handle exceptions

## Morphology
# .
class Morphology(BasicClass):
	
	# ---- Variables ----
	
	## show
	# .
	show = False
	
	## color
	# .
	__color = False
	
	## func
	# .
	__func = False
	
	## parameters
	# .
	__parameters = False
	
	## kennel
	# .
	__kennel = False
	
	## Constructor Class
	def __init__(self, color, func, arg):
		func = 'Closing'
		color = 'Green'
		self.__func = func
		self.__color = color
		super(Morphology, self).__init__(arg, self.__color, self.__func)
		
		self.__parameters = self._confini.read()
		if self.__parameters == -1:
			self.__parameters = {
				'size_kennel': 1,
				'interaction': 1,
				'morphological': 3,
				'interaction': 1
			}
			
		self.__kennel = cv2.getStructuringElement(
			cv2.MORPH_ELLIPSE,
			(
				self.__parameters['size_kennel'],
				self.__parameters['size_kennel']
			)
		)
		
	## morphologicalTransformations
	def morphologicalTransformations(self, mask):
		mask = cv2.morphologyEx(
			mask,
			self.__parameters['morphological'],
			self.__kennel,
			self.__parameters['interaction']
		)
		if self.show == False:
			return mask
		else:
			return mask
	
	## finalize
	def finalize(self):
		super(Morphology, self).finalize(self.__parameters)