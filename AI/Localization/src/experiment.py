__author__ = "RoboFEI-HT"
__authors__ = "Aislan C. Almeida"
__license__ = "GNU General Public License v3.0"

from Viewer import * # Imports the environment of the viewer
# from AMCL import * # Imports the Particle Filter Class
import time 

# To pass arguments to the function
import argparse
# Import a shared memory
import sys
sys.path.append('../../Blackboard/src/')
from SharedMemory import SharedMemory

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

#--------------------------------------------------------------------------------------------------
#   Class implementing the Core of the Localization Process
#--------------------------------------------------------------------------------------------------
class MINDREADER():
    def __init__(self):
        self.bkb = SharedMemory() # Instance of a blackboard
        config = ConfigParser()   # Configuration file

        try:
            config.read('../../Control/Data/config.ini') # Reads the config archive
            mem_key = int(config.get('Communication', 'no_player_robofei'))*100 # Get the memory key
        except:
            print "#----------------------------------#"
            print "#   Error loading config parser.   #"
            print "#----------------------------------#"
            sys.exit()

        self.Mem = self.bkb.shd_constructor(mem_key) # Create the link to the blackboard

    def main(self):
        while True:
            # print "CONTROL_ACTION", self.bkb.read_int(self.Mem, 'CONTROL_ACTION')
            # print "VISION_FIRST_GOALPOST", self.bkb.read_float(self.Mem, 'VISION_FIRST_GOALPOST')
            # print "VISION_SECOND_GOALPOST", self.bkb.read_float(self.Mem, 'VISION_SECOND_GOALPOST')
            # print "VISION_THIRD_GOALPOST", self.bkb.read_float(self.Mem, 'VISION_THIRD_GOALPOST')
            # print "VISION_FOURTH_GOALPOST", self.bkb.read_float(self.Mem, 'VISION_FOURTH_GOALPOST')
            # print "VISION_FIELD", self.bkb.read_int(self.Mem, 'VISION_FIELD')
            # print "IMU_EULER_Z", self.bkb.read_float(self.Mem, 'IMU_EULER_Z')
            # print "DECISION_LOCALIZATION", self.bkb.read_int(self.Mem, 'DECISION_LOCALIZATION')
            # print 'VISION_PAN_DEG', self.bkb.read_float(self.Mem, 'VISION_PAN_DEG')
            # x = self.bkb.read_int(self.Mem, 'VISION_FIELD')
            # v = read(x)

            # print v
            # print "First position"
            # try:
            #     self.second()
            # except:
            #     print "Interrupted"
            try:
                index = 0
                # MCL
                print 'Simple MCL'
                for i in xrange(30):
                    index += 1
                    print "\tExperiment number", index
                    self.first()
                    self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                    time.sleep(1)
                
                for i in xrange(30):
                    index += 1
                    print "\tExperiment number", index
                    self.second()
                    self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                    time.sleep(1)

                # # MCL with variable quantity of particles
                # print 'Changing quantity of particles'
                # for i in xrange(30):
                #     index += 1
                #     print "\tExperiment number", index
                #     self.first()
                #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                #     time.sleep(1)

                # for i in xrange(30):
                #     index += 1
                #     print "\tExperiment number", index
                #     self.second()
                #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                #     time.sleep(1)

                # # MCL with Value of the Perfect Information
                # print 'Using the value of the perfect information'
                # for i in xrange(30):
                #     index += 1
                #     print "\tExperiment number", index
                #     self.first()
                #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                #     time.sleep(1)

                # for i in xrange(30):
                #     index += 1
                #     print "\tExperiment number", index
                #     self.second()
                #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                #     time.sleep(1)

                # # MCL with changing quantity of particles and VPI
                # print 'Changing quantity of particles and VPI'
                # for i in xrange(30):
                #     index += 1
                #     print "\tExperiment number", index
                #     self.first()
                #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                #     time.sleep(1)

                # for i in xrange(30):
                #     index += 1
                #     print "\tExperiment number", index
                #     self.second()
                #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                #     time.sleep(1)

                # # MCL with position resetting
                # print 'Position Resetting'
                # for i in xrange(30):
                #     index += 1
                #     print "\tExperiment number", index
                #     self.first()
                #     self.second()
                #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                #     time.sleep(1)

                # for i in xrange(30):
                #     index += 1
                #     print "\tExperiment number", index
                #     self.second()
                #     self.first()
                #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                #     time.sleep(1)

                # # MCL with position resetting and quantity variation of particles
                # print 'Position resetting and changing quantity of particles'
                # for i in xrange(30):
                #     index += 1
                #     print "\tExperiment number", index
                #     self.first()
                #     self.second()
                #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                #     time.sleep(1)

                # for i in xrange(30):
                #     index += 1
                #     print "\tExperiment number", index
                #     self.second()
                #     self.first()
                #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                #     time.sleep(1)

                # # MCL with position resetting and VPI
                # print 'Position resetting and value of perfect information'
                # for i in xrange(30):
                #     index += 1
                #     print "\tExperiment number", index
                #     self.first()
                #     self.second()
                #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                #     time.sleep(1)

                # for i in xrange(30):
                #     index += 1
                #     print "\tExperiment number", index
                #     self.second()
                #     self.first()
                #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                #     time.sleep(1)

                # # Complete system
                # print 'Complete implementation'
                # for i in xrange(30):
                #     index += 1
                #     print "\tExperiment number", index
                #     self.first()
                #     self.second()
                #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                #     time.sleep(1)

                # for i in xrange(30):
                #     index += 1
                #     print "\tExperiment number", index
                #     self.second()
                #     self.first()
                #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 11011)
                #     time.sleep(1)
            except:
                print "\nOut"
            # print "Second position"
            # self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', 10102)
            # time.sleep(3)
            # print "Save files"
            # self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', 11011)
            # time.sleep(3)
            # print "Finish simulator"
            # self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', 11111)
            # time.sleep(1)
            # print "Finish me"
            # self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', 999)
            self.bkb.write_int(self.Mem, 'VISION_WORKING', 11111)
            self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 11111)
            time.sleep(1)
            self.bkb.write_int(self.Mem, 'VISION_WORKING', 0)
            self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 0)
            self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', 999)
            exit()
    
    def first(self):
        # Starting position
        self.bkb.write_int(self.Mem, 'VISION_WORKING', 10101)
        time.sleep(0.5)
        # Move forward
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 1)
        time.sleep(12)
        # Rotate right
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 3)
        time.sleep(3)
        # Walk forward
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 1)
        time.sleep(6)
        # Rotate right
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 3)
        time.sleep(1.8)
        # Walk forward
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 1)
        time.sleep(25)
        # Rotate left
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 2)
        time.sleep(5)
        # Walk forward
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 1)
        time.sleep(10)
        # Stop
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 0)

    def second(self):
        self.bkb.write_int(self.Mem, 'VISION_WORKING', 10102)
        time.sleep(0.5)
        # Move forward
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 1)
        time.sleep(25)
        # Rotate left
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 2)
        time.sleep(3)
        # Walk forward
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 1)
        time.sleep(10)
        # Gait
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 11)
        time.sleep(2)
        # Walk forward
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 1)
        time.sleep(10)
        # Stop
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 0)

def read(x):
    v = []
    for i in xrange(31, -1, -1):
        aux = x >> i
        x -= aux << i
        v.insert(0, abs(aux))

    return v

#Call the main function, start up the simulation
if __name__ == "__main__":
    MR = MINDREADER()
    MR.main()