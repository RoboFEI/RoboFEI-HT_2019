# coding: utf-8

# ****************************************************************************
# * @file: ConfigIni.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class ConfigIni
# ****************************************************************************

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append("../include")
sys.path.append("../src")

# The standard libraries used in the vision system.
import configparser # Used to read ini files

# Used class developed by RoboFEI-HT.
from VisualMemoryException import * # Used to handle exceptions

## Class to config ini
# Class used to read the ini file from the view.
class ConfigIni(object):
    
    # ---- Variables ----
    
    ## Address
    # Path of the config.ini file.
    __address = "./Data/config.ini"
    
    ## Dictionary
    # Dictionary to be used.
    __dictionary = None
    
    ## myobject
    # Class requesting variable reading.
    __myobject = None
    
    ## function
    # Function that requests the reading of variables.
    __function = None
    
    ## __conf
    # Variable for instantiation of the configparser responsible for reading ini files.
    __conf = None
    
    ## Constructor Class
    def __init__(self, obj, func, address=None):
        # Testing new address
        if address != None:
            self.__address = address
        
        # Instantiating class variables.
        self.__myobject = obj
        self.__function = func
        self.__conf = configparser.RawConfigParser()
        
        # Checking file existence
        if self.__conf.read(self.__address) is []:
            print "Config.ini file not found!"
            
        # Checking section existence
        if (self.__myobject + " - " + self.__function).upper() in self.__conf.sections():
            return
        else:
            print (self.__myobject + " - " + self.__function).upper(), "section not found!"
        
    ## readVariables
    # Function used to instantiate the dictionary that was used and update it with the config variables.
    # @ param base Used dictionary.
    def readVariables(self, base):
        self.__dictionary = base # Saving class dictionary.
        
        # Checking section existence
        if (self.__myobject + " - " + self.__function).upper() in self.__conf.sections():
            # Completing/Overwriting dictionary values.
            for key in self.__conf[(self.__myobject + " - " + self.__function).upper()].keys():
                try: # Reading int
                    self.__dictionary[str(key)] = self.__conf.getint((self.__myobject + " - " + self.__function).upper(), str(key))
                    continue
                except ValueError:
                    pass
    
                try: # Reading float
                    self.__dictionary[str(key)] = self.__conf.getfloat((self.__myobject + " - " + self.__function).upper(), str(key))
                    continue
                except ValueError:
                    pass
    
                try: # Reading bool
                    self.__dictionary[str(key)] = self.__conf.getboolean((self.__myobject + " - " + self.__function).upper(), str(key))
                    continue
                except ValueError:
                    pass
    
                try: # Reading string
                    self.__dictionary[str(key)] = self.__conf.get((self.__myobject + " - " + self.__function).upper(), str(key))
                    continue
                except ValueError:
                    pass
        
        return self.__dictionary
    
    ## end
    # Responsible for saving the changes in config file.
    def end(self):
        self.__conf.read(self.__address)
            
        with open(self.__address, "wb") as configfile:
            self.__conf[(self.__myobject + " - " + self.__function).upper()] = self.__dictionary
            self.__conf.write(configfile)