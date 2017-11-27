# coding: utf-8

# ****************************************************************************
# * @file: BasicThread.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class BasicThread
# ****************************************************************************

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the visual memory system.
from threading import Thread, Condition, Lock # Used to create classes with thread functions

# Used class developed by RoboFEI-HT.
from KalmanFilter import * # Class responsible for implementing kalman filter methods.

## Class to BasicThread
# Responsible for implementing the methods and variables responsible for managing the thread.
class BasicThread(KalmanFilter, Thread):
    __metaclass__ = ABCMeta
    
    # ---- Variables ----
    
    ## _running
    # Reports whether the thread is still running.
    _running = False
    
    ## __pauseistrue
    # Variable responsible for managing thread pause and execution.
    __pauseistrue = False
    
    ## _pausethread
    # Variable responsible for managing thread pause and execution.
    _pausethread = None
    
    ## pause
    def _pause(self):
        '''Function responsible for stopping thread execution.'''
        if not self.__pauseistrue:
            self._pausethread.acquire()
            self.__pauseistrue = True
    
    ## resume
    def _resume(self):
        '''Responsible function for releasing the thread for execution.'''
        if self.__pauseistrue:
            self._pausethread.notify()
            self._pausethread.release()
            self.__pauseistrue = False
    
    ## Constructor Class
    @abstractmethod
    def __init__(self, a, s, obj):
        # Starting parent classes
        super(BasicThread, self).__init__(a, s, obj)
        
        Thread.__init__(self)
        
        # Instantiating control variable.
        self._pausethread = Condition(Lock( ))
        
        # Stopping the process.
        self._pause( )
        
    ## run
    @abstractmethod
    def run(self):
        '''Example of thread execution.'''
        self._running = True
        while self._running:
            with self._pausethread:
                print "Hello Word !"
                time.sleep(1)
            self._pause( )
    
    ## finalize
    def _finalize(self):
        '''Finish the object.'''
        self._running = False
        self._resume( )
        self.join( )
    
    ## threadPaused
    def _threadPaused(self):
        '''Tests whether the object is still in the crawl tolerance.'''
        return self.__pauseistrue