# coding: utf-8

# ****************************************************************************
# * @file: Landmark.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class Landmark
# ****************************************************************************

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
    def __init__(self, a, s):
        # Instantiating constructor for inherited class.
        super(Landmark, self).__init__(a, s, "Landmarks")
        
        # Creating characteristic variables for landmarks and reading.
        self._parameters.update({
            "linear_acceleration": True,
            "precision": 2,
        })
        
        self._parameters = self._conf.readVariables(self._parameters)
        
        self.reset( )
        
    ## update
    # .
    def update(self, data):
        self._predictedstate["x"][2:, 0] = -self._speeds[data["movement"]]["x_speed"][:len(self._speeds[data["movement"]]["x_speed"])-1, 0]
        self._predictedstate["covariance"] = self._speeds[data["movement"]]["R"]
        
        super(Landmark, self)._update(data)
        
        # Updating to current instant in time
        if self._predictedstate["time"] != time.time( ):
            _predict(tnow = None, movements = 1)
        else:
            if self._args.savedata == True:
                try:
                    a = np.load("./Data/Land.npy")
                    a = np.concatenate((a,
                        [[
                            self._state["time"],
                            [float(i) for i in self._state["x"][:,0]],
                            [self._state["covariance"][i,i] for i in xrange(self._state["covariance"].shape[0])],
                            [float(i) for i in self._state["covariance"][:,0]],
                        ]]),
                        axis=0
                    )
                except IOError:
                    a = [[
                        self._state["time"],
                        [float(i) for i in self._state["x"][:,0]],
                        [self._state["covariance"][i,i] for i in xrange(self._state["covariance"].shape[0])],
                        [float(i) for i in self._state["covariance"][:,0]],
                    ]]
                np.save("./Data/Land", a)
    
            if self._predictedstate["covariance"][0, 0] < self._parameters['vision_error']*self._parameters['precision'] and self._predictedstate["covariance"][1, 1] < self._parameters['precision']:
                self._bkb.write_float("VISUAL_MEMORY_LAND_X", self._predictedstate["x"][0,0])
                self._bkb.write_float("VISUAL_MEMORY_LAND_Y", self._predictedstate["x"][1,0])
                self._bkb.write_float("VISUAL_MEMORY_LAND_LOC", 1)
            else:        
                self._bkb.write_float("VISUAL_MEMORY_LAND_LOC", 0)
        
        return [data["movement"], self._predictedstate["x"], self._predictedstate["covariance"]]
    
    ## predict
    # .
    def predict(self, tnow = None, movements = None):
        self._predictedstate["x"][2:, 0] = -self._speeds[movements]["x_speed"][:len(self._speeds[movements]["x_speed"])-1, 0]
        self._predictedstate["covariance"] = self._speeds[movements]["R"]
        
        super(Landmark, self)._predict(tnow, movements)
        
        if self._args.savedata == True:
            try:
                a = np.load("./Data/Land.npy")
                a = np.concatenate((a,
                    [[
                        self._state["time"],
                        [float(i) for i in self._state["x"][:,0]],
                        [self._state["covariance"][i,i] for i in xrange(self._state["covariance"].shape[0])],
                        [float(i) for i in self._state["covariance"][:,0]],
                    ]]),
                    axis=0
                )
            except IOError:
                a = [[
                    self._state["time"],
                    [float(i) for i in self._state["x"][:,0]],
                    [self._state["covariance"][i,i] for i in xrange(self._state["covariance"].shape[0])],
                    [float(i) for i in self._state["covariance"][:,0]],
                ]]
            np.save("./Data/Land", a)
    
        if self._predictedstate["covariance"][0, 0] < self._parameters['vision_error']*self._parameters['precision'] and self._predictedstate["covariance"][1, 1] < self._parameters['precision']:
            self._bkb.write_float("VISUAL_MEMORY_LAND_X", self._predictedstate["x"][0,0])
            self._bkb.write_float("VISUAL_MEMORY_LAND_Y", self._predictedstate["x"][1,0])
            self._bkb.write_float("VISUAL_MEMORY_LAND_LOC", 1)
        else:        
            self._bkb.write_float("VISUAL_MEMORY_LAND_LOC", 0)
    
    ## end
    # .
    def end(self):
        self._end( )