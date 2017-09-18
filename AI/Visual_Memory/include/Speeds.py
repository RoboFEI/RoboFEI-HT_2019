# coding: utf-8

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
class Speeds( ):
    
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
                [1], # cosntant
            ]),
                
            "R": sym.Matrix(sym.Identity(6)*0)
        })
        
        __t = sym.symbols("t") # Declaring variable time
        
        self.p_x, self.p_y, self.v_x, self.v_y, self.a_x, self.a_y = sym.symbols("self.p_x, self.p_y, self.v_x, self.v_y, self.a_x, self.a_y") # Object state variables
        
        # Robot speed and acceleration variables
        self.vr_x, self.vr_y = sym.symbols("self.vr_x self.vr_y")
        ar_x, ar_y = sym.symbols("ar_x ar_y")
        
        # Kalman filter matrices
        self.__u = sym.Matrix([
            [0],
            [0],
            [0],
            [0],
            [1],
        ])
        
        self.__R = sym.Matrix(sym.Identity(6)*1000)
        
                        [1], # cos(ωr*t)
                        [0], # sin(ωr*t)
                        [1],
                    ]),
    
                    "R": copy(self.__R)
                })
        return self.__movementslist[x]