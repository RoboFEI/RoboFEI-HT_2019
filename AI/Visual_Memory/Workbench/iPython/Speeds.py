# coding: utf-8

# ****************************************************************************
# * @file: Speeds.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class Speeds
# ****************************************************************************

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append("../include")
sys.path.append("../src")

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from Basic import * # Class with implementations and basic variables

## Class to Speeds
# Class responsible for managing the robot's possible speeds (me).
class Speeds(Basic):
    
    # ---- Variables ----
    
    ## __movementslist
    # Velocity list of robot movements.
    __movementslist = []
    
    ## __u
    # Speed matrix $u_t$.
    __u = None
    
    ## __R
    # Speed error matrix $R_t$.
    __R = None
    
    ## Constructor Class
    # Initializes basic network parameters and creates standard speeds.
    def __init__(self):
        self.__movementslist.append({
            "x_speed": sym.Matrix([
                [0], # v_x
                [0], # v_y
                [0], # a_x
                [0], # a_y
                [1], # constant
            ]),
                
            "R": sym.Matrix(sym.Identity(6)*0)
        })
        
        __t = sym.symbols("t") # Declaring variable time
        
        # Robot speed and acceleration variables
        self.vrx, self.vry = sym.symbols("vr_x vr_y")
        self.arx, self.ary = sym.symbols("ar_x ar_y")
        
        # Kalman filter matrices
        self.__u = sym.Matrix([
            [0],
            [0],
            [0],
            [0],
            [1],
        ])
        
        self.__R = sym.Matrix(sym.Identity(6)*1000)
        
    ## update
    # Adds average robot speeds or upgrades to speeds.
    # @param vector Observed speed.
    def update(self, vector):
        if vector[0] == 0:
            return
        
        if vector[0] + 1 > len(self.__movementslist):
            while vector[0] + 1 > len(self.__movementslist):
                self.__movementslist.append({
                    "x_speed": sym.Matrix([
                        [0], # v_x
                        [0], # v_y
                        [0], # a_x
                        [0], # a_y
                        [1], # constant
                    ]),
    
                    "R": copy(self.__R)
                })
        
        self.__movementslist[vector[0]]["x_speed"] = -sym.Matrix(vector[1][2:]).row_insert(4, sym.Matrix([-1]))
        self.__movementslist[vector[0]]["R"] = vector[2]
    
    ## __getitem__
    # Returns the dictionary of motion vectors.
    # @param x Vector position to be accessed.
    # @return Returns the dictionary that will be used.
    def __getitem__(self, x):
        if x + 1 > len(self.__movementslist):
            while x + 1 > len(self.__movementslist):
                self.__movementslist.append({
                    "x_speed": sym.Matrix([
                        [0], # v_x
                        [0], # v_y
                        [0], # a_x
                        [0], # a_y
                        [1], # constant
                    ]),
    
                    "R": copy(self.__R)
                })
        return self.__movementslist[x]