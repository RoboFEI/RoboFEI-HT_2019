# coding: utf-8

# ---- Imports ----

# Libraries to be used
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the vision system

# Used class developed by RoboFEI-HT
from VisionException import * # Used to handle exceptions
from BasicClass import * # Basic support class

## Class to HAAR cascades
# Classifier used to identify objects.
class HaarCascades(BasicClass):
	
	# ---- Variables ----
	
	## Variable HAAR
	# Used to perform HAAR detection and classification
	__haarcascade = None
	
	## myobject
	# Name of myobject
	__myobject = None
	
	## Parameters HAAR
	# Parameters used in the classifier.
	__parametershaar = None
	
	## Constructor Class
	def __init__(self, name, arg):
		print 'Initializing class for ' + name + ' detection'
		super(HaarCascades, self).__init__(name, "HAAR", arg)
		myobject = name
		haarcascade = cv2.CascadeClassifier('./data/' + name + '.xml') # Reading feature XML file
		haarcascade = cv2.CascadeClassifier('../data/haarcascade_frontalface_alt2.xml') # debug-iPython Testando face
		
		try: # Testing whether file exists or is empty
			if haarcascade.empty():
				raise VisionException(0, name)
		except VisionException as e:
			sys.exit()
		
		self.__parametershaar = self._confini.read()
		
		if self.__parametershaar == -1:
			print "Parameters not found for " + name + ", using standard parameters."
			self.__parametershaar = {
				"scaleFactor": 1.1,
				"minNeighbors": 3,
				"minSize": 30,
				"fontScale": 1,
				"subtitleR": 0,
				"subtitleG": 255,
				"subtitleB": 0
			}
		
	## detectHaar
	# Used to detect the object using the HAAR classifier.
	def detectHaar(self, frame):
		objects = haarcascade.detectMultiScale(
			frame,
			scaleFactor = self.__parametershaar["scaleFactor"],
			minNeighbors = self.__parametershaar["minNeighbors"],
			minSize = (self.__parametershaar["minSize"], self.__parametershaar["minSize"])
		)
		if args.visionball == False:
			return
		
		# Draw a rectangle around the objects
		for (x, y, w, h) in objects:
			cv2.rectangle( # Mark detected object
				frame, # Image used for drawing
				(x, y), # Starting position
				(x+w, y+h), # Final position
				(self.__parametershaar["subtitleB"], self.__parametershaar["subtitleG"], self.__parametershaar["subtitleR"]), # Box color
				2 # Line Width
			)
			
			size = cv2.getTextSize( # Text Size
				myobject, # Written text
				cv2.FONT_HERSHEY_SIMPLEX, # Font
				self.__parametershaar["fontScale"], # Font scale
				1 # Line Width
			)[0]
			
			cv2.rectangle( # Drawing text background
				frame, # Image used for drawing
				(x - 1, y - size[1] - 2), # Starting position
				(x + size[0] - 5, y), # Final position
				(self.__parametershaar["subtitleB"], self.__parametershaar["subtitleG"], self.__parametershaar["subtitleR"]), # Box color
				-1 # Line Width - Filling in rectangle
			)
			
			cv2.putText( # Drawing text in the image
				frame, # Image used for drawing
				myobject, # Written text
				(x-3, y-1), # Starting position
				cv2.FONT_HERSHEY_SIMPLEX, # Font
				self.__parametershaar["fontScale"], # Font scale
				(0,0,0) # Font color - White
			)
	
		# Display the resulting frame
		cv2.imshow('Detecting ' + name, frame)
	
	## finalize
	# Terminates the HAAR process and saves the generated information.
	def finalize(self):
		super(HaarCascades, self).finaliza(self.__parametershaar)