# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append("../include")
sys.path.append("../src")

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from KalmanFilter import * # Class responsible for implementing kalman filter methods.

## Class to Robots
# Class responsible for performing robots tracking.
class Robots(KalmanFilter):
    
    # ---- Variables ----
    
    ## reset
    # .
    def reset(self):
        super(Robots, self)._reset( )
        
        self._A = self._A[:-2,:-2]
        self._B = self._B[:-2,:]
        self._R = self._R[:-2,:-2]
        self._C = self._C[:,:-2]
        
        self._predictedstate["x"] = self._predictedstate["x"][:-2,:]
        self._predictedstate["covariance"] = self._predictedstate["covariance"][:-2,:-2]
    
    ## Constructor Class
    def __init__(self, s):
        # Instantiating constructor for inherited class.
        super(Robots, self).__init__(s, "Robots")
        
        # Creating characteristic variables for Robots and reading.
        self._parameters.update({ })
        self._parameters = self._conf.readVariables(self._parameters)
        
        self.reset( )