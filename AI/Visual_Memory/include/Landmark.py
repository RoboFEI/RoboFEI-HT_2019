# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append("../include")
sys.path.append("../src")

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from BasicThread import * # Class responsible for implementing thread

## Class to Landmark
# .
class Landmark(BasicThread):
	
	# ---- Variables ----
	
	## __tlastmeasurement
	# Saves the instant at the last measurement time.
	__tlastmeasurement = -1
	
	## __movlastmeasurement
	# Saves the moviment at the last measurement time.
	__movlastmeasurement = 0
	
	## __A
	# Declaring matrix A of the Kalman Filter.
	__A = None
	
	## __C
	# Declaring matrix C of the Kalman Filter.
	__C = None
	
	## reset
	def reset(self):
		t = sym.symbols("t") # Declaring variable time
	
		# Creating the Kalman Filter Matrix
		self.__A = sym.Matrix([
				[1, 0, t, 0, 0.5*t**2, 0],
				[0, 1, 0, t, 0, 0.5*t**2],
				[0, 0, 1, 0, t, 0],
				[0, 0, 0, 1, 0, t],
				[0, 0, 0, 0, 1, 0],
				[0, 0, 0, 0, -1, 0],
			])
	
		self.__C = sym.Matrix([
				[1, 0, 0, 0, 0, 0],
				[0, 1, 0, 0, 0, 0],
			])
	
		__R = sym.Matrix(sym.Identity(6)*parameters["motion_error"])
	
		__Q = sym.Matrix(sym.Identity(2)*parameters["vision_error"])
	
		# Initial state
		self._predictedstate["x"] = sym.Matrix([0, 0, 0, 0, 0, 0])
		self._predictedstate["covariance"] = sym.Matrix(sym.Identity(6)*1000)
		self._predictedstate["time"] = -1
	
		self._state = self._predictedstate
	
	## Constructor Class
	def __init__(self, s):
		super(Landmark, self).__init__(s)
		
		# Default values
		parameters = {
			"vision_error": 2,
			"motion_error": 2,
		}
		
		# Reading "config.ini" values
		conf = ConfigIni("Landmark", "Settings")
		parameters = conf.read(parameters)
		
		self.reset()
		
	## prediction
	def prediction(self, tnow = None):
		# If had never read data
		if self._state["time"] == -1 and tnow == None:
			# Calculating states
			self._state["x"] = (
				self.__A*self._state["x"] # A * x
			).subs(t, 0)
			
			# Calculating covariance
			self._state["covariance"] = (
				self.__A*self._state["covariance"]*sym.transpose(self.__A) + __R # A * covariance * A.T + R
			).subs(t, 0)
			return
		
		# Time that will be used for calculation
		if tnow == None:
			tnow = time.time()
			# Calculating states
			self._predictedstate["x"] = (
				self.__A*self._state["x"] # A * x
			).subs(t, tnow - self._state["time"])
			
			# Calculating covariance
			self._predictedstate["covariance"] = (
				self.__A*self._state["covariance"]*sym.transpose(self.__A) + __R # A * covariance * A.T + R
			).subs(t, tnow - self._state["time"])
			
			self._predictedstate["time"] = tnow
			return
		else:
			# First prediction
			if self._state["time"] == -1:
				self._state["time"] = tnow
			
			# Calculating states
			self._state["x"] = (
				self.__A*self._state["x"] # A * x
			).subs(t, tnow - self._state["time"])
			
			# Calculating covariance
			self._state["covariance"] = (
				self.__A*self._state["covariance"]*sym.transpose(self.__A) + __R # A * covariance * A.T + R
			).subs(t, tnow - self._state["time"])
			
			self._state["time"] = tnow
			return
	
	## update
	def update(self, observation):
		self.prediction(observation[3]) # Send time to predition
		
		k = self._predictedstate['covariance'] * sym.transpose(self.__C) * sym.inv_quick( # covariance*C.T*(__)^(-1)
			self.__C * self._predictedstate['covariance'] * sym.transpose(self.__C) + __Q # C*covariance*C.T + Q
		)
		
		z = sym.Matrix(observation[1:3])
		
		self._state['x'] = self._predictedstate['x'] + k*(z - self.__C*self._predictedstate['x'])
		self._state['covariance'] = (sym.Matrix(sym.Identity(6)) - k*self.__C) * self._predictedstate['covariance']
		
		self._predictedstate = self._state