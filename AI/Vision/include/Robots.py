# coding: utf-8

# ****************************************************************************
# * @file: Robots.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class Robots
# ****************************************************************************

# ---- Imports ----

# The standard libraries used in the vision system.

# The standard libraries used in the vision system.
import cv2 # OpenCV library used for image processing.

# Used class developed by RoboFEI-HT.
from DNN import * # Class that implements object detection using a deep neural network (DNN).
from ColorSegmentation import * # Class responsible for color segmentation.
from BasicThread import * # Responsible for implementing the methods and variables responsible for managing the thread.

## Class Robots
class Robots(BasicThread):
    '''Class responsible for detecting thefts and a time of classification they belong.'''
    
    # ---- Variables ----
    
    ## listdata
    __listdata = [ ]
    
    ## menu
    __menu = 'show'
    
    ## Constructor Class
    def __init__(self, a):
        '''Initialize the class and instantiate the objects needed to detect the robots.
        @param a Entry Parameters of the vision system.'''
        super(Robot, self).__init__(a, 'Robots', 'Parameters')
        
        __parameters = {
            "percentage_time_color": 10,
        }
        
        __parameters = self._conf.readVariables(__parameters)
        
        __teams = []
        self.__teams.append(ColorSegmentation("Cyano", a, False))
        self.__teams.append(ColorSegmentation("Magenta", a, False))
        
    ## cutObject
    def __cutObject(self, index, data):
        '''Returns the cutoff window in the uploaded index image.
        @param index Position of the date that will be used to create the window cut.
        @param data Data used to perform image cropping.
        @return Returns a vector with the frame to be cut.'''
        return np.array(
            data["objects"]["boxes"].values[index] * np.array(
                data["frame"].shape[:2] + data["frame"].shape[:2]
            ),
            dtype = int
        )
    
    ## teamDetection
    def __teamDetection(self, data):
        global self.__menu #debug-ipython
        '''Detects which team belongs to the robot.
        @param data Data that will be analyzed for the detection of teams.
        @return Returns a DataFrame with the teams.'''
        time_robot = []
        for i in xrange(len(data["objects"])):
            xmin, ymin, xmax, ymax = self.__cutObject(i, data)            
            maxcolor = -1
            time = 0
            for j in xrange(len(self.__teams)):
                if self._args.robots == True and self.__menu == 'setcolor':
                    self.__teams[j].show = True
                    while True:
                        mask = self.__teams[j].segmentation(
                            data["frame"][xmin:xmax, ymin:ymax, :]
                        )
                        if cv2.waitKey(1) == ord('q'):
                            cv2.destroyAllWindows()
                            break
                    self.__teams[j].show = False
                else:
                    mask = self.__teams[j].segmentation(
                        data["frame"][xmin:xmax, ymin:ymax, :]
                    )
                area = sum(sum(mask))*100.0/((xmax - xmin)*(ymax - ymin)) 
                if area >= __parameters["percentage_time_color"] and maxcolor < area:
                    maxcolor = area
                    time = j + 1
            time_robot.append(time)
        data["objects"]["time"] = np.array(time_robot)
        return data
    
    ## classification
    # .
    def classification(self, data):
        global self.__menu #debug-ipython
        self.__teamDetection(data)
        
        # Displaying parameter windows
        if self._args.robots == True:
            self.__menu = 'show'
            cv2.imshow(
                'Robots parameters',
                cv2.resize(
                    data['frame'],
                    None,
                    fx=380.0/data['frame'].shape[0],
                    fy=380.0/data['frame'].shape[0]
                )
            )
            keyboard = cv2.waitKey(1)
            if keyboard == ord('s'):
                cv2.destroyAllWindows()
                self.__menu = 'setcolor'
            elif keyboard == ord('q'):
                cv2.destroyAllWindows()
                raise VisionException(5, 'Robots')
    
    while True:
        del observation['objects']['time']
        try:
            classification(observation)
        except:
            break
    
    observation['objects']
    
    #self-iPython classificatio
    
    ## run
    def run(self):
        '''Execution loop.'''
        self._running = True
        while self._running:
            with self._pausethread:
                while self.__listdata != []:
                    data = self.__listdata.pop(0)
                    self.classification(data)
            self._pause( )