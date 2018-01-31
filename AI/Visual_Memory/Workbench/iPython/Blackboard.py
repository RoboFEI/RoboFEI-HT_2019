# coding: utf-8

# ****************************************************************************
# * @file: Blackboard.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class Blackboard
# ****************************************************************************

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the vision system.
import configparser # Used to read ini files

# Used class developed by RoboFEI-HT.
from VisualMemoryException import * # Used to handle exceptions

# Import a shared memory.
sys.path.append('../Blackboard/src/')
from SharedMemory import SharedMemory

## Class to Blackboard
# Class used to manage blackboard writing and reading.
class Blackboard(object):
    
    # ---- Variables ----
    
    ## mem
    # Number used to write to shared memory.
    __mem = None
    
    ## bkb
    # C ++ libraries with shared memory functions.
    __bkb = None
    
    ## Constructor Class
    # Instantiating objects and reading default values.
    def __init__(self):
        self.__bkb = SharedMemory() # Instantiating blackboard functions in C ++.
        self.__mem = configparser.RawConfigParser() # Instantiating library to find robot number.
        
        # Looking for config.ini file
        if self.__mem.read('../Control/Data/config.ini') is not [] and "Communication" in self.__mem.sections() and "no_player_robofei" in self.__mem["Communication"].keys():
            self.__mem = int(self.__mem["Communication"]["no_player_robofei"])*100
        else:
            # Error while not finding file, section or number of robot.
            raise VisualMemoryException(0, 'Could not read config, no robot number')
        
        # Creating blackboard with config.ini read value.
        self.__mem = self.__bkb.shd_constructor(self.__mem)
        
    ## write_float
    # Used to do the writing of float variables on the blackboard.
    # @param variable Name of the variable that will be accessed in the blackboard.
    # @param value Value to be written.
    def write_float(self, variable, value):
        self.__bkb.write_float(self.__mem, variable, value)
    
    ## read_float
    # Used to read float values from the blackboard.
    # @param variable Variable that will be read from blackbord.
    # @return Read value of variable.
    def read_float(self, variable):
        return self.__bkb.read_float(self.__mem, variable)
    
    ## write_int
    # Used to do the writing of int variables on the blackboard.
    # @param variable Name of the variable that will be accessed in the blackboard.
    # @param value Value to be written.
    def write_int(self, variable, value):
        self.__bkb.write_int(self.__mem, variable, value)
    
    ## read_int
    # Used to read int values from the blackboard.
    # @param variable Variable that will be read from blackbord.
    # @return Read value of variable.
    def read_int(self, variable):
        return self.__bkb.read_int(self.__mem, variable)
    
    ## write_double
    # Used to do the writing of double variables on the blackboard.
    # @param variable Name of the variable that will be accessed in the blackboard.
    # @param value Value to be written.
    def write_double(self, variable, value):
        self.__bkb.write_double(self.__mem, variable, value)
    
    ## read_double
    # Used to read double values from the blackboard.
    # @param variable Variable that will be read from blackbord.
    # @return Read value of variable.
    def read_double(self, variable):
        return self.__bkb.read_double(self.__mem, variable)