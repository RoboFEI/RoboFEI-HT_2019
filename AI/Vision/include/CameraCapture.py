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
    
    ## parameters variable
    # .
    __parameters = None
    
    ## observation variable
    # Saves the observation of the most recent state.
    __observation = {}
    
    ## running variable
    # Flag responsible for executing camera capture
    _running = None
    
    ## cameraOpen
    # Used to locate the port where the camera is connected and connect to it.
    # @return Returns the object of the camera and the port on which it is connected.
    def __cameraOpen(self, video):
        if video == None:
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
        else:
            camera = cv2.VideoCapture(video)
            if not camera.isOpened():
                raise VisionException(2, '')
            port = 0
            
        return camera, port
    
    ## trackbarFocus
    # Responsible for reading the values of the trackbar.
    # @param value Amount to be processed.
    def __trackbarFocus(self, value):
        self.__parameters['focus'] = value
        os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c focus_absolute=" + str(self.__parameters['focus']))
    
    ## trackbarSaturation
    # Responsible for reading the values of the trackbar.
    # @param value Amount to be processed.
    def __trackbarSaturation(self, value):
        self.__parameters['saturation'] = value
        os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c saturation=" + str(self.__parameters['saturation']))
    
    ## finalize
    # Terminates the capture process and saves the generated information
    def finalize(self):
        if self._args.camera == True:
            cv2.destroyAllWindows()
        
        super(CameraCapture, self)._finalize()
        self.__camera.release()
        
        super(CameraCapture,self)._end( )
    
    ## Constructor Class
    def __init__(self, arg):
        print '\33[1;33m' + '---- Initializing class camera ----' + '\33[0m'
        super(CameraCapture, self).__init__(arg, 'Camera' , 'parameters')
        
        self.__parameters = {
            'fps': 30,
            'focus': 25,
            'saturation': 128,
            'resolution': '2304x1536'
        }
        self.__parameters = self._conf.readVariables(self.__parameters)
        
        self.__camera, self.__port = self.__cameraOpen(self._args.video)
        
        self.__camera.set(3,int(self.__parameters['resolution'].split('x')[0]))
        self.__camera.set(4,int(self.__parameters['resolution'].split('x')[1]))
        
        os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c focus_auto=0")
        os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c focus_absolute=" + str(self.__parameters['focus']))
        os.system("v4l2-ctl -d /dev/video" + str(self.__port) + " -c saturation=" + str(self.__parameters['saturation']))
        
        self._pause()
        
        self.start()
        
    ## run
    # Function that will be executed as a thread
    def run(self):
        self._running = True
        
        if self._args.camera is True:
            cv2.namedWindow('Camera parameters')
            cv2.createTrackbar('focus', 'Camera parameters', self.__parameters['focus'], 250, self.__trackbarFocus)
            cv2.createTrackbar('saturation', 'Camera parameters', self.__parameters['saturation'], 255, self.__trackbarSaturation)
            print ""
        
        while self._running:
            start = time.time()
            
            self.__observation['time'] = time.time()
            __, self.__observation['frame'] = self.__camera.read()
            self.__observation['pos_tilt'] = self._bkb.read_float('VISION_TILT_DEG')
            self.__observation['pos_pan'] = self._bkb.read_float('VISION_PAN_DEG')
            self.__observation['mov'] = self._bkb.read_int('DECISION_ACTION_A')
            self._resume()
            
            if self.__observation['frame'] is None:
                break
            
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
                if cv2.waitKey(1) == ord('q'):
                    self._args.camera = 'off'
            elif self._args.video is None:
                end = start + 1.0/self.__parameters['fps'] - time.time()
                if end > 0:
                    time.sleep( # Camera fps
                        end
                    )
            else:
                end = start + 1.0/30 - time.time()
                if end > 0:
                    time.sleep( # Camera fps
                        end
                    )
            
            if self._args.camera == True or self._args.camera == 'off':
                diff = time.time() - start
                s = '\33[0;36m' + 'FPS' + '\33[0m' + ': ' + str(1.0/(diff))
                self.printPreviousLine(s)
    
    ## currentObservation
    def currentObservation(self):
        with self._pausethread:
            pass
        self._pause()
        
        if self.__observation['frame'] is None:
            if self._args.video is not None:
                raise VisionException(5, 'CameraCapture')
            else:
                raise VisionException(6, '')
        return self.__observation.copy()
