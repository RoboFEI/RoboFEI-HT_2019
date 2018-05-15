# coding: utf-8

import sys
import time
import cv2
sys.path.append('../include')
from BasicThread import * # Importing the class that administrate threads.

class Landmarks(BasicThread):

    ## listdata
    __listdata = [ ]
    __centerClass = [ ]

    ## Constructor Class
    def __init__(self, arg):
        super(Landmarks, self).__init__(arg, 'DNN', 'Parameters')
        print 'Initializing'
        self.start()

## __classification
    def __classification(self, data):
        # print data['objects'].loc[:, ['boxes']].values  # Return a list of the values from column boxes
        print data['objects']

        #######  Calculate the center of the boxes  ##############################################
        # print len(data['objects'].loc[:, ['classes']])
        # for x in xrange(len(data['objects'].loc[:, ['classes']])):
        #     self.__centerClass = 1*((data['objects'].loc[[x], ['boxes']].values.tolist())[0])[0]
        #     print self.__centerClass[2] -(self.__centerClass[2]-self.__centerClass[0])/2
        #     print self.__centerClass[3] -(self.__centerClass[3]-self.__centerClass[1])/2
        #######  Calculate the center of the boxes  ##############################################

        raw_input()

    ## classifyingLand
    def classifyingLand(self, data):
        if self._running == False:
            raise VisionException(5, 'Robots') #raise: Force an exception.
        self.__listdata.append(data)
        self._resume()

    ## run
    def run(self):
        '''Execution loop.'''
        self._running = True
        while self._running:
            with self._pausethread: #Stop the thread until self.resume() have been executed in ClassifyingLand.
                while self.__listdata != []:
                    data = self.__listdata.pop(0)
                    self.__classification(data)
            self._pause( )

        #Finalizing the thread
    def finalize(self):
        self._finalize()
        self._end()
        cv2.destroyAllWindows()
