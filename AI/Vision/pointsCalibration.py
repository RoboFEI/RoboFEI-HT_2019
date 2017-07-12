# coding: utf-8

import cv2
import numpy as np

#--------------------------------------------------------------------------------------------------
#   Class used for the vision system.
#--------------------------------------------------------------------------------------------------
class PointCalibration():
	#----------------------------------------------------------------------------------------------
	#   Constructor.
	#----------------------------------------------------------------------------------------------
	def __init__(self):
		self.cap = None
		self.img = None
		self.vector = None
		self.mouse = None
		self.clicks = 0

	#----------------------------------------------------------------------------------------------
	#   Initializes the capture from camera.
	#----------------------------------------------------------------------------------------------
	def InitCap(self):
		self.cap = cv2.VideoCapture(0)

	#----------------------------------------------------------------------------------------------
	#   Captures a image with the camera.
	#----------------------------------------------------------------------------------------------
	def Capture(self):
		try:
			_, self.img = self.cap.read()
		except:
			print "Error on frame capture"
			self.img = np.zeros((512,512,3), np.uint8)

	#----------------------------------------------------------------------------------------------
	#   Generates the positions vector, to be used for localization.
	#----------------------------------------------------------------------------------------------
	def PointGenerator(self):
		self.img = None
		self.vector = np.zeros([32,2])
		cv2.namedWindow('ROBOT VISION')
		cv2.setMouseCallback('ROBOT VISION', self.getpoint)
		
		print "\nPress s to skip.\n"

		while self.clicks < 32:
			try:
				self.Capture()
				for p in self.vector:
					if np.sum(p) != 0:
						cv2.circle(self.img, (int(p[1]), int(p[0])), 2, (255,255,0), -1)
				cv2.imshow('ROBOT VISION', self.img)
			except:
				print "-= ERROR ON METHOD PointGenerator =-"

			k = cv2.waitKey(20) & 0xFF
			if k == 27:
				break

			if self.clicks > 0:
				self.vector[self.clicks-1] = self.mouse

		if self.clicks == 32:
			np.save('./Data/Vector', self.vector)
			print "Saved archive with points."
		else:
			print "Points where not saved."
			exit()

	#----------------------------------------------------------------------------------------------
	#   Main method.
	#----------------------------------------------------------------------------------------------
	def Main(self):
		self.InitCap()

		try:
			self.vector = np.load('./Data/Vector.npy')
		except:
			self.PointGenerator()

		print "\nIf changes are needed press n,\nelse press ESC or q.\n"

		while True:
			try:
				self.Capture()
				for p in self.vector:
					cv2.circle(self.img, (int(p[1]), int(p[0])), 2, (255,255,0), -1)
				cv2.imshow('ROBOT VISION', self.img)
			except:
				print "-= ERROR ON METHOD Main =-"

			k = cv2.waitKey(20) & 0xFF
			if k == 27 or k == ord('q'):
				break
			elif k == ord('n'):
				self.clicks = 0
				self.PointGenerator()
				print "\nIf changes are needed press n,\nelse press ESC or q.\n"
		
		self.cap.release()
		cv2.destroyAllWindows()

	#--------------------------------------------------------------------------------------------------
	#   Event to get mouse click
	#--------------------------------------------------------------------------------------------------
	def getpoint(self, event, x, y, flags, param):
		if event == cv2.EVENT_LBUTTONDOWN and self.clicks < 32:
			self.mouse = (y,x)
			self.clicks += 1
			print self.clicks, self.mouse

P = PointCalibration()
P.Main()