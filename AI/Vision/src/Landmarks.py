# coding: utf-8

import sys
import time
import cv2
sys.path.append('../include')
from BasicThread import * # Importing the class that administrate threads.

class Landmarks(BasicThread):

    ## listdata
    __listdata = [ ]

    ## Constructor Class
    def __init__(self, arg):
        super(Landmarks, self).__init__(arg, 'DNN', 'Parameters')
        print 'Initializing'
        self.start()

## __classification
    def __classification(self, data):
        print "testeeeeeee"

    ## classifyingLand
    def classifyingLand(self, data):
        if self._running == False:
            raise VisionException(5, 'Robots') #raise: Force an exception.
        print data['objects']# pandas
        print data['objects'].loc[[0],['boxes']] #Selecionando os valores da tabela de dados "data"
        raw_input()
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
        print 'Finalizing'
        self._running = False
