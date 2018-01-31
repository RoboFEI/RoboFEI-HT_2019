# coding: utf-8

# ****************************************************************************
# * @file: Behavior.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class Behavior
# ****************************************************************************

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the visual memory system.
import os # Class used for communication with the system
import signal # Class used for external interrupt detection.
from math import log10, floor # Functions used for rounding UI

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
    def __init__(self, a):
        self.killedProcess( ) # Function to monitor external process kill.
        self.args = a # Input arguments.
        
        super(Behavior, self).__init__(a, "Settings", "Visual Memory")
        
        # Creating default values and reading values
        self.parameters = {
            "number_robots": 8,
            "execution_period_ms": 100,
            "weight_robot": 0.0006,
        }
        self.parameters = self._conf.readVariables(self.parameters)
        
        if self.args.numberrobots != None:
            self.parameters["number_robots"] = self.args.numberrobots
        
        if self.args.executionperiod != None:
            self.parameters["execution_period_ms"] = self.args.executionperiod
        
        if self.parameters["number_robots"] < 0 or self.parameters["number_robots"] > 22:
            raise VisualMemoryException(1, self.parameters["number_robots"])
        
        # Creating objects to be tracking
        self.me = Speeds( )
        self.land = Landmark(self.args, self.me)
        
        # Support Variables
        self.robots = []
        self.__newrobots = []
        self.__posrobot = [0, 0, 0]
        
        for i in xrange(-self.parameters["number_robots"]/2, self.parameters["number_robots"]/2):
            if i == 0:
                continue
            self.__newrobots.append(Robots(self.args, self.me, self.__posrobot, i))
        a = self.__newrobots.pop()
        print "Finalizando"
        a.end()
        print "Finalizado"
        
    ## readDataLandmarks
    # Responsible for reading the data coming from the vision system.
    def readDataLandmarks(self, old):
        if self._bkb.read_int("VISION_LAND_TAG") == 1:
            data = [{
                    "tag": 1,
                    "pos": [self._bkb.read_float("VISION_LAND_X"), self._bkb.read_float("VISION_LAND_Y")],
                    "time": self._bkb.read_double("VISION_LAND_TIME"),
                    "movement": self._bkb.read_int("VISION_LAND_MOV"),
                }]
            
            self._bkb.write_int("VISION_LAND_TAG", 0)
            return old + data
        else:
            return old
    
    ## readDataRobots
    # .
    def readDataRobots(self, old):
        data = []
        for number in xrange(1, 22):
            if self._bkb.read_int("VISION_RB" + str(number).zfill(2) + "_TAG") == 0:
                continue
            
            data.append({
                "tag": self._bkb.read_int("VISION_RB" + str(number).zfill(2) + "_TAG") - 2,
                "pos": [self._bkb.read_float("VISION_RB" + str(number).zfill(2) + "_X")*100, self._bkb.read_float("VISION_RB" + str(number).zfill(2) + "_Y")*100],
                "time": self._bkb.read_double("VISION_RB" + str(number).zfill(2) + "_TIME"),
                "movement": int(self._bkb.read_int("VISION_RB" + str(number).zfill(2) + "_MOV")),
            })
            
            self._bkb.write_int("VISION_RB" + str(number).zfill(2) + "_TAG", 0)
        
        data = sorted(old + data, key= lambda k: k["time"])
        
        return data
    
    ### Teste readDataRobots
    
    ## distributeDataRobots
    # .
    def distributeDataRobots(self, datarobots):
        if datarobots == [] or self.__newrobots + self.robots == []:
            return
        
        index = 0
        timenow = -1
        while index < len(datarobots):
            data = datarobots[index]
            
            # New instant in time.
            if data["time"] != timenow:
                opponent = [ robot for robot in self.robots if robot.timenumber < 0 ]
                indefinite = [ robot for robot in self.robots if robot.timenumber == 0 ]
                teammate = [ robot for robot in self.robots if robot.timenumber > 1 ]
                timenow = data["time"]
            
            # First input data
            if self.robots == []:
                candidates = self.__newrobots.pop(0)
                candidates.timenumber = data["tag"]*(len([ robot for robot in self.robots if robot.timenumber*data["tag"] > 0 ]) + 1)
                candidates.updateThread(data)
                self.robots.append(candidates)
                datarobots.pop(index)
                continue
            
            # Calculates the similarity of the data with the objects
            #  Saving position
            self.__posrobot[0], self.__posrobot[1], self.__posrobot[2] = data["pos"] + [data["time"]]
            
            #  Generating Candidates
            if data["tag"] == -1:
                candidates = opponent + indefinite
            elif data["tag"] == 1:
                candidates = indefinite + teammate
            else:
                candidates = opponent + indefinite + teammate
            
            for cad in candidates:
                while not cad._threadPaused():
                    time.sleep(0.033333)
            
            #  Calculates the similarity
            if len(candidates) == 1:
                candidates[0].calculatesDistance()
            else:
                candidates.sort(reverse=True)
            
            # Sends the data to the most similar object and run object update
            if self.__newrobots != [] and (candidates == [] or candidates[0].weight < self.parameters["weight_robot"]):
                candidates = self.__newrobots.pop(0)
                candidates.timenumber = data["tag"]*(len([ robot for robot in self.robots if robot.timenumber*data["tag"] > 0 ]) + 1)
                candidates.updateThread(data)
                self.robots.append(candidates)
                datarobots.pop(index)
                index -= 1
            else:
                if candidates != [] and candidates[0].timenumber < 0:
                    opponent.remove(candidates[0])
                    candidates[0].updateThread(data)
                    datarobots.pop(index)
                    index -= 1
                elif candidates != [] and candidates[0].timenumber > 0:
                    teammate.remove(candidates[0])
                    candidates[0].updateThread(data)
                    datarobots.pop(index)
                    index -= 1
                elif candidates != []:
                    indefinite.remove(candidates[0])
                    candidates[0].timenumber = data["tag"]*(len([ robot for robot in self.robots if robot.timenumber*data["tag"] > 0 ]) + 1)
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
    
    ## printPreviousLine
    # .
    def printPreviousLine(self, text, lines=1, back=True):
        for i in xrange(lines):
            print "\033[F\r",
        print text
    
        if back:
            for i in xrange(lines - 1):
                print ""
    
    ## roundUI
    # .
    def roundUI(self, x, digits = 4):
        try:
            return round(x, (digits - 1)-int(floor(log10(abs(x)))))
        except ValueError:
            return 0
    
    ## updatingScreen
    # .
    def updatingScreen(self):
        # Update landmark
        if self._bkb.read_float("VISUAL_MEMORY_LAND_LOC") == 0:
            text = "+---+ Landmark +     Não    +--------------+           00000          +      "
        else:
            text = "+---+ Landmark +     Sim    +--------------+           00000          +      "
        
        texts = [
            "| x |          |            |     "+ str(self.roundUI(self._bkb.read_float("VISUAL_MEMORY_LAND_X"))).zfill(5) +"    |                          |      ",
            text,
            "| y |          |            |     "+ str(self.roundUI(self._bkb.read_float("VISUAL_MEMORY_LAND_Y"))).zfill(5) +"    |                          |      ",
        ]
        if self.parameters["number_robots"] > 1:
            for i, text in zip(range(4 + (self.parameters["number_robots"] - 1)*4, 4 + (self.parameters["number_robots"] - 1)*4 - 3, -1), texts):
                self.printPreviousLine(text, lines=i)
        else:
            for i, text in zip(range(4, 1, -1), texts):
                self.printPreviousLine(text, lines=i)
        
        # Update robots
        for robot in xrange(1, self.parameters["number_robots"]):
            # Update friend robots
            if robot <= (self.parameters["number_robots"] - 1)/2:
                if self._bkb.read_float("VISUAL_MEMORY_AL_"+ str(robot).zfill(2) +"_LOC") == 0:
                    text = "+---+  Aliado  +     Não    +--------------+           "+ str(self.roundUI(self._bkb.read_float("VISUAL_MEMORY_AL_"+ str(robot).zfill(2) +"_MAX_VEL"))).zfill(5) +"          +      "
                else:
                    text = "+---+  Aliado  +     Sim    +--------------+           "+ str(self.roundUI(self._bkb.read_float("VISUAL_MEMORY_AL_"+ str(robot).zfill(2) +"_MAX_VEL"))).zfill(5) +"          +      "
    
                texts = [
                    "| x |          |            |     "+ str(self.roundUI(self._bkb.read_float("VISUAL_MEMORY_AL_"+ str(robot).zfill(2) +"_X"))).zfill(5) +"    |                          |      ",
                    text,
                    "| y |          |            |     "+ str(self.roundUI(self._bkb.read_float("VISUAL_MEMORY_AL_"+ str(robot).zfill(2) +"_Y"))).zfill(5) +"    |                          |      ",
                ]
            else:
                if self._bkb.read_float("VISUAL_MEMORY_OP_"+ str(robot - (self.parameters["number_robots"] - 1)/2).zfill(2) +"_LOC") == 0:
                    text = "+---+ Oponente +     Não    +--------------+           "+ str(self.roundUI(self._bkb.read_float("VISUAL_MEMORY_OP_"+ str(robot - (self.parameters["number_robots"] - 1)/2).zfill(2) +"_MAX_VEL"))).zfill(5) +"          +      "
                else:
                    text = "+---+ Oponente +     Sim    +--------------+           "+ str(self.roundUI(self._bkb.read_float("VISUAL_MEMORY_OP_"+ str(robot - (self.parameters["number_robots"] - 1)/2).zfill(2) +"_MAX_VEL"))).zfill(5) +"          +      "
    
                texts = [
                    "| x |          |            |     "+ str(self.roundUI(self._bkb.read_float("VISUAL_MEMORY_OP_"+ str(robot - (self.parameters["number_robots"] - 1)/2).zfill(2) +"_X"))).zfill(5) +"    |                          |      ",
                    text,
                    "| y |          |            |     "+ str(self.roundUI(self._bkb.read_float("VISUAL_MEMORY_OP_"+ str(robot - (self.parameters["number_robots"] - 1)/2).zfill(2) +"_Y"))).zfill(5) +"    |                          |      ",
                ]
            
            for i, text in zip(range((self.parameters["number_robots"] - robot)*4, (self.parameters["number_robots"] - robot)*4 - 3, -1), texts):
                self.printPreviousLine(text, lines=i)
    
    ## run
    def run(self):
        # Initiating variables
        datalandmarks = []
        datarobots = []
        databall = []
    
        if self.args.debug:
            print "\nPeríodo de execução:", self.parameters["execution_period_ms"], "\tPeso mínimo:", self.parameters["weight_robot"]*100, "%", "\tTempo:", time.strftime("%H:%M:%S", time.localtime(time.time( )))
            print "    +----------+------------+--------------+--------------------------+      "
            print "    |   Nome   | Localizado | Posição (cm) | Velocidade máxima (cm/s) |      "
            print "+---+----------+------------+--------------+--------------------------+      "
            print "| x |          |            |     00000    |                          |      "
            print "+---+ Landmark +     Não    +--------------+           00000          +      "
            print "| y |          |            |     00000    |                          |      "
            print "+---+----------+------------+--------------+--------------------------+      "
    
            for i in xrange((self.parameters["number_robots"] - 1)/2):
                print "| x |          |            |     00000    |                          |      "
                print "+---+  Aliado  +     Não    +--------------+           00000          +      "
                print "| y |          |            |     00000    |                          |      "
                print "+---+----------+------------+--------------+--------------------------+      "
            for i in xrange((self.parameters["number_robots"] - 1)/2, (self.parameters["number_robots"] - 1)):
                print "| x |          |            |     00000    |                          |      "
                print "+---+ Oponente +     Não    +--------------+           00000          +      "
                print "| y |          |            |     00000    |                          |      "
                print "+---+----------+------------+--------------+--------------------------+      "
    
        while True:
            try:
                # Start counting time
                start = time.time()
        
                # Analyzing landmarks ------------------------------------------------------------
                
        #         # Reading data from landmarks
        #         datalandmarks = readDataLandmarks(datalandmarks)
        ##         print "datalandmarks:", datalandmarks
        
        #         if datalandmarks != []:
        #             # Predict new landmarks position and robot speed (me)
        #             me.update(land.update(datalandmarks.pop(0)))
        #         else:
        #             # Predicts only the new landmarks position
        #             land.predict(movements = 0)
                    
                # Analyzing robots ------------------------------------------------------------
        
                # Reading robots data
                datarobots = self.readDataRobots(datarobots)
        #         print "datarobots:", datarobots
                
                # Distribute the data to the robot objects
                self.distributeDataRobots(datarobots)
                
                ## Reading ball data
                # databall = readDataBall(databall)
        
                ## Distribute the data to the ball objects
                # Batata
        
                ## Doing cleaning and objects (lost objects)
                i = 0
                while i < len(self.robots):
                    if self.robots[i].testReset( ):
                        self.__newrobots.append(self.robots.pop(i))
                        continue
                    i += 1
                        
                ## Predicts objects (Now)
                for robot in self.robots:
                    robot.predictThread(movements=0)
        
                ## Send object for vision screening
                # Batata
        
                # Displaying debug values
                if self.args.debug:        
                    self.printPreviousLine(
                        "Período de execução: " + str(self.parameters["execution_period_ms"]) + "\tPeso mínimo: " + str(self.parameters["weight_robot"]*100) + "%\tTempo: " + time.strftime("%H:%M:%S", time.localtime(time.time( ))),
                        lines=8+4*(self.parameters["number_robots"]-1)
                    )            
                    self.updatingScreen( )
        
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