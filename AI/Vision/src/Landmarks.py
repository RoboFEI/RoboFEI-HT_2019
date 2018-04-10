# coding: utf-8

import sys
import time
import cv2
sys.path.append('../include')
from BasicThread import * # Importing the class that administrate threads.

class Landmarks(BasicThread):


    ## Constructor Class
    def __init__(self, arg):
        super(Landmarks, self).__init__(arg, 'DNN', 'Parameters')
    print 'Initializing'

    #Execution using thread
    def run(self, observation):
        self._running = True #Initializing thread
        #with self._pausethread:
        self.runing()
        time.sleep(1)
        self._pause()

    #Finalizing the thread
    def finalize(self):
        print 'Finalizing'
        self._running = False

    def runing(self):
        print 'Runing'
