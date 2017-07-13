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
	
	## observation
	# .
	__observation = None
	
	## step
	# .
	__step = None
	
	def __init__(self, arg):
		print 'Initiating class localization'
		super(LocalizationVision, self).__init__(arg)
		
		# Try to load the points, if it doesn't work, kill the process.
		try:
			self.vector = np.load('./Data/Vector.npy')
			print "\n-= Succeeded loading points. =-\n"
		except:
			print "\n-= Error loading points. =-\n"
		
			print "Run \"python pointsCalibration.py\" in order\nto calibrate the points for the Vision System."
			exit()
		
		self.vals = np.zeros(32)
		self.frames = 5
		self.count = 0
		
		self.__green = ColorSegmentation('Green', None)
		self.__closing = Morphology('Green', 'Closing', None)
		
		self._pause()
		self.start()
		
		if self._args.localization == True:
			self.__green.show = True
			self.__closing.show = True
		
	def main(self, mask, pan):
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
		self._resume()
	
	## run
	def run(self):
		self._running = True
		while self._running:
			with self._pausethread:
				if self._running == False:
				  break
				if self.__step == 0:
					self.__step += 1
					self.__observation['frame'] = self.__green.segmentation(self.__observation['frame'])
			
				if self.__step == 1:
					self.__step += 1
					self.__observation['frame'] = self.__closing.morphologicalTransformations(self.__observation['frame'])
			
				self.__observation['frame'] = self.main(self.__observation['frame'], self.__observation['pos_pan'])
			
				if self._args.localization == True:
					if cv2.waitKey(1) & 0xFF == ord('q'):
						self.__green.show = False
						self.__closing.show = False
						self._args.localization = False
						cv2.destroyAllWindows()
			self._pause()
	
	## finalize
	def finalize(self):
		self._running = False
		self._pausethread.notify()
		self._pausethread.release()
		self.join()
		self.__green.finalize()
		self.__closing.finalize()