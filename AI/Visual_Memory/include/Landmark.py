# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from KalmanFilter import * # Class responsible for implementing kalman filter methods.

## Class to Landmark
# Class responsible for performing landmarks tracking.
class Landmark(KalmanFilter):
    
    # ---- Variables ----
    
    ## reset
    # .
    def reset(self):
        super(Landmark, self)._reset( )
        
        self._B = sym.Matrix([
            [0, 0, 0, 0, self._p_x],
            [0, 0, 0, 0, self._p_y],
            [0, 0, 0, 0, self._v_x],
            [0, 0, 0, 0, self._v_y],
            [0, 0, 0, 0, self._a_x],
            [0, 0, 0, 0, self._a_y],
        ])
        
        self._R = sym.zeros(6) 
    
    ## Constructor Class
    def __init__(self, s):
        # Instantiating constructor for inherited class.
        super(Landmark, self).__init__(s, "Landmarks")
        
        # Creating characteristic variables for landmarks and reading.
        self._parameters.update({ })
        self._parameters = self._conf.readVariables(self._parameters)
        
        self.reset( )
        
    ## update
    # .
    def update(self, data):
        super(Landmark, self).update(data)
        
        return [data["movement"], self._state['x'], self._state['covariance']]