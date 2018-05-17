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
from sklearn.externals import joblib # Reading data recorded by sklearn.

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
    
    ## lastupdate
    __lastupdate = -1
    
    ## filename
    __filename = './Data/distance_network.sav'
    
    ## finalize
    # .
    def finalize(self):
        '''Closes the process and saves changes.'''
       
        self._finalize()
        if self._args.robots == True:
            cv2.destroyAllWindows()
        
        for team in self.__teams:
            team._end()
        self._end()
    
    ## Constructor Class
    def __init__(self, a):
        '''Initialize the class and instantiate the objects needed to detect the robots.
        @param a Entry Parameters of the vision system.'''
        super(Robots, self).__init__(a, 'Robots', 'Parameters')
        
        self.__parameters = {
            "percentage_time_color": 10,
        }
        
        self.__parameters = self._conf.readVariables(self.__parameters)
        
        self.__teams = []
        self.__teams.append(ColorSegmentation("Cyano", a, False))
        self.__teams.append(ColorSegmentation("Magenta", a, False))
        
        self.__nndistance = joblib.load(self.__filename)
        
        #Clear blackboard
        for number in xrange(1,22):
            self._bkb.write_int("VISION_RB" + str(number).zfill(2) + "_TAG", 0)
        
        self.start()
        
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
    #                         cv2.destroyWindow(__teams[j].color + ' Segmentation')
                            break
                    self.__teams[j].show = False
                else:
                    mask = self.__teams[j].segmentation(
                        data["frame"][xmin:xmax, ymin:ymax, :]
                    )
                area = sum(sum(mask))*100.0/((xmax - xmin)*(ymax - ymin)) 
                if area >= self.__parameters["percentage_time_color"] and maxcolor < area:
                    maxcolor = area
                    time = j*2 - 1
            time_robot.append(time)
        data["objects"]["time"] = np.array(time_robot)
        return data
    
    ## estimatedDistance
    def __estimatedDistance(self, data):
        '''Estimate the distance of the object using neural network.
        @param data Data to be used for analysis.
        @return Returns the increased distance data of the objects.'''
        listdist = []
        for ymin, xmin, ymax, xmax in data['objects']['boxes']:
    
            listdist.append([
                np.cos(0.9075712110370513*(0.5 - (xmax + xmin)/2))*self.__nndistance.predict(ymax - ymin)[0],
                np.sin(0.9075712110370513*(0.5 - (xmax + xmin)/2))*self.__nndistance.predict(ymax - ymin)[0]
            ])
            
        data['objects']['dist'] = listdist    
        return data
    
    ## __writeBlackboard
    # .
    def __writeBlackboard(self, data):
        number = 1    
        for __, __, __, robot, [xdist, ydist] in data['objects'].values:
            while number < 22 and self._bkb.read_int("VISION_RB" + str(number).zfill(2) + "_TAG") != 0:
                number += 1
            
            if number == 22: #Full memory
                break
            
            self._bkb.write_float("VISION_RB" + str(number).zfill(2) + "_X", xdist)
            self._bkb.write_float("VISION_RB" + str(number).zfill(2) + "_Y", ydist*1.2)
            self._bkb.write_double("VISION_RB" + str(number).zfill(2) + "_TIME", data['time']),
            self._bkb.write_int("VISION_RB" + str(number).zfill(2) + "_MOV", data['mov']),
            self._bkb.write_int("VISION_RB" + str(number).zfill(2) + "_TAG", robot + 2)
    
    ## __classification
    def __classification(self, data):
        '''Sorting Detected Robots and Writing on Blackboard.'''
        
        if self.__lastupdate > data['time']:
            return
        self.__lastupdate = data['time'] + 1
        
        self.__teamDetection(data)
        self.__estimatedDistance(data)
        self.__writeBlackboard(data)
        
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
                self.__menu = 'setcolor'
            elif keyboard == ord('q'):
                self._running = False
    
    ## classifyingRobots
    def classifyingRobots(self, data):
        if self._running == False:
            raise VisionException(5, 'Robots')
        self.__listdata.append(data)
        self._resume()
    
    ## run
    def run(self):
        '''Execution loop.'''
        self._running = True
        while self._running:
            with self._pausethread:
                while self.__listdata != []:
                    data = self.__listdata.pop(0)
                    self.__classification(data)
            self._pause( )
