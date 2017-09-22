# coding: utf-8

# ---- Imports ----

# Libraries to be used.
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
    
    ## posrobot
    # Variable used to instantiate class responsible for robot speed.
    __posrobot = None
    
    ## parameters
    # Variable used to instantiate class responsible for robot speed.
    parameters = None
    
    ## Robots
    # List of robots
    robots = __newrobots = None
    
    ## Constructor Class
    def __init__(self):
        super(Behavior, self).__init__("Settings", "Visual Memory")
        
        # Creating default values and reading values
        self.parameters = {
            "number_robots": 4,
            "execution_period_ms": 100,
            "weight_robot": 10,
        }
        self.parameters = self._conf.readVariables(self.parameters)
        
        # Creating objects to be tracking
        me = Speeds( )
        land = Landmark(me)
        
        self.robots = []
        self.__newrobots = []
        
        for i in xrange(self.parameters["number_robots"]-1):
            self.__newrobots.append(Robots(me, posrobot))
        
    ## readDataLandmarks
    # Responsible for reading the data coming from the vision system.
    def readDataLandmarks(self):
        if self._bkb.read_float("VISION_LAND_TAG") == 1:
            data = [{
                    "tag": 1,
                    "pos": [self._bkb.read_float("VISION_LAND_X"), self._bkb.read_float("VISION_LAND_Y")],
                    "time": self._bkb.read_float("VISION_LAND_TIME"),
                }]
            
            self._bkb.write_float("VISION_LAND_TAG", 0)
            return old + data
        else:
            return old
    
    ## readDataRobots
    # .
    def readDataRobots(self):
        data = []
        for number in xrange(1, self.parameters["number_robots"]):
            if self._bkb.read_float("VISION_RB" + str(number).zfill(2) + "_TAG") == 0:
                continue
            
            data.append({
                "tag": self._bkb.read_float("VISION_RB" + str(number).zfill(2) + "_TAG") - 2,
                "pos": [self._bkb.read_float("VISION_RB" + str(number).zfill(2) + "_X"), self._bkb.read_float("VISION_RB" + str(number).zfill(2) + "_Y")],
                "time": self._bkb.read_float("VISION_RB" + str(number).zfill(2) + "_TIME"),
            })
            
            self._bkb.write_float("VISION_RB" + str(number).zfill(2) + "_TAG", 0)
        
        return old + data
    
    ## distributeDataRobots
    # .
    def distributeDataRobots(self):
        if datarobots == []:
            return
        
        index = 0
        time = -1
        while index < len(datarobots):
            data = datarobots[index]
            
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
            if candidates[0].weight > self.parameters["weight_robot"] and self.__newrobots != []:
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
    
    ## run
    # .
    def run(self):
        # Start counting time
        datalandmarks = []
        datarobots = []
        
        start = time.time()
        
        # Reading data from landmarks
        datalandmarks = self.readDataLandmarks(datalandmarks)
        
        if datalandmarks != []:
            # Predict robot speed (me)
            me.update(land(datalandmarks.pop(0)))
        else:
            # Predicts only the new landmarks position
            land.predict(movements = 1)
        
        # Reading robots data
        datarobots = self.readDataRobots(datarobots)
        
        # Distribute the data to the robot objects
        self.distributeDataRobots(datarobots)
        
        #self-iPython ru