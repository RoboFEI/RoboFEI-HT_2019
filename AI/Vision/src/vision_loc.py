import cv2 
import numpy as np
from math import *
import os
from calibration import *
import argparse
import sys
from servo import Servo

sys.path.append('../../Blackboard/src/') # Creates a link to the Blackboard
from SharedMemory import SharedMemory # Imports Blackboard's class
# Used to get information from the config.ini
try:
    from ConfigParser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

# Get arguments from the program excution
parser = argparse.ArgumentParser(description='Vision for Localization', epilog= 'Vision system adapted to be used for the Localization process.')
parser.add_argument('--calibrate', '-c', action="store_true", help = 'Calibrates the segmentation variables.')
parser.add_argument('--show', '-s', action="store_true", help = 'Shows the image seen by the robot.')

#--------------------------------------------------------------------------------------------------
#   Class implementing the Vision Used on Localization
#--------------------------------------------------------------------------------------------------
class LocalizationVision():
    #----------------------------------------------------------------------------------------------
    #   Class constructor
    #----------------------------------------------------------------------------------------------
    def __init__(self):
        self.args = parser.parse_args() # Holds arguments to be used throughout the program

        self.bkb = SharedMemory() # Creates the blackboard object
        # Reads config.ini to get needed information
        config = ConfigParser() # 
        config.read('../../Control/Data/config.ini')
        mem_key = int(config.get('Communication', 'no_player_robofei'))*100
        self.Mem = self.bkb.shd_constructor(mem_key)
        self.Pan = int(config.get('Offset', 'ID_19'))
        self.Tilt = int(config.get('Offset', 'ID_20'))

        self.servo = Servo(self.Pan, self.Tilt) # Initializes servos
        self.limit = 307 # Limits the head turning to only 90 degrees

        # If calibration is requested it executes calibration
        if self.args.calibrate:
            calib = Calibration()
            calib.Main()
            calib = None

        while True:
            try: # Try to open an existing file
                file = open('.thresholds') # open file to read and write
                data = file.read() # reads file into data
                file.close() # closes file
                data = data.split(' ') # split lines
                data = [int(data[aux]) for aux in range(30)]

                self.Blue = np.array(data[0:6]) # Thresholds for blue color
                self.Red = np.array(data[6:12]) # Thresholds for red color
                self.Yellow = np.array(data[12:18]) # Thresholds for yellow color
                self.Purple = np.array(data[18:24]) # Thresholds for purple color
                
                self.blur = data[24] # How much blur in the image
                self.krnl = data[25] # Chooses the size of the kernel for erosion/dilatation
                self.ersn = data[26] # Chooses the quantity of iterations for erosion
                self.dltn = data[27] # Chooses the quantity of iterations for dilatation
                self.rads = data[28] # Chooses the radius of the color picking tool
                self.thrs = data[29] # Chooses the thresholds to adjust colors
                
                print "\n>>> Thresholds loading successful! <<<\n"
                break
            except:
                print ">>> ERROR LOADING THRESHOLDS! <<<"
                # Forcely executes calibration
                calib = Calibration()
                calib.Main()
                calib = None


