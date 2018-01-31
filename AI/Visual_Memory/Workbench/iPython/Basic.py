# coding: utf-8

# ****************************************************************************
# * @file: Basic.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class Basic
# ****************************************************************************

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the visual memory system.
from abc import ABCMeta, abstractmethod # Used to create abstract classes.
from copy import copy # Function used to duplicate data.
import sympy as sym # Class used for manipulation of arrays and symbolic variables.

# Used class developed by RoboFEI-HT.
from Blackboard import * # Class used to manage blackboard writing and reading.
from ConfigIni import * # Class used to read the ini file from the view.

## Class to Basic
# Standard and abstract class.
class Basic(object):
    __metaclass__ = ABCMeta
    
    # ---- Variables ----
    
    ## _args
    # Input arguments.
    _args = None
    
    ## _conf
    # Variable used to instantiate class ConfigIni.
    _conf = None
    
    ## _bkb
    # Variable used to instantiate class Blackboard.
    _bkb = None
    
    ## Constructor Class
    # Instantiating default classes.
    @abstractmethod
    def __init__(self, a, obj, func):
        self._args = a
        self._conf = ConfigIni(obj, func)
        self._bkb = Blackboard( )
        
    ## _end
    # Finishing classes.
    def _end(self):
        self._conf.end( )