# coding: utf-8

# ---- Imports ----

# Libraries to be used
import sys
sys.path.append('../include')
sys.path.append('../src')

import os # Library for interaction with the system
from BasicThread import * # Base class with primary functions
from copy import copy
from time import sleep

# Used class developed by RoboFEI-HT
from ConfigIni import * # Used to read the configuration file

## Class CameraCapture
# Class responsible for performing the observation of domain
class CameraCapture(BasicThread):
	
	# ---- Variables ----
	
	## Camera variable
	# Responsible for communicating with the camera
	camera = None
	
	## frame variable
	# Stores the image taken from the camera
	frame = None
	
	## bkb variable
	# Used to access a shared memory
	bkb = None
	
	## mem variable
	# Memory Pointer
	mem = None
	
	## exe variable
	# Flag responsible for executing camera capture
	exe = None
	
	## Constructor Class
	def __init__(self, memory, memorynumber):
		Thread.__init__(self)
		self.camera = self.CameraOpen()
		self.bkb = memory
		self.mem = memorynumber
		self.start()
		
	## CameraOpen
	# Used to locate the port where the camera is connected and connect to it
	def CameraOpen(self):
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
		return camera
	
	## finalize
	# Terminates the capture process and saves the generated information
	def finalize(self):
		self.exe = False
		self.join()
		self.camera.release()
	
	## run
	# Function that will be executed as a thread
	def run(self):
		self.exe = True
		while self.exe:
			ret, self.frame = self.camera.read() # Capture frame-by-frame
			sleep(1.0/30) # Camera FPS
	
	## currentObservation
	# Sends the current environment information
	def currentObservation(self):
		return copy(self.frame)