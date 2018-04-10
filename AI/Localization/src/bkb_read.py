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
            # self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', -999)
            # self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', -999)
            # print "CONTROL_ACTION", self.bkb.read_int(self.Mem, 'CONTROL_ACTION')
            # print "VISION_FIRST_GOALPOST", self.bkb.read_float(self.Mem, 'VISION_FIRST_GOALPOST')
            # print "VISION_SECOND_GOALPOST", self.bkb.read_float(self.Mem, 'VISION_SECOND_GOALPOST')
            # print "VISION_THIRD_GOALPOST", self.bkb.read_float(self.Mem, 'VISION_THIRD_GOALPOST')
            # print "VISION_FOURTH_GOALPOST", self.bkb.read_float(self.Mem, 'VISION_FOURTH_GOALPOST')
            print "iVISION_FIELD", self.bkb.read_int(self.Mem, 'iVISION_FIELD')
            print "fVISION_FIELD", self.bkb.read_float(self.Mem, 'fVISION_FIELD')
            # print "iVISION_FIELD", self.bkb.read_int(self.Mem, 'iVISION_FIELD')
            # print "fVISION_FIELD", self.bkb.read_float(self.Mem, 'fVISION_FIELD')
            print "IMU_EULER_Z", self.bkb.read_float(self.Mem, 'IMU_EULER_Z')
            print 'VISION_PAN_DEG', self.bkb.read_float(self.Mem, 'VISION_PAN_DEG')
            # x = self.bkb.read_int(self.Mem, 'VISION_FIELD')
            # v = read(x)

            print
            time.sleep(0.5)
            # print v

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
