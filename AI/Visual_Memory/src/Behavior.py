# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import os
import signal # Class used for external interrupt detection.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from Basic import * # Standard and abstract class.
from Robots import * # Class responsible for performing robots tracking.
from Landmark import * # Class responsible for performing landmarks tracking.

## Class Behavior
# Class responsible for managing the behavior of Visual Memory.
class Behavior(Basic):
    
    # ---- Variables ----
    
    ## __posrobot
    # Variable used to instantiate class responsible for robot speed.
    __posrobot = None
    
    ## parameters
    # Variable used to instantiate class responsible for robot speed.
    parameters = None
    
    def signal_term_handler(self, signal, frame):
        raise VisualMemoryException(3, '')
    
    def killedProcess(self):
        signal.signal(signal.SIGTERM, self.signal_term_handler)
    
    ## Constructor Class
    def __init__(self):
        self.killedProcess( )
        super(Behavior, self).__init__("Settings", "Visual Memory")
        
        # Creating default values and reading values
        self.parameters = {
            "number_robots": 8,
            "execution_period_ms": 100,
            "weight_robot": 0.6,
        }
        self.parameters = self._conf.readVariables(self.parameters)
        
        if self.parameters["number_robots"] < 0 or self.parameters["number_robots"] > 22:
            raise VisualMemoryException(1, self.parameters["number_robots"])
        
        # Creating objects to be tracking
        self.me = Speeds( )
        self.land = Landmark(self.me)
        
        # Support Variables
        self.robots = []
        self.__newrobots = []
        self.__posrobot = [0, 0]
        
        for i in xrange(self.parameters["number_robots"]-1):
            self.__newrobots.append(Robots(self.me, self.__posrobot))
        
    ## readDataLandmarks
    # Responsible for reading the data coming from the vision system.
    def readDataLandmarks(self, old):
        if self._bkb.read_float("VISION_LAND_TAG") == 1:
            data = [{
                    "tag": 1,
                    "pos": [self._bkb.read_float("VISION_LAND_X"), self._bkb.read_float("VISION_LAND_Y")],
                    "time": self._bkb.read_float("VISION_LAND_TIME"),
                    "movement": int(self._bkb.read_float("VISION_LAND_MOV")),
                }]
            
            self._bkb.write_float("VISION_LAND_TAG", 0)
            return old + data
        else:
            return old
    
    ## readDataRobots
    # .
    def readDataRobots(self, old):
        data = []
        for number in xrange(1, self.parameters["number_robots"]):
            if self._bkb.read_float("VISION_RB" + str(number).zfill(2) + "_TAG") == 0:
                continue
            
            data.append({
                "tag": self._bkb.read_float("VISION_RB" + str(number).zfill(2) + "_TAG") - 2,
                "pos": [self._bkb.read_float("VISION_RB" + str(number).zfill(2) + "_X"), self._bkb.read_float("VISION_RB" + str(number).zfill(2) + "_Y")],
                "time": self._bkb.read_float("VISION_RB" + str(number).zfill(2) + "_TIME"),
                "movement": int(self._bkb.read_float("VISION_RB" + str(number).zfill(2) + "_MOV")),
            })
            
            self._bkb.write_float("VISION_RB" + str(number).zfill(2) + "_TAG", 0)
        
        data = sorted(old + data, key= lambda k: k["time"])
        
        return data
    
    ## distributeDataRobots
    # .
    def distributeDataRobots(self, datarobots):
        if datarobots == []:
            return
        
        index = 0
        time = -1
        while index < len(datarobots):
            data = datarobots[index]
            
            # First input data
            if self.robots == []:
                candidates = self.__newrobots.pop(0)
                candidates.updateThread(data)
                self.robots.append(candidates)
                datarobots.pop(index)
                continue
                
            if data["time"] != time:
                opponent = [ robot for robot in self.robots if robot.timenumber == -1 ]
                indefinite = [ robot for robot in self.robots if robot.timenumber == 0 ]
                teammate = [ robot for robot in self.robots if robot.timenumber == 1 ]
                time = data["time"]
    
            # Calculates the similarity of the data with the objects
            #  Saving position
            self.__posrobot[0], self.__posrobot[1] = data["pos"]
            
            #  Generating Candidates
            if data["tag"] == -1:
                candidates = opponent + indefinite
            elif data["tag"] == 1:
                candidates = indefinite + teammate
            else:
                candidates = opponent + indefinite + teammate
            
            #  Calculates the similarity
            candidates.sort()
            
            #  Sends the data to the most similar object and run object update
            if (candidates == [] or candidates[0].weight > self.parameters["weight_robot"]) and self.__newrobots != []:
                candidates = self.__newrobots.pop(0)
                candidates.updateThread(data)
                self.robots.append(candidates)
                datarobots.pop(index)
                index -= 1
            else:
                if candidates[0].timenumber == -1:
                    opponent.remove(candidates[0])
                    candidates[0].updateThread(data)
                    datarobots.pop(index)
                    index -= 1
                elif candidates[0].timenumber == 1:
                    teammate.remove(candidates[0])
                    candidates[0].updateThread(data)
                    datarobots.pop(index)
                    index -= 1
                else:
                    indefinite.remove(candidates[0])
                    candidates[0].updateThread(data)
                    datarobots.pop(index)
                    index -= 1
            
            index += 1
    
    ## readDataBall
    # Responsible for reading the data coming from the vision system.
    def readDataBall(self):
        if self._bkb.read_float("VISION_BALL_TAG") == 1:
            data = [{
                    "tag": 1,
                    "pos": [self._bkb.read_float("VISION_BALL_X"), self._bkb.read_float("VISION_BALL_Y")],
                    "time": self._bkb.read_float("VISION_BALL_TIME"),
                    "movement": self._bkb.read_float("VISION_BALL_MOV"),
                }]
            
            self._bkb.write_float("VISION_BALL_TAG", 0)
            return old + data
        else:
            return old
    
    ## run
    # .
    def run(self):
        # Initiating variables
        datalandmarks = []
        datarobots = []
        databall = []
        
        while True:
            try:
                # Start counting time
                start = time.time()
            
                # Reading data from landmarks
                datalandmarks = self.readDataLandmarks(datalandmarks)
            
                if datalandmarks != []:
                    # Predict robot speed (me)
                    self.me.update(self.land.update(datalandmarks.pop(0)))
                else:
                    # Predicts only the new landmarks position
                    self.land.predict(movements = 1)
            
                # Reading robots data
                datarobots = self.readDataRobots(datarobots)
            
                # Distribute the data to the robot objects
                self.distributeDataRobots(datarobots)
            
                ## Reading ball data
                # databall = readDataBall(databall)
            
                ## Distribute the data to the ball objects
                # Batata
            
                ## Doing cleaning and objects (lost objects)
                # Batata
            
                ## Predicts objects (Now)
                # Batata
            
                ## Send object for vision screening
                # Batata
            
                # Wait an instant on the remaining time
                delta = self.parameters["execution_period_ms"]*1e-3 - time.time() + start
                if delta > 0:
                    time.sleep(delta)
            except KeyboardInterrupt:
                os.system('clear') # Cleaning terminal
                print "Keyboard interrupt detected"
                break
            except VisualMemoryException as e:
                break
    
    ## end
    # .
    def end(self):
        self._end( )
        kill = self.robots + self.__newrobots
        
        for robot in kill:
            robot.end( )
        
        self.land.end( )