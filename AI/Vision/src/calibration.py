import cv2
import numpy as np
from math import *
import os
import time

#--------------------------------------------------------------------------------------------------
#   This class implements the calibration process of the landmarks.
#--------------------------------------------------------------------------------------------------
class Calibration():
    #----------------------------------------------------------------------------------------------
    #   Constructor of the class
    #----------------------------------------------------------------------------------------------
    def __init__(self):
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
        except: # Creates a new one
            self.Blue = np.array([255, 255, 255, 0, 0, 0]) # Initial thresholds vector
            self.Red = np.array([255, 255, 255, 0, 0, 0]) # Initial thresholds vector
            self.Yellow = np.array([255, 255, 255, 0, 0, 0]) # Initial thresholds vector
            self.Purple = np.array([255, 255, 255, 0, 0, 0]) # Initial thresholds vector
            # Like the last one
            self.blur = 1
            self.krnl = 1
            self.ersn = 1
            self.dltn = 1
            self.rads = 5
            self.thrs = 5
            print "\n>>> Threshold creation successful! <<<\n"

        self.img = None # holds the captured frame
        self.hsv = None # holds the frame after changing the color segment
        self.pos = (0, 0) # holds mouse position

        self.color = 'BLUE' # Color being segmented

    #----------------------------------------------------------------------------------------------
    #   Method which will initialize camera
    #----------------------------------------------------------------------------------------------
    def InitCap(self):
        self.cap = cv2.VideoCapture(1) # Try opening any different device, other than the main
        if not self.cap.isOpened(): # if there is only one device
            self.cap = cv2.VideoCapture(0) # opens the main device

    #----------------------------------------------------------------------------------------------
    #   Method that captures the image for the next frame
    #----------------------------------------------------------------------------------------------
    def capture(self):
        try:
            # self.img = cv2.imread('../../../../VsnTst/resize1.jpg') # Get image from archive
            _, self.img = self.cap.read()  # Get image from camera
            imgblur = cv2.medianBlur(self.img, self.blur) # Blurs image
            self.hsv = cv2.cvtColor(imgblur, cv2.COLOR_BGR2HSV) # Convert to HSV
        except:
            print "Error on frame initialization."

    #----------------------------------------------------------------------------------------------
    #   Method that get mouse actions
    #----------------------------------------------------------------------------------------------
    def Segment(self, event, x, y, flags, param):
        # Updates mouse position
        if event == cv2.EVENT_MOUSEMOVE:
            self.pos = (x, y)

        if event == cv2.EVENT_LBUTTONDOWN:
            # Vector of weights
            P = np.array([])
            # Vector with the weighed sum of the HSV values of the point.
            hM = np.array([])
            sM = np.array([])
            vM = np.array([])

            # Iterates through all points around the click to compute their weighs.
            for i in range(2*self.rads):
                for j in range(2*self.rads):
                    try:
                        # Relative x and y positions.
                        ai = x + i - int(self.rads)
                        aj = y + j - int(self.rads)
                        # Computes the weight.
                        aP = exp(-(pow(x-ai,2)+pow(y-aj,2))/18)
                        # Gets the HSV values from the point.
                        aC = self.hsv[aj][ai]
                        # Saves everything on the vectors.
                        P = np.append(P, aP)
                        hM = np.append(hM, aC[0] * aP)
                        sM = np.append(sM, aC[1] * aP)
                        vM = np.append(vM, aC[2] * aP)
                    except:
                        pass

            # Computes the normalizing factor.
            N = np.sum(P)
            # Computes the weighed sum of all HSV values.
            mH = np.sum(hM)
            mS = np.sum(sM)
            mV = np.sum(vM)

            if self.color == 'BLUE':
                self.Blue[0] = int(min(max(mH/N - self.thrs, 0), self.Blue[0]))
                self.Blue[1] = int(min(max(mS/N - self.thrs, 0), self.Blue[1]))
                self.Blue[2] = int(min(max(mV/N - self.thrs, 0), self.Blue[2]))
                self.Blue[3] = int(max(min(mH/N + self.thrs, 255), self.Blue[3]))
                self.Blue[4] = int(max(min(mS/N + self.thrs, 255), self.Blue[4]))
                self.Blue[5] = int(max(min(mV/N + self.thrs, 255), self.Blue[5]))

            if self.color == 'RED':
                self.Red[0] = int(min(max(mH/N - self.thrs, 0), self.Red[0]))
                self.Red[1] = int(min(max(mS/N - self.thrs, 0), self.Red[1]))
                self.Red[2] = int(min(max(mV/N - self.thrs, 0), self.Red[2]))
                self.Red[3] = int(max(min(mH/N + self.thrs, 255), self.Red[3]))
                self.Red[4] = int(max(min(mS/N + self.thrs, 255), self.Red[4]))
                self.Red[5] = int(max(min(mV/N + self.thrs, 255), self.Red[5]))

            if self.color == 'YELLOW':
                self.Yellow[0] = int(min(max(mH/N - self.thrs, 0), self.Yellow[0]))
                self.Yellow[1] = int(min(max(mS/N - self.thrs, 0), self.Yellow[1]))
                self.Yellow[2] = int(min(max(mV/N - self.thrs, 0), self.Yellow[2]))
                self.Yellow[3] = int(max(min(mH/N + self.thrs, 255), self.Yellow[3]))
                self.Yellow[4] = int(max(min(mS/N + self.thrs, 255), self.Yellow[4]))
                self.Yellow[5] = int(max(min(mV/N + self.thrs, 255), self.Yellow[5]))

            if self.color == 'PURPLE':
                self.Purple[0] = int(min(max(mH/N - self.thrs, 0), self.Purple[0]))
                self.Purple[1] = int(min(max(mS/N - self.thrs, 0), self.Purple[1]))
                self.Purple[2] = int(min(max(mV/N - self.thrs, 0), self.Purple[2]))
                self.Purple[3] = int(max(min(mH/N + self.thrs, 255), self.Purple[3]))
                self.Purple[4] = int(max(min(mS/N + self.thrs, 255), self.Purple[4]))
                self.Purple[5] = int(max(min(mV/N + self.thrs, 255), self.Purple[5]))

    #----------------------------------------------------------------------------------------------
    #   Method which resets calibrations
    #----------------------------------------------------------------------------------------------
    def Reset(self):
        if self.color == 'BLUE':
            self.Blue = np.array([255, 255, 255, 0, 0, 0])
        elif self.color == 'RED':
            self.Red = np.array([255, 255, 255, 0, 0, 0])
        elif self.color == 'YELLOW':
            self.Yellow = np.array([255, 255, 255, 0, 0, 0])
        elif self.color == 'PURPLE':
            self.Purple = np.array([255, 255, 255, 0, 0, 0])

    #----------------------------------------------------------------------------------------------
    #   Method used to calibrate colors
    #----------------------------------------------------------------------------------------------
    def Calibration(self):
        self.InitCap()
        flag = None
        # Creates and sets trackbar positions.
        cv2.namedWindow('Trackbars')
        cv2.createTrackbar('Color', 'Trackbars', 0, 3, nothing)
        cv2.createTrackbar('Blur', 'Trackbars', 1, 100, nothing)
        cv2.setTrackbarPos('Blur', 'Trackbars', self.blur)
        cv2.createTrackbar('Kernel', 'Trackbars', 1, 100, nothing)
        cv2.setTrackbarPos('Kernel', 'Trackbars', self.krnl)
        cv2.createTrackbar('Erosion', 'Trackbars', 1, 100, nothing)
        cv2.setTrackbarPos('Erosion', 'Trackbars', self.ersn)
        cv2.createTrackbar('Dilatation', 'Trackbars', 1, 100, nothing)
        cv2.setTrackbarPos('Dilatation', 'Trackbars', self.dltn)
        cv2.createTrackbar('Radius', 'Trackbars', 1, 100, nothing)
        cv2.setTrackbarPos('Radius', 'Trackbars', self.rads)
        cv2.createTrackbar('Threshold', 'Trackbars', 1, 100, nothing)
        cv2.setTrackbarPos('Threshold', 'Trackbars', self.thrs)
        # Creates a window for calibration visualization
        cv2.namedWindow('Calibration')
        cv2.setMouseCallback('Calibration', self.Segment) # Changes mouse event

        veccolor = ['BLUE', 'RED', 'YELLOW', 'PURPLE']
        while True: # Main loop
            auxcolor = cv2.getTrackbarPos('Color', 'Trackbars') # Gets the color been worked
            self.color = veccolor[auxcolor]

            # Gets the values from the trackbars
            self.blur = cv2.getTrackbarPos('Blur', 'Trackbars')
            if self.blur % 2 == 0:
                self.blur += 1
            self.krnl = max(cv2.getTrackbarPos('Kernel', 'Trackbars'), 1)
            self.ersn = cv2.getTrackbarPos('Erosion', 'Trackbars')
            self.dltn = cv2.getTrackbarPos('Dilatation', 'Trackbars')
            self.rads = max(cv2.getTrackbarPos('Radius', 'Trackbars'), 1)
            self.thrs = max(cv2.getTrackbarPos('Threshold', 'Trackbars'), 1)

            self.capture() # Captures the image

            # Creates a image showing the color been segmented
            track = np.zeros((50, 300, 3), np.uint8)
            c = [(255,255,100), (100,100,255), (100,255,255), (200,100,200)]
            track[:,:] = c[auxcolor]
            
            cv2.imshow('Trackbars', track)
            final = self.img

            threshs = [self.Blue, self.Red, self.Yellow, self.Purple]
            
            # Segments hsv image for blue
            mask = cv2.inRange(self.hsv, threshs[auxcolor][0:3], threshs[auxcolor][3:6])
            # Creates a kernel for erosion/dilatation
            kern = np.ones((self.krnl, self.krnl), np.uint8)
            # Erodes mask
            erod = cv2.erode(mask, kern, iterations=self.ersn)
            # Dilatates mask
            dila = cv2.dilate(erod, kern, iterations=self.dltn)
            # Get contours in the mask
            cnt,_ = cv2.findContours(dila, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # Draws the contours
            cv2.drawContours(final, cnt, -1, c[auxcolor], -1)

            # Draws a circle around mouse
            cv2.circle(final, self.pos, self.rads, (200, 200, 200), 1)
            
            # Shows final image
            cv2.imshow('Calibration', final)

            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                flag = 'E'
                break
            elif k == 114:
                self.Reset()
            elif k == 118:
                flag = 'V'
                break

        cv2.destroyAllWindows()
        self.cap.release()
        print '>>> Calibration Terminated <<<'

        if flag == 'V':
            return 0
        elif flag == 'E':
            return 3

    #----------------------------------------------------------------------------------------------
    #   Method to see the results of calibration process
    #----------------------------------------------------------------------------------------------
    def Verify(self):
        self.InitCap()
        cv2.namedWindow('Calibration') # Creates a window
        flag = None # Control flag
        while True:
            self.capture()
            c = [(255,255,100), (100,100,255), (100,255,255), (200,100,200)]
            final = np.copy(self.img)
            threshs = [self.Blue, self.Red, self.Yellow, self.Purple]
            for i in range(4):
                # Segments hsv image for blue
                mask = cv2.inRange(self.hsv, threshs[i][0:3], threshs[i][3:6])
                # Creates a kernel for erosion/dilatation
                kern = np.ones((self.krnl, self.krnl), np.uint8)
                # Erodes mask
                erod = cv2.erode(mask, kern, iterations=self.ersn)
                # Dilatates mask
                dila = cv2.dilate(erod, kern, iterations=self.dltn)
                # Get contours in the mask
                cnt,_ = cv2.findContours(dila, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                # Draws the contours
                cv2.drawContours(final, cnt, -1, c[i], -1)
            cv2.imshow('Calibration', final)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                flag = 'E'
                break
            elif k == 115:
                flag = 'F'
                break
            elif k == 99:
                flag = 'C'
                break
        
        cv2.destroyAllWindows()
        self.cap.release()

        if flag == 'F':
            return 2
        elif flag == 'C':
            return 1
        elif flag == 'E':
            return 3

    #----------------------------------------------------------------------------------------------
    #   Maint method
    #----------------------------------------------------------------------------------------------
    def Main(self):
        while True:
            x = self.Verify()
            if x == 1:
                print '>>> Start Calibration <<<'
                x = self.Calibration()
            elif x == 2:
                self.Finish()
                break
            elif x == 3:
                break


    #----------------------------------------------------------------------------------------------
    #   Method which saves the thresholds
    #----------------------------------------------------------------------------------------------
    def Finish(self):
        string = '' # Creates an empty string
        # Converts the data into a string
        for Vec in [self.Blue, self.Red, self.Yellow, self.Purple]:
            for v in Vec:
                string += str(v) + ' '

        for v in [self.blur, self.krnl, self.ersn, self.dltn, self.rads, self.thrs]:
            string += str(v) + ' '

        # Writes the string to a file
        file = open('.thresholds', 'w')
        file.write(string)
        file.close()

        print '>>> Calibration Saved <<<'

#--------------------------------------------------------------------------------------------------
#   Method that does nothing, used by trackbars on cv2
#--------------------------------------------------------------------------------------------------
def nothing(x):
    pass
