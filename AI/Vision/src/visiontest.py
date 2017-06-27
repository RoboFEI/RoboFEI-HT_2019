import cv2 
import numpy as np
from math import *
import os
from calibration import *
import argparse
import sys
from vision_loc import *

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
class VisionTest():
    #----------------------------------------------------------------------------------------------
    #   Class constructor
    #----------------------------------------------------------------------------------------------
    def __init__(self):
        self.args = parser.parse_args() # Holds arguments to be used throughout the program

        self.bkb = SharedMemory() # Creates the blackboard object
        # Reads config.ini to get needed information
        mem_key = 100
        self.Mem = self.bkb.shd_constructor(mem_key)

        self.vis = LocalizationVision(self.bkb, self.Mem)

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

        self.img = None # holds the captured frame
        self.hsv = None # holds the frame after changing the color segment

        self.Main()

    #----------------------------------------------------------------------------------------------
    #   Method used to initialize frame capture
    #----------------------------------------------------------------------------------------------
    def InitCap(self):
        self.cap = cv2.VideoCapture(0) # Try opening any different device, other than the main
        # if not self.cap.isOpened(): # if there is only one device
        #     self.cap = cv2.VideoCapture(0) # opens the main device
        #     if not self.cap.isOpened():
        #         print "ERROR LOADING CAMERA:\nDEVICE NOT FOUND!"
        #         exit()

    #----------------------------------------------------------------------------------------------
    #   Method which will capture a image from the camera
    #----------------------------------------------------------------------------------------------
    def Capture(self):
        try:
            _, self.img = self.cap.read()  # Get image from camera
            imgblur = cv2.medianBlur(self.img, self.blur) # Blurs image
            self.hsv = cv2.cvtColor(imgblur, cv2.COLOR_BGR2HSV) # Convert to HSV
        except:
            print "ERROR ON FRAME CAPTURE!"

    #----------------------------------------------------------------------------------------------
    #   Main method
    #----------------------------------------------------------------------------------------------
    def Main(self):
        cv2.namedWindow('ROBOT VISION')
        
        self.InitCap()
        
        thrs = self.Blue

        while True:
            self.Capture()

            try:
                mask = cv2.inRange(self.hsv, thrs[0:3], thrs[3:6])
            except:
                pass

            self.vis.Main(mask, np.random.randint(-90, 90))
            
            cv2.imshow('ROBOT VISION', self.img * mask.reshape(mask.shape + (1,)).astype(int))

            k = cv2.waitKey(15) & 0xFF
            if k == 27:
                break

        cv2.destroyAllWindows()

VisionTest()
