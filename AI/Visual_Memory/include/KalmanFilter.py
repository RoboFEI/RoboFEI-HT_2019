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
    _p_x = None; _p_y = None; _v_x = None; _v_y = None; _a_x = None; _a_y = None; _b_x = None; _b_y = None
    
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
                [-self._t, 0, self._p_x, self._p_y, 0],
                [0, -self._t, self._p_y, -self._p_x, 0],
                [0, 0, self._v_x, self._v_y, 0],
                [0, 0, self._v_y, -self._v_x, 0],
                [0, 0, self._a_x, self._a_y, 0],
                [0, 0, self._a_y, -self._a_x, 0],
            ])
    
        self._R = sym.Matrix(sym.Identity(6))
    
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
        super(KalmanFilter,self).__init__("Kalman Filter", obj)
        
        # Creating standard parameters and reading
        self._parameters = {
            "vision_error": 0.1,
        }
        
        self._parameters = self._conf.readVariables(self._parameters)
        
        # Variable to robot speed
        self._speeds = s
        
        self._t = sym.symbols("t") # Declaring variable time
        
        # Status variables
        self._p_x, self._p_y = sym.symbols("p_x, p_y")
        self._v_x, self._v_y = sym.symbols("v_x, v_y")
        self._a_x, self._a_y = sym.symbols("a_x, a_y")
        
    ## __predictNow
    # Performs the prediction using the current instant in time to determine the new state.
    # def __predictNow(self, tnow = None, movements = None):
    #     if _state["time"] != -1: # Checking if you can hear at least one measurement.
    #         # Time that will be used for calculation
    #         tnow = time.time()
    #     else:
    #         tnow = -1
    
    #     # Calculating states
    #     _state["x"] = (
    #         _A*_state["x"] # A * x
    #     ).subs([
    #         [_t, tnow - _state["time"]], # Inserting delta time
    #     ])
    
    #     _state["x"] = (
    #         _B*_speeds[movements]["U"] # B * U
    #     ).subs([
    #         [_t, tnow - _state["time"]], # Inserting delta time
            
    #         # State Variables
    #         [_p_x, _state["x"][0]],
    #         [_p_y, _state["x"][1]],
    #         [_v_x, _state["x"][2]],
    #         [_v_y, _state["x"][3]],
    #         [_a_x, _state["x"][4]],
    #         [_a_y, _state["x"][5]],
    #     ])
    
    #     # Calculating covariance
    #     _state["covariance"] = (
    #         _A*_state["covariance"]*sym.transpose(_A) + _R*_speeds[movements]["R"] # A * covariance * A.T + R
    #     ).subs([
    #         [_t, tnow - _state["time"]],
    #     ])
        
    #     _state["x"] = sym.Matrix(_state["x"])
    #     for x in xrange(2,len(_state["x"])):
    #         if abs(_state["x"][x]) < _parameters["vision_error"]/2:
    #             _state["x"][x] = 0
    #         if (x == 2 or x == 3) and _state["x"][x] == 0:
    #             _state["x"][x+2] = 0
    
    #     _state["time"] = tnow
    
    ## __predictTime
    # Uses a current instant in time and updates the observation and the current state.
    def __predictTime(self, tnow = None, movements = None):
        
        if self._predictedstate["time"] == -1: # Checking if you can hear at least one measurement.
            self._predictedstate["time"] = tnow
            
        # Calculating stop time (speed equal to zero)
        times = [tnow]
        for i in xrange(2,4):
            a = -self._predictedstate["x"][i]/self._predictedstate["x"][i+2]
            if a == sym.nan or a == sym.zoo or a < 0 :
                times.append(tnow)
            else:
                times.append(float(self._predictedstate["time"] + a))
        while tnow > min([n for n in times if n>=0]):
            self.__predictTime(tnow=min([n for n in times if n>0]), movements=movements)
            times = [tnow]
            for i in xrange(2,4):
                a = -self._predictedstate["x"][i]/self._predictedstate["x"][i+2]
                if a == sym.nan or a == sym.zoo:
                    times.append(tnow)
                else:
                    times.append(float(self._predictedstate["time"] + a))
            
        # Calculating states
        self._predictedstate["x"] = (
            self._A*self._predictedstate["x"] # A * x
        ).subs([
            [self._t, tnow - self._predictedstate["time"]], # Inserting delta time
        ])
    
        self._predictedstate["x"] = (
            self._B*self._speeds[movements]["x_speed"] # B * U
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
    #     print _A.shape, _predictedstate["covariance"].shape, _R.shape, _speeds[movements]["R"].shape
        self._predictedstate["covariance"] = (
            self._A*self._predictedstate["covariance"]*sym.transpose(self._A) + self._R*self._speeds[movements]["R"] # A * covariance * A.T + R
        ).subs([
            [self._t, tnow - self._predictedstate["time"]],
        ])
        
        # Resetting acceleration if speed equals zero
        self._predictedstate["x"] = sym.Matrix(self._predictedstate["x"])
        for x in xrange(len(self._predictedstate["x"])):
    #         print x, "Testando", _predictedstate["x"][x]
            if x != 2 and x != 3 and abs(self._predictedstate["x"][x]) < self._parameters["vision_error"]/2:
    #             print "Foi"
                self._predictedstate["x"][x] = 0.0
            elif abs(self._predictedstate["x"][x]) < self._parameters["vision_error"]/2:
    #             print "Foi"
                self._predictedstate["x"][x] = 0.0
                self._predictedstate["x"][x+2] = 0.0
    
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
        self.predict(data["time"], data["movement"])
        
        k = self._predictedstate["covariance"] * sym.transpose(self._C) * sym.inv_quick( # covariance*C.T*(_)^(-1)
            self._C * self._predictedstate["covariance"] * sym.transpose(self._C) + self._Q # C*covariance*C.T + Q
        )
        
        z = sym.Matrix(data["pos"])
        
        self._predictedstate["x"] = self._predictedstate["x"] + k*(z - self._C*self._predictedstate["x"])
        self._predictedstate["covariance"] = (sym.Matrix(sym.Identity(6)) - k*self._C) * self._predictedstate["covariance"]
        
        # Resetting acceleration if speed equals zero
        self._predictedstate["x"] = sym.Matrix(self._predictedstate["x"])
        for x in xrange(len(self._predictedstate["x"])):
            if x != 2 and x != 3 and abs(self._predictedstate["x"][x]) < self._parameters["vision_error"]/2:
                self._predictedstate["x"][x] = 0.0
            elif abs(self._predictedstate["x"][x]) < self._parameters["vision_error"]/2:
                self._predictedstate["x"][x] = 0.0
                self._predictedstate["x"][x+2] = 0.0
        
        self._state = copy(self._predictedstate)