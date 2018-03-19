# coding: utf-8

# ****************************************************************************
# * @file: Orchestrator.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class Orchestrator
# ****************************************************************************

# ---- Imports ----

# The standard libraries used in the vision system.

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from BasicProcesses import * # Standard and abstract class.
from CameraCapture import * # Class responsible for performing the observation of domain.
from DNN import * # Class that implements object detection using a deep neural network (DNN).
from Robots import * # Class responsible for detecting thefts and a time of classification they belong.

## Class Orchestrator
# Class responsible for managing the vision process.
class Orchestrator(BasicProcesses):
    
    # ---- Variables ----
    
    ## camera
    # Object responsible for reading the camera.
    camera = True
    
    ## dnn
    # Object responsible for performing a classification use DNN.
    dnn = None
    
    ## robots
    # Object responsible for robots classification.
    robots = None
    
    ## Constructor Class
    def __init__(self, a):
        super(Orchestrator, self).__init__(a, "Vision", "Parameters")
        
        # Instantiating camera object
        try:
            self.camera = CameraCapture(a)
        except VisionException as e:
            sys.exit(1)
        
        # Instantiating dnn object
        try:
            self.dnn = DNN(a)
        except VisionException as e:
            self.camera.finalize()
            sys.exit(1)
        
        # Instantiating robots object
        try:
            self.robots = Robots(a)
        except VisionException as e:
            self.camera.finalize()
            self.dnn.finalize()
            sys.exit(1)
        
    ## run
    # .
    def run(self):
        while True:
            try:
                observation = self.camera.currentObservation()
                observation['objects'] = self.dnn.detect(observation)
                self.robots.classifyingRobots(observation)
            except VisionException as e:
                break
                    
            except KeyboardInterrupt:
                os.system("clear")
                print "\33[1;31mDetect KeyboardInterrupt\33[0m\n"
                break
    
    ## end
    # .
    def end(self):
        self.camera.finalize()
        self.dnn.finalize()
        self.robots.finalize()
        #self._end( )
