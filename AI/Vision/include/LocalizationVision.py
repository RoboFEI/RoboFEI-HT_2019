# coding: utf-8

import numpy as np
import sys
sys.path.append('../include')
sys.path.append('../src')
from BasicClass import *
from BasicThread import * # Base class with primary functions
from ColorSegmentation import * #
from Morphology import * #

def write(v):
	x = 0
	for i in range(32):
		x += int(v[i]) << i
	return x

#--------------------------------------------------------------------------------------------------
#   Class used for the vision system.
#--------------------------------------------------------------------------------------------------
class LocalizationVision(BasicThread):
 #----------------------------------------------------------------------------------------------
 #   Constructor gets the BlackBoard object and the memory key.
 #----------------------------------------------------------------------------------------------
	
	# ---- Variables ----
	
	## show
	# .
	show = False
	
	## observation
	# .
	__observation = None
	
	## step
	# .
	__step = None
	
	def __init__(self, arg):
		super(LocalizationVision, self).__init__(arg)
		
		# Try to load the points, if it doesn't work, kill the process.
		try:
			self.vector = np.load('./Data/vector.npy')
			print "\n-= Succeeded loading points. =-\n"
		except:
			print "\n-= Error loading points. =-\n"
		
			print "Run \"python pointsCalibration.py\" in order\nto calibrate the points for the Vision System."
			exit()
		
		self.vals = np.zeros(32)
		self.frames = 5
		self.count = 0
		
		self.green = ColorSegmentation('Green', None)
		self.closing = Morphology('Green', 'Closing', None)
		
	def main(mask, pan):
		p = []
		for i in self.vector:
			p.append(mask[tuple(i)])
	
		if self.count < self.frames:
			self.vals += np.array(p)
			self.count += 1
		else:
			self.vals /= self.frames * 255.
			x = np.rint(self.vals)
			s = np.mean(np.abs(self.vals-x))
	
			self._bkb.write_int('iVISION_FIELD', write(x))
			self._bkb.write_float('fVISION_FIELD', int(pan)+s)
	
			self.vals = np.zeros(32)
			self.frames = 5
			self.count = 0
	
	## find
	def find(self, observation, step):
		self.__observation = observation.copy()
		self.__step = step
		self.start()
	
	## run
	def run(self):
		if self.__step == 0:
			self.__step += 1
			self.__observation['frame'] = self.green.segmentation(self.__observation['frame'])
		
		if self.__step == 1:
			self.__step += 1
			self.__observation['frame'] = self.closing.morphologicalTransformations(self.__observation['frame'])
		
		self.__observation['frame'] = main(self.__observation['frame'], self.__observation['pos_pan'])
	
	## finalize
	def finalize(self):
		self.green.finalize()
		self.closing.finalize()
