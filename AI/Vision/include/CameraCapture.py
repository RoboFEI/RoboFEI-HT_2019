# coding: utf-8

# ****************************************************************************
# * @file: CameraCapture.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class CameraCapture
# ****************************************************************************

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the vision system.
import os # Library for interaction with the system
from copy import copy # To create copies of the variables
import time # Using for time control and measurement
import cv2 # OpenCV library used for image processing.

# Used class developed by RoboFEI-HT.
from BasicThread import * # Base class with primary functions

## Class CameraCapture
# Class responsible for performing the observation of domain.
class CameraCapture(BasicThread):
    
    # ---- Variables ----
    
    ## Camera variable
    # Responsible for communicating with the camera.
    __camera = None
    
    ## Port variable
    # Port where the camera is connected.
    __port = None
    
    ## observation variable
    # Saves the observation of the most recent state.
    __observation = None
    
    ## running variable
    # Flag responsible for executing camera capture
    _running = None
    
    ## cameraOpen
    # Used to locate the port where the camera is connected and connect to it.
    # @return Returns the object of the camera and the port on which it is connected.
    def __cameraOpen(self):
        p = os.popen('ls /dev/video*')
        line = p.readline()
        if line == '':
            raise VisionException(1, '')
        
        for port in xrange(10):
            camera = cv2.VideoCapture(port)
            if camera.isOpened():
                break
        
        if not camera.isOpened():
            raise VisionException(2, '')
        return camera, port
    
    ## trackbarFocus
    # Responsible for reading the values of the trackbar.
    # @param value Amount to be processed.
    def __trackbarFocus(self, value):
        self.__observation['focus'] = value
        os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c focus_absolute=" + str(self.__observation['focus']))
    
    ## trackbarSaturation
    # Responsible for reading the values of the trackbar.
    # @param value Amount to be processed.
    def __trackbarSaturation(self, value):
        self.__observation['saturation'] = value
        os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c saturation=" + str(self.__observation['saturation']))
    
    ## finalize
    # Terminates the capture process and saves the generated information
    def finalize(self):
        cv2.destroyAllWindows()
        super(CameraCapture, self)._finalize()
        self.__camera.release()
        
        if 'frame' in self.__observation.keys():
            del self.__observation['frame']
        if 'pos_tilt' in self.__observation.keys():
            del self.__observation['pos_tilt']
        if 'pos_pan' in self.__observation.keys():
            del self.__observation['pos_pan']
        if 'time' in self.__observation.keys():
            del self.__observation['time']
        super(CameraCapture,self)._end( )
    
    ## Constructor Class
    def __init__(self, arg):
        print '\33[1;33m' + '---- Initializing class camera ----' + '\33[0m'
        super(CameraCapture, self).__init__(arg, 'Camera' , 'parameters')
        
        self.__observation = {
            'fps': 30,
            'focus': 25,
            'saturation': 128,
            'resolution': '2304x1536'
        }
        self.__observation = self._conf.readVariables(self.__observation)
        
        self.__camera, self.__port = self.__cameraOpen()
        
        self.__camera.set(3,int(self.__observation['resolution'].split('x')[0]))
        self.__camera.set(4,int(self.__observation['resolution'].split('x')[1]))
        
        os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c focus_auto=0")
        os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c focus_absolute=" + str(self.__observation['focus']))
        os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c saturation=" + str(self.__observation['saturation']))
        
        self.start()
        
    ## run
    # Function that will be executed as a thread
    def run(self):
        self._running = True
        
        if self._args.camera is True:
            cv2.namedWindow('Camera parameters')
            cv2.createTrackbar('focus', 'Camera parameters', self.__observation['focus'], 250, self.__trackbarFocus)
            cv2.createTrackbar('saturation', 'Camera parameters', self.__observation['saturation'], 255, self.__trackbarSaturation)
            print ""
        
        while self._running:
            start = time.time()
            
            __, self.__observation['frame'] = self.__camera.read()
            self.__observation['pos_tilt'] = self._bkb.read_float('VISION_TILT_DEG')
            self.__observation['pos_pan'] = self._bkb.read_float('VISION_PAN_DEG')
            self.__observation['time'] = time.localtime()
            
            if self._args.camera == True:
                cv2.imshow(
                    'Camera parameters',
                    cv2.resize(
                        self.__observation['frame'],
                        None,
                        fx=380.0/self.__observation['frame'].shape[0],
                        fy=380.0/self.__observation['frame'].shape[0]
                    )
                )
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self._args.camera = 'off'
                    cv2.destroyAllWindows()
            else:
                if start + 1.0/self.__observation['fps'] - time.time() > 0:
                    time.sleep( # Camera fps
                        start + 1.0/self.__observation['fps'] - time.time()
                    )
            
            if self._args.camera == True or self._args.camera == 'off':
                diff = time.time() - start
                s = '\33[0;36m' + 'FPS' + '\33[0m' + ': ' + str(1.0/(diff))
                self.printPreviousLine(s)
    
    ## currentObservation
    def currentObservation(self):
        return self.__observation.copy()