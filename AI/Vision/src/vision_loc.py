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
        self.limit = (self.Pan-307, self.Pan, self.Pan+307) # Limits the head turning to only 90 degrees

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
        self.pos = self.Pan # holds the position which the frame was generated
        self.pandirection = 0 # Changing step for pan.

        self.Main()

    #----------------------------------------------------------------------------------------------
    #   Method used to initialize frame capture
    #----------------------------------------------------------------------------------------------
    def InitCap(self):
        self.cap = cv2.VideoCapture(1) # Try opening any different device, other than the main
        if not self.cap.isOpened(): # if there is only one device
            self.cap = cv2.VideoCapture(0) # opens the main device
            if not self.cap.isOpened():
                print "ERROR LOADING CAMERA:\nDEVICE NOT FOUND!"
                exit()

    #----------------------------------------------------------------------------------------------
    #   Method which will capture a image from the camera
    #----------------------------------------------------------------------------------------------
    def Capture(self):
        try:
            _, self.img = self.cap.read()  # Get image from camera
            imgblur = cv2.medianBlur(self.img, self.blur) # Blurs image
            self.hsv = cv2.cvtColor(imgblur, cv2.COLOR_BGR2HSV) # Convert to HSV
            self.pos = self.limit[1] # Saves pan position
        except:
            print "ERROR ON FRAME CAPTURE!"

    #----------------------------------------------------------------------------------------------
    #   Method which changes head's position
    #----------------------------------------------------------------------------------------------
    def PanHead(self):
        if self.Pan < self.limit[0] and self.pandirection < 0:
            self.pandirection *= -1
        elif self.Pan > self.limit[2] and self.pandirection > 0:
            self.pandirection *= -1
        self.Pan += self.pandirection
        self.servo.writeWord(19, 30, int(self.Pan))

    #----------------------------------------------------------------------------------------------
    #   Method which converts a relative position on pixels into degrees
    #----------------------------------------------------------------------------------------------
    def IsIn(self, value):
        x = value - len(self.img[0])/2
        y = (0.1 * x * 640)/(65 * len(self.img[0]))
        return degrees(atan(y)) 

    #----------------------------------------------------------------------------------------------
    #   Method which returns the head's angle
    #----------------------------------------------------------------------------------------------
    def GetAng(self):
        return (self.limit[1]-self.Pan)*300/1024.0

    #----------------------------------------------------------------------------------------------
    #   Main method
    #----------------------------------------------------------------------------------------------
    def Main(self):
        if self.args.show:
            cv2.namedWindow('ROBOT VISION')
        
        self.InitCap()
        
        self.pandirection = 7

        thrs = [self.Blue, self.Red, self.Yellow, self.Purple]
        c = [(255,255,100), (100,100,255), (100,255,255), (200,100,200)]

        while True:
            ret = [-999, -999, -999, -999]
            
            self.Capture()

            for i in range(4):
                try:
                    mask = cv2.inRange(self.hsv, thrs[i][0:3], thrs[i][3:6])
                    kern = np.ones((self.krnl, self.krnl), np.uint8)
                    erod = cv2.erode(mask, kern, iterations=self.ersn)
                    dila = cv2.dilate(erod, kern, iterations=self.dltn)
                    cnt,_ = cv2.findContours(dila, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    areas = [cv2.contourArea(aux) for aux in cnt]
                    max_index = np.argmax(areas)
                    cnt = cnt[max_index]
                    x,y,w,h = cv2.boundingRect(cnt)
                    M = cv2.moments(cnt)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    
                    if cnt != None:
                        ret[i] = -self.IsIn(cx)-self.GetAng()

                    if self.args.show:
                        cv2.rectangle(self.img, (x,y), (x+w,y+h), c[i], 2)
                        cv2.circle(self.img, (cx, cy), 5, c[i], -1)
                except:
                    pass
                    
            self.bkb.write_float(self.Mem,'VISION_BLUE_LANDMARK_DEG', ret[0]) 
            self.bkb.write_float(self.Mem,'VISION_RED_LANDMARK_DEG', ret[1])
            self.bkb.write_float(self.Mem,'VISION_YELLOW_LANDMARK_DEG', ret[2])
            self.bkb.write_float(self.Mem,'VISION_PURPLE_LANDMARK_DEG', ret[3])
            
            print ret
            
            if self.args.show:
                cv2.line(self.img, (len(self.img[0])/2,0), (len(self.img[0])/2,len(self.img)),(0,255,0))
                cv2.imshow('ROBOT VISION', self.img)

            self.PanHead()

            k = cv2.waitKey(15) & 0xFF
            if k == 27:
                break

        cv2.destroyAllWindows()

LocalizationVision()
