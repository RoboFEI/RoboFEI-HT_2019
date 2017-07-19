# coding: utf-8

# Libraries to be used
import sys
sys.path.append('../include')
sys.path.append('../src')

import os # Library for interaction with the system
from copy import copy
import time
# from datetime import *

# Used class developed by RoboFEI-HT
from BasicThread import * # Base class with primary functions

## Class CameraCapture
# Class responsible for performing the observation of domain
class CameraCapture(BasicThread):
	
	# ---- Variables ----
	
	## Camera variable
	# Responsible for communicating with the camera.
	__camera = None
	
	## Port variable
	# Port where the camera is connected.
	__port = None
	
	## observation variable
	# Saves the observation of the most recent state.
	__observation = None
	
	## exe variable
	# Flag responsible for executing camera capture
	__exe = None
	
	## cameraOpen
	# Used to locate the port where the camera is connected and connect to it
	def cameraOpen(self):
		p = os.popen('ls /dev/video*')
		line = p.readline()
		if line == '':
			raise VisionException(1, '')
		
		for port in xrange(10):
			camera = cv2.VideoCapture(port)
			if camera.isOpened():
				break
		
		if not camera.isOpened():
			raise VisionException(2, '')
		return camera, port
	
	## trackbarFocus
	# Responsible for reading the values of the trackbar.
	def __trackbarFocus(self, value):
		self.__observation['focus'] = value
		os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c focus_absolute=" + str(self.__observation['focus']))
	
	## trackbarSaturation
	# Responsible for reading the values of the trackbar.
	def __trackbarSaturation(self, value):
		self.__observation['saturation'] = value
		os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c saturation=" + str(self.__observation['saturation']))
	
	## finalize
	# Terminates the capture process and saves the generated information
	def finalize(self):
		self.__exe = False
		self.join()
		self.__camera.release()
		del self.__observation['frame']
		del self.__observation['pos_tilt']
		del self.__observation['pos_pan']
		del self.__observation['time']
		super(CameraCapture,self).finalize(self.__observation)
	
	## Constructor Class
	def __init__(self, arg):
		super(CameraCapture, self).__init__(arg, 'Camera' , 'parameters')
		
		self.__observation = self._confini.read()
		if self.__observation is -1:
			self.__observation = {
				'fps': 30,
				'focus': 25,
				'saturation': 128,
			}
		
		self.__camera, self.__port = self.cameraOpen()
		
		self.__camera.set(3,1280)
		self.__camera.set(4,720)
		
		os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c focus_auto=0")
		os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c focus_absolute=" + str(self.__observation['focus']))
		os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c saturation=" + str(self.__observation['saturation']))
		
		self.start()
		
	## run
	# Function that will be executed as a thread
	def run(self):
		self.__exe = True
		
		if self._args.camera is True:
			cv2.namedWindow('Camera parameters')
			cv2.createTrackbar('focus', 'Camera parameters', self.__observation['focus'], 250, self.__trackbarFocus)
			cv2.createTrackbar('saturation', 'Camera parameters', self.__observation['saturation'], 255, self.__trackbarSaturation)
		
		while self.__exe:
			if self._args.camera == True or self._args.camera == 'off':
				os.system('clear') # Cleaning terminal
	#			 clear_output()
				start = time.time()
			
			ret, self.__observation['frame'] = self.__camera.read()
			self.__observation['pos_tilt'] = self._bkb.read_float('VISION_TILT_DEG')
			self.__observation['pos_pan'] = self._bkb.read_float('VISION_PAN_DEG')
			self.__observation['time'] = time.localtime()
			
			if self._args.camera == True:
				cv2.imshow('Camera parameters', self.__observation['frame'])
				if cv2.waitKey(1) & 0xFF == ord('q'):
					self._args.camera = 'off'
					cv2.destroyAllWindows()
			else:
				time.sleep(1.0/self.__observation['fps']) # Camera fps
			
			if self._args.camera == True or self._args.camera == 'off':
				diff = time.time() - start
				print 'Diff:', diff, 'FPS medido:', 1.0/(diff)
	
	## currentObservation
	def currentObservation(self):
		return self.__observation.copy()