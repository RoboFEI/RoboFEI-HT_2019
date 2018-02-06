# coding: utf-8

# ****************************************************************************
# * @file: ColorSegmentation.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 14/11/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class ColorSegmentation
# ****************************************************************************

# ---- Imports ----

# Libraries to be used
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the vision system
from abc import ABCMeta, abstractmethod # Used to create abstract classes
from threading import Thread # Used to create classes with thread functions
import numpy as np
import cv2 # OpenCV library used for image processing.

# Used class developed by RoboFEI-HT
from BasicProcesses import * # Standard and abstract class.
from VisionException import * # Used to handle exceptions

## ColorSegmentation
# Class responsible for color segmentation.
class ColorSegmentation(BasicProcesses):
    
    # ---- Variables ----
    
    ## show
    # .
    show = False
    
    ## upper
    # Range maximum values.
    __upper = None
    
    ## lower
    # Range minimum values.
    __lower = None
    
    ## Color
    # Color to segmentaion.
    color = None
    
    ## Parameters
    # Parameters used to perform color segmentation.
    __parameters = None
    
    ## Constructor Class
    def __init__(self, c, a, s):
        self.show = s
        self.color = c
        super(ColorSegmentation, self).__init__(a, self.color, "Segmentation", adreess="./Data/"+ self.color +".ini")
        
        # Creating default values and reading config
        self.__parameters = {
            'h_min': 127,
            's_min': 0,
            'v_min': 0,
            'h_max': 127,
            's_max': 255,
            'v_max': 255,
            'color_b': 0,
            'color_g': 0,
            'color_r': 0,
            'name': self.color
        }
        self.__parameters = self._conf.readVariables(self.__parameters)
        
        # define range of color in HSV
        self.__lower = np.array([self.__parameters['h_min'], self.__parameters['s_min'], self.__parameters['v_min']])
        self.__upper = np.array([self.__parameters['h_max'], self.__parameters['s_max'], self.__parameters['v_max']])
    
    ## trackbarHMin
    # Trackbar control function.
    def __trackbarHMin(self, value):
        self.__parameters['h_min'] = min(
            value, # Read trackbar value
            self.__parameters['h_max'] - 1 # Minimum possible to be in range.
        )
        
        cv2.setTrackbarPos( # Adjusting value on trackbar
                'h_min', # Name of trackbar
                self.color + ' Segmentation', # Window Name
                self.__parameters['h_min'] # Value to be set
            )
        
        #Updating minimum vector
        self.__lower = np.array([
                self.__parameters['h_min'], # Min value to hue
                self.__parameters['s_min'], # Min value to saturation
                self.__parameters['v_min'] # Min value to value
            ])
    
    ## trackbarHMax
    # Trackbar control function.
    def __trackbarHMax(self, value):
        self.__parameters['h_max'] = max(
            value, # Read trackbar value
            self.__parameters['h_min'] + 1 # Maximum possible to be in range.
        )
        
        cv2.setTrackbarPos( # Adjusting value on trackbar
                'h_max', # Name of trackbar
                self.color + ' Segmentation', # Window Name
                self.__parameters['h_max'] # Value to be set
            )
        
        #Updating maximum vector
        self.__upper = np.array([
                self.__parameters['h_max'], # Max value to hue
                self.__parameters['s_max'], # Max value to saturation
                self.__parameters['v_max'] # Max value to value
            ])
    
    ## trackbarSMin
    # Trackbar control function.
    def __trackbarSMin(self, value):
        self.__parameters['s_min'] = min(
            value, # Read trackbar value
            self.__parameters['s_max'] - 1 # Minimum possible to be in range.
        )
        
        cv2.setTrackbarPos( # Adjusting value on trackbar
                's_min', # Name of trackbar
                self.color + ' Segmentation', # Window Name
                self.__parameters['s_min'] # Value to be set
            )
        
        #Updating minimum vector
        self.__lower = np.array([
                self.__parameters['h_min'], # Min value to hue
                self.__parameters['s_min'], # Min value to saturation
                self.__parameters['v_min'] # Min value to value
            ])
    
    ## trackbarSMax
    # Trackbar control function.
    def __trackbarSMax(self, value):
        self.__parameters['s_max'] = max(
            value, # Read trackbar value
            self.__parameters['s_min'] + 1 # Maximum possible to be in range.
        )
        
        cv2.setTrackbarPos( # Adjusting value on trackbar
                's_max', # Name of trackbar
                self.color + ' Segmentation', # Window Name
                self.__parameters['s_max'] # Value to be set
            )
        
        #Updating maximum vector
        self.__upper = np.array([
                self.__parameters['h_max'], # Max value to hue
                self.__parameters['s_max'], # Max value to saturation
                self.__parameters['v_max'] # Max value to value
            ])
    
    ## trackbarVMin
    # Trackbar control function.
    def __trackbarVMin(self, value):
        self.__parameters['v_min'] = min(
            value, # Read trackbar value
            self.__parameters['v_max'] - 1 # Minimum possible to be in range.
        )
        
        cv2.setTrackbarPos( # Adjusting value on trackbar
                'v_min', # Name of trackbar
                self.color + ' Segmentation', # Window Name
                self.__parameters['v_min'] # Value to be set
            )
        
        #Updating minimum vector
        self.__lower = np.array([
                self.__parameters['h_min'], # Min value to hue
                self.__parameters['s_min'], # Min value to saturation
                self.__parameters['v_min'] # Min value to value
            ])
    
    ## trackbarVMax
    # Trackbar control function.
    def __trackbarVMax(self, value):
        self.__parameters['v_max'] = max(
            value, # Read trackbar value
            self.__parameters['v_min'] + 1 # Maximum possible to be in range.
        )
        
        cv2.setTrackbarPos( # Adjusting value on trackbar
                'v_max', # Name of trackbar
                self.color + ' Segmentation', # Window Name
                self.__parameters['v_max'] # Value to be set
            )
        
        #Updating maximum vector
        self.__upper = np.array([
                self.__parameters['h_max'], # Max value to hue
                self.__parameters['s_max'], # Max value to saturation
                self.__parameters['v_max'] # Max value to value
            ])
    
    ## segmentation
    # Function that performs the segmentation of a given color and returns a mask
    def segmentation(self, img):
        # Color segmentation
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.__lower, self.__upper)
        
        if self.show == False:
            return mask
        else:
            blank_image = np.zeros(
                img.shape,
                np.uint8
            )
            
            blank_image[:,:,0] = self.__parameters['color_b']
            blank_image[:,:,1] = self.__parameters['color_g']
            blank_image[:,:,2] = self.__parameters['color_r']
            
            img = cv2.bitwise_and(
                img,
                img,
                blank_image,
                mask = 255 - mask
            )
            
            scale = max(860.0/img.shape[1], 640.0/img.shape[0])
            if scale > 0:
                scale = min(860.0/img.shape[1], 640.0/img.shape[0])
            
            img =cv2.resize(
                img,
                (0, 0),
                fx=scale,
                fy=scale
            )
            
            cv2.imshow(
                self.color + ' Segmentation',
                img
            )
            
            if self.show == True and self.show != "":
                self.show = ""
                cv2.createTrackbar(
                    'h_min',
                    self.color + ' Segmentation',
                    self.__parameters['h_min'],
                    255,
                    self.__trackbarHMin,
                )
    
                cv2.createTrackbar(
                    'h_max',
                    self.color + ' Segmentation',
                    self.__parameters['h_max'],
                    255,
                    self.__trackbarHMax,
                )
    
                cv2.createTrackbar(
                    's_min',
                    self.color + ' Segmentation',
                    self.__parameters['s_min'],
                    255,
                    self.__trackbarSMin,
                )
    
                cv2.createTrackbar(
                    's_max',
                    self.color + ' Segmentation',
                    self.__parameters['s_max'],
                    255,
                    self.__trackbarSMax,
                )
    
                cv2.createTrackbar(
                    'v_min',
                    self.color + ' Segmentation',
                    self.__parameters['v_min'],
                    255,
                    self.__trackbarVMin,
                )
    
                cv2.createTrackbar(
                    'v_max',
                    self.color + ' Segmentation',
                    self.__parameters['v_max'],
                    255,
                    self.__trackbarVMax,
                )
            
            return mask