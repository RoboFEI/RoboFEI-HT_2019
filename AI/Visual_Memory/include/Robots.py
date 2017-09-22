# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append("../include")
sys.path.append("../src")

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from BasicThread import * # Responsible for implementing the methods and variables responsible for managing the thread.

## Class to Robots
# Class responsible for performing robots tracking.
class Robots(BasicThread):
    
    # ---- Variables ----
    
    ## __listfunction
    # .
    __listfunction = None
    
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
        
        self.__listfunction = [ ]
        
    ## __predictVector
    # .
    def __predictVector(self, vector):
        super(Robots, self).self.predict(vector[0], vector[1])
        
        if vector[0] == None and vector[1] == None:
            kalman._bkb()
            
    #self-iPython __predictVecto
    
    ## predictThread
    # .
    def predictThread(self, tnow = None, movements = None):
        self.__listfunction.append([self.__predictVector, [tnow, movements]])
        _resume( )
    
    ## updateVector
    # .
    def __updateVector(self, vector):
        kalman.self.update(vector[0])
    
    ## updateThread
    # .
    def updateThread(self, tnow = None, movements = None):
        self.__listfunction.append([self.__updateVector, [data]])
        _resume( )
    
    ## run
    # .
    def run(self):
        self.__running = True
        while self.__running:
            with self._pausethread:
                while self.__listfunction != []:
                    func, data = self.__listfunction.pop(0)
                    func(data)
            self._pause( )
    
    ## end
    # .
    def end(self):
        self._finalize( )
        super(Robots, self)._end( )