# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append("../include")
sys.path.append("../src")

# The standard libraries used in the visual memory system.
import time # Libraries used for time management.
import numpy as np # Used for matrix calculations.

# Used class developed by RoboFEI-HT.
from Basic import * # Standard and abstract class.
from Speeds import * # Class responsible for managing the robot"s possible speeds (me).

## Class to KalmanFilter
# Class responsible for implementing kalman filter methods.
class KalmanFilter(Basic):
	__metaclass__ = ABCMeta
	
	# ---- Variables ----
	
	## _parameters
	# Variable used to instantiate class responsible for robot speed.
	_parameters = None
	
	## _speeds
	# Variable used to instantiate class responsible for robot speed.
	_speeds = None
	
	## _t
	# Time variable used in kalman filter.
	_t = None
	
	## _predictedstate
	# Variable used to make predictions from observations.
	_predictedstate = { }
	
	## _state
	# Variable used to predict the position of the object at the current instant.
	_state = { }
	
	# Matrix used in kalman filter.
	_A = None; _B = None; _R = None; _C = None; _Q = None
	
	# Status variables.
	_p_x = None; _p_y = None; _v_x = None; _v_y = None; _a_x = None; _a_y = None
	
	## _reset
	def _reset(self):
		# Creating the Kalman Filter Matrix
		self._A = sym.Matrix([
				[1, 0, self._t, 0, 0.5*self._t**2, 0],
				[0, 1, 0, self._t, 0, 0.5*self._t**2],
				[0, 0, 1, 0, self._t, 0],
				[0, 0, 0, 1, 0, self._t],
				[0, 0, 0, 0, 1, 0],
				[0, 0, 0, 0, 0, 1],
			])
	
		self._B = sym.Matrix([
				[-self._t, 0, self._p_x, self._p_y],
				[0, -self._t, self._p_y, -self._p_x],
				[0, 0, self._v_x, self._v_y],
				[0, 0, self._v_y, -self._v_x],
				[0, 0, self._a_x, self._a_y],
				[0, 0, self._a_y, -self._a_x],
			])
	
		self._R = sym.Matrix(sym.Identity(6)*self._parameters["motion_error"])
	
		self._C = sym.Matrix([
				[1, 0, 0, 0, 0, 0],
				[0, 1, 0, 0, 0, 0],
			])
	
		self._Q = sym.Matrix(sym.Identity(2)*self._parameters["vision_error"])
	
		# Initial state
		self._predictedstate["x"] = sym.Matrix([0, 0, 0, 0, 0, 0])
		self._predictedstate["covariance"] = sym.Matrix(sym.Identity(6)*1000)
		self._predictedstate["time"] = -1
	
		self._state = copy(self._predictedstate)
	
	## Constructor Class
	# Responsible for starting the matrices of kalman patterns.
	@abstractmethod
	def __init__(self, s, obj):
		
		# Instantiating parent class
		super(KalmanFilter,self)._init_("Kalman Filter", obj)
		
		# Creating standard parameters and reading
		self._parameters = {
			"motion_error": 1,
			"vision_error": 1,
		}
		
		self._parameters = self._conf.readVariables(self._parameters)
		
		# Variable to robot speed
		self._speeds = s
		
		self._t = sym.symbols("t") # Declaring variable time
		
		# Status variables
		self._p_x, self._p_y = sym.symbols("p_x, p_y")
		self._v_x, self._v_y = sym.symbols("v_x, v_y")
		self._a_x, self._a_y = sym.symbols("a_x, a_y")
		
		self._reset()
		
	## __predictNow
	# Performs the prediction using the current instant in time to determine the new state.
	def __predictNow(self, time = None, movements = None):
		# Time that will be used for calculation
		tnow = time.time()
	
		# Calculating states
		self._state["x"] = (
			self._A*self._state["x"] # A * x
		).subs([
			[self._t, tnow - self._state["time"]], # Inserting delta time
		])
	
		self._state["x"] = (
			self._B*self._speeds[movements]["U"] # B * U
		).subs([
			[self._t, tnow - self._state["time"]], # Inserting delta time
			
			# State Variables
			[self._p_x, self._state["x"][0]],
			[self._p_y, self._state["x"][1]],
			[self._v_x, self._state["x"][2]],
			[self._v_y, self._state["x"][3]],
			[self._a_x, self._state["x"][4]],
			[self._a_y, self._state["x"][5]],
		])
	
		# Calculating covariance
		self._state["covariance"] = (
			self._A*self._state["covariance"]*sym.transpose(self._A) + self._R # A * covariance * A.T + R
		).subs([
			[self._t, tnow - self._state["time"]],
		])
	
		self._state["time"] = tnow
	
	## __predictTime
	# Uses a current instant in time and updates the observation and the current state.
	def __predictTime(self, tnow = None, movements = None):
		# Calculating states
		self._predictedstate["x"] = (
			self._A*self._predictedstate["x"] # A * x
		).subs([
			[self._t, tnow - self._predictedstate["time"]], # Inserting delta time
		])
	
		self._predictedstate["x"] = (
			self._B*self._speeds[movements]["U"] # B * U
		).subs([
			[self._t, tnow - self._predictedstate["time"]], # Inserting delta time
			
			# State Variables
			[self._p_x, self._predictedstate["x"][0]],
			[self._p_y, self._predictedstate["x"][1]],
			[self._v_x, self._predictedstate["x"][2]],
			[self._v_y, self._predictedstate["x"][3]],
			[self._a_x, self._predictedstate["x"][4]],
			[self._a_y, self._predictedstate["x"][5]],
		])
	
		# Calculating covariance
		self._predictedstate["covariance"] = (
			self._A*self._predictedstate["covariance"]*sym.transpose(self._A) + self._R # A * covariance * A.T + R
		).subs([
			[self._t, tnow - self._predictedstate["time"]],
		])
	
		self._predictedstate["time"] = tnow
		
		self._state = copy(self._predictedstate["time"])
	
	## predict
	# .
	def predict(self, tnow = None, movements = None):
		{
			(float, int): self.__predictTime,
			(type(None), int): self.__predictNow,
		}[(type(tnow), type(movements))](tnow, movements)
	
	## update
	# .
	def update(self, data):
		# Predicting value in observation time.
		self.predict(data["time"], 0)
		
		k = self._predictedstate["covariance"] * sym.transpose(self._C) * sym.inv_quick( # covariance*C.T*(_)^(-1)
			self._C * self._predictedstate["covariance"] * sym.transpose(self._C) + self._Q # C*covariance*C.T + Q
		)
		
		z = sym.Matrix(data["pos"])
		
		self._predictedstate["x"] = self._predictedstate["x"] + k*(z - self._C*self._predictedstate["x"])
		self._predictedstate["covariance"] = (sym.Matrix(sym.Identity(6)) - k*self._C) * self._predictedstate["covariance"]
		
		self._state = copy(self._predictedstate)