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
        try:
            self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 0)
            # # Experiment zero - reference
            # print 'mindcontroller: Experiment zero'
            # for i in xrange(1):
            #     # Sets up the experiment
            #     print '\tSetting up experiment', i
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 100)
            #     # Waits until all processes are ready
            #     while self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING') != 120:
            #         time.sleep(0.1)

            #     print '\x1b[1F\x1b[2K\tRunning experiment', i
            #     # Starts the experiment
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 200)

            #     # State Machine
            #     self.FirstTrack()
            #     # Stop
            #     self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 0)

            #     print '\x1b[1F\x1b[2K\tFinishing experiment', i
            #     # Finishes the experiment
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 300+i)
            #     while self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING') != 500+i:
            #         time.sleep(0.1)

            # # Experiment one - using landmarks
            # print 'Experiment one'
            # for i in xrange(1):
            #     # Sets up the experiment
            #     print '\tSetting up experiment', i
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 101)
            #     # Waits until all processes are ready
            #     while self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING') != 121:
            #         time.sleep(0.1)
                
            #     print '\x1b[1F\x1b[2K\tRunning experiment', i
            #     # Starts the experiment
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 200)

            #     # State Machine
            #     self.FirstTrack()
            #     # Stop
            #     self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 0)

            #     print '\x1b[1F\x1b[2K\tFinishing experiment', i
            #     # Finishes the experiment
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 300+i)
            #     while self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING') != 500+i:
            #         time.sleep(0.1)

            # # Experiment two - using keypoints
            # print 'Experiment two'
            # for i in xrange(19, 30):
            #     # Sets up the experiment
            #     print '\tSetting up experiment', i
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 102)
            #     # Waits until all processes are ready
            #     while self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING') != 122:
            #         time.sleep(0.1)
                
            #     print '\x1b[1F\x1b[2K\tRunning experiment', i
            #     # Starts the experiment
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 200)

            #     # State Machine
            #     self.FirstTrack()
            #     # Stop
            #     self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 0)

            #     print '\x1b[1F\x1b[2K\tFinishing experiment', i
            #     # Finishes the experiment
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 300+i)
            #     while self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING') != 500+i:
            #         time.sleep(0.1)

            # Experiment three - Quantity of particles
            # print 'Experiment three'
            # for i in xrange(1):
            #     # Sets up the experiment
            #     print '\tSetting up experiment', i
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 103)
            #     # Waits until all processes are ready
            #     while self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING') != 123:
            #         time.sleep(0.1)
                
            #     print '\x1b[1F\x1b[2K\tRunning experiment', i
            #     # Starts the experiment
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 200)

            #     # State Machine
            #     self.FirstTrack()
            #     # Stop
            #     self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 0)

            #     print '\x1b[1F\x1b[2K\tFinishing experiment', i
            #     # Finishes the experiment
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 300+i)
            #     while self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING') != 500+i:
            #         time.sleep(0.1)

            # # Experiment four - Value of Perfect Information
            # print 'Experiment four'
            # for i in xrange(1):
            #     # Sets up the experiment
            #     print '\tSetting up experiment', i
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 104)
            #     # Waits until all processes are ready
            #     while self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING') != 124:
            #         time.sleep(0.1)
                
            #     print '\x1b[1F\x1b[2K\tRunning experiment', i
            #     # Starts the experiment
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 200)

            #     # State Machine
            #     self.FirstTrack()
            #     # Stop
            #     self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 0)

            #     print '\x1b[1F\x1b[2K\tFinishing experiment', i
            #     # Finishes the experiment
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 300+i)
            #     while self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING') != 500+i:
            #         time.sleep(0.1)

            # Experiment five - kidnap
            print 'Experiment five'
            for i in xrange(1):
                # Sets up the experiment
                print '\tSetting up experiment', i
                self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 105)
                # Waits until all processes are ready
                while self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING') != 125:
                    time.sleep(0.1)
                
                print '\x1b[1F\x1b[2K\tRunning experiment', i
                # Starts the experiment
                self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 200)

                # State Machine
                self.FirstTrack()
                # Stop
                self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 0)
                # Jump
                self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 600)
                # Wait
                time.sleep(1)
                # State Machine
                self.SecondTrack()
                # Stop
                self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 0)

                print '\x1b[1F\x1b[2K\tFinishing experiment', i
                # Finishes the experiment
                self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 300+i)
                while self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING') != 500+i:
                    time.sleep(0.1)

            # # Experiment six - all
            # print 'Experiment six'
            # for i in xrange(1):
            #     # Sets up the experiment
            #     print '\tSetting up experiment', i
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 106)
            #     # Waits until all processes are ready
            #     while self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING') != 126:
            #         time.sleep(0.1)
                
            #     print '\x1b[1F\x1b[2K\tRunning experiment', i
            #     # Starts the experiment
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 200)

            #     # State Machine
            #     self.FirstTrack()
            #     # Stop
            #     self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 0)
            #     # Jump
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 600)
            #     # Wait
            #     time.sleep(1)
            #     # State Machine
            #     self.SecondTrack()
            #     # Stop
            #     self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 0)

            #     print '\x1b[1F\x1b[2K\tFinishing experiment', i
            #     # Finishes the experiment
            #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 300+i)
            #     while self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING') != 500+i:
            #         time.sleep(0.1)
            
        except:
            print '\n\nLocalization: Force quit!'
            self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 0)
        finally:
            self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 900)
            exit()

    def FirstTrack(self):
        # WalkForward 16 secs
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 1)
        time.sleep(16)

        # Turn Right 10 secs
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 3)
        time.sleep(10)

        # WalkForward 15 secs
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 1)
        time.sleep(15)
        
        # Turn Left 4 secs
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 2)
        time.sleep(4)

        # WalkForward 15 secs
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 1)
        time.sleep(15)

    def SecondTrack(self):
        # Walkforward 25 secs
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 1)
        time.sleep(25)

        # Turnleft 10 secs
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 2)
        time.sleep(10)        

        # Walkforward 25 secs 
        self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 1)
        time.sleep(25)

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
