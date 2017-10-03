# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append("../include")
sys.path.append("../src")

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from KalmanFilter import * # Class responsible for implementing Kalman filter methods.

## Class to Landmark
# Class responsible for performing landmarks tracking.
class Landmark(KalmanFilter):
    
    # ---- Variables ----
    
    ## reset
    # .
    def reset(self):
        super(Landmark, self)._reset( )
        
        self._B = sym.Matrix([
            [0, 0, 0, 0, self._px],
            [0, 0, 0, 0, self._py],
            [0, 0, 0, 0, self._vx],
            [0, 0, 0, 0, self._vy],
            [0, 0, 0, 0, self._ax],
            [0, 0, 0, 0, self._ay],
        ])
        
        self._R = sym.zeros(6)
       
    ## Constructor Class
    def __init__(self, s):
        # Instantiating constructor for inherited class.
        super(Landmark, self).__init__(s, "Landmarks")
        
        # Creating characteristic variables for landmarks and reading.
        self._parameters.update({
            "linear_acceleration": True,
            "precision": 0.6,
        })
        
        self._parameters = self._conf.readVariables(self._parameters)
        
        self.reset( )
        
    ## update
    # .
    def update(self, data):
        self._predictedstate["x"][2:, 0] = -self._speeds[data["movement"]]["x_speed"][:len(self._speeds[data["movement"]]["x_speed"])-1, 0]
        self._predictedstate["covariance"] = self._speeds[data["movement"]]["R"]
        
        super(Landmark, self).update(data)
        
        if self._predictedstate["covariance"][0, 0] < self._parameters['precision'] and self._predictedstate["covariance"][1, 1] < self._parameters['precision']:
            self._bkb.write_float("VISUAL_MEMORY_LAND_X", self._predictedstate["x"][0,0])
            self._bkb.write_float("VISUAL_MEMORY_LAND_Y", self._predictedstate["x"][1,0])
            self._bkb.write_float("VISUAL_MEMORY_LAND_LOC", 1)
        else:        
            self._bkb.write_float("VISUAL_MEMORY_LAND_LOC", 0)
        
        return [data["movement"], self._predictedstate["x"], self._predictedstate["covariance"]]
    
    ## end
    # .
    def end(self):
        self._end( )