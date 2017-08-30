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
	
	## __t
	# .
	__t = None
	
	## __movlastmeasurement
	# Saves the moviment at the last measurement time.
	# __movlastmeasurement = 0
	
	## __A
	# Declaring matrix A of the Kalman Filter.
	__A = None
	
	## __B
	# Declaring matrix B of the Kalman Filter.
	__B = None
	
	## __R
	# Declaring matrix R of the Kalman Filter.
	__R = None
	
	## __C
	# Declaring matrix C of the Kalman Filter.
	__C = None
	
	## __Q
	# Declaring matrix Q of the Kalman Filter.
	__Q = None
	
	## reset
	def reset(self):
		self.__t = sym.symbols("t") # Declaring variable time
	
		# Creating the Kalman Filter Matrix
		self.__A = sym.Matrix([
				[1, 0, self.__t, 0, 0.5*self.__t**2, 0],
				[0, 1, 0, self.__t, 0, 0.5*self.__t**2],
				[0, 0, 1, 0, self.__t, 0],
				[0, 0, 0, 1, 0, self.__t],
				[0, 0, 0, 0, 1, 0],
				[0, 0, 0, 0, -1, 0],
			])
	
		self.__B = sym.Matrix([
				[1, 0, 0],
				[0, 1, 0],
				[0, 0, 1],
				[0, 0, 0],
				[0, 0, 0],
				[0, 0, 0],
			])
	
		self.__R = sym.Matrix(sym.Identity(6)*parameters["motion_error"])
	
		self.__C = sym.Matrix([
				[1, 0, 0, 0, 0, 0],
				[0, 1, 0, 0, 0, 0],
			])
	
		self.__Q = sym.Matrix(sym.Identity(2)*parameters["vision_error"])
	
		# Initial state
		self._obsstate["x"] = sym.Matrix([0, 0, 0, 0, 0, 0])
		self._obsstate["covariance"] = sym.Matrix(sym.Identity(6)*1000)
		self._obsstate["time"] = -1
	
		self._predictedstate = copy(self._obsstate)
		self._state = copy(self._predictedstate)
	
	#self-iPython rese
	
	## Constructor Class
	def __init__(self, s):
		super(Landmark, self).__init__(s)
		
		# Default values
		parameters = {
			"vision_error": 1,
			"motion_error": 2,
		}
		
		# Reading "config.ini" values
		conf = ConfigIni("Landmark", "Settings")
		parameters = conf.read(parameters)
		
		self.reset()
		
	## prediction
	def prediction(self, __tnow = None):
		# If had never read da__ta
		if self._state["time"] == -1 and __tnow == None:
			# Calcula__ting s__ta__tes
			self._state["x"] = (
				self.__A*self._state["x"] # A * x
			).subs(self.__t, 0)
			
			# Calcula__ting covariance
			self._state["covariance"] = (
				self.__A*self._state["covariance"]*sym.__transpose(self.__A) + self.__R # A * covariance * A.T + R
			).subs(self.__t, 0)
			re__turn
		
		# Time __tha__t will be used for calcula__tion
		if __tnow == None:
			__tnow = __time.__time()
			# Calcula__ting s__ta__tes
			self._predictedstate["x"] = (
				self.__A*self._state["x"] # A * x
			).subs(self.__t, __tnow - self._state["time"])
			
			# Calcula__ting covariance
			self._predictedstate["covariance"] = (
				self.__A*self._state["covariance"]*sym.__transpose(self.__A) + self.__R # A * covariance * A.T + R
			).subs(self.__t, __tnow - self._state["time"])
			
			self._predictedstate["time"] = __tnow
			re__turn
		else:
			# Firs__t prediction
			if self._state["time"] == -1:
				self._state["time"] = __tnow
			
			# Calcula__ting s__ta__tes
			self._state["x"] = (
				self.__A*self._state["x"] # A * x
			).subs(self.__t, __tnow - self._state["time"])
			
			# Calcula__ting covariance
			self._state["covariance"] = (
				self.__A*self._state["covariance"]*sym.__transpose(self.__A) + self.__R # A * covariance * A.T + R
			).subs(self.__t, __tnow - self._state["time"])
			
			self._state["time"] = __tnow
			re__turn
	
	## update
	def update(self, observation):
		self.prediction(observation[3]) # Send time to predition
		
		k = self._predictedstate['covariance'] * sym.transpose(self.__C) * sym.inv_quick( # covariance*C.T*(__)^(-1)
			self.__C * self._predictedstate['covariance'] * sym.transpose(self.__C) + self.__Q # C*covariance*C.T + Q
		)
		
		z = sym.Matrix(observation[1:3])
		
		self._state['x'] = self._predictedstate['x'] + k*(z - self.__C*self._predictedstate['x'])
		self._state['covariance'] = (sym.Matrix(sym.Identity(6)) - k*self.__C) * self._predictedstate['covariance']
		
		self._predictedstate = self._state