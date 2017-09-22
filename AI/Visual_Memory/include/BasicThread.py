# coding: utf-8

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
    
    ## __running
    # Reports whether the thread is still running.
    __running = False
    
    ## __pauseistrue
    # Variable responsible for managing thread pause and execution.
    __pauseistrue = False
    
    ## _pausethread
    # Variable responsible for managing thread pause and execution.
    _pausethread = None
    
    ## pause
    # Function responsible for stopping thread execution.
    def _pause(self):
        if not self.__pauseistrue:
            self._pausethread.acquire()
            self.__pauseistrue = True
    
    ## resume
    # Responsible function for releasing the thread for execution.
    def _resume(self):
        if self.__pauseistrue:
            self._pausethread.notify()
            self._pausethread.release()
            self.__pauseistrue = False
    
    ## Constructor Class
    @abstractmethod
    def __init__(self, s, obj):
        # Starting parent classes
        super(BasicThread, self).__init__(s, obj)
        
        Thread.__init__(self)
        
        # Instantiating control variable.
        self._pausethread = Condition(Lock( ))
        
        # Stopping the process.
        self._pause( )
        
    ## run
    # .
    @abstractmethod
    def run(self):
        self.__running = True
        while self.__running:
            with self._pausethread:
                print "Hello Word !"
                time.sleep(1)
            self._pause( )
    
    ## _finalize
    # .
    def _finalize(self):
        self.__running = False
        self._resume( )
        self.join( )