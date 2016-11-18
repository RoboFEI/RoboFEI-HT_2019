import numpy as np
import os
import ctypes
import pygame
from math import *
import random as rnd
from screen import *

class VISION():
    #----------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, robot):
        self.robot = robot # Saves the robot object's address

        self.bkb = self.robot.bkb # Holds Blackboard's address
        self.Mem = self.robot.Mem # Holds memory key

        self.fov = 180 # Total field of view in degrees

    def Draw(self, where):
        nx = self.robot.x + 1000 * cos(radians(self.fov/2.0 - self.robot.rotate))
        ny = self.robot.y + 1000 * sin(radians(self.fov/2.0 - self.robot.rotate))
        pygame.draw.line(where, (0, 0, 0), (self.robot.x, self.robot.y), (nx, ny), 1)

        nx = self.robot.x + 1000 * cos(radians(-self.fov/2.0 - self.robot.rotate))
        ny = self.robot.y + 1000 * sin(radians(-self.fov/2.0 - self.robot.rotate))
        pygame.draw.line(where, (0, 0, 0), (self.robot.x, self.robot.y), (nx, ny), 1)

    def DrawLM(self, where):
        pygame.draw.circle(where, (0, 200, 255), (70, 70), 10, 2) # Draw Blue
        pygame.draw.circle(where, (255, 0, 0), (970, 70), 10, 2) # Draw Red
        pygame.draw.circle(where, (255,255,0), (70, 670), 10, 2) # Draw Yellow
        pygame.draw.circle(where, (100, 0, 200), (970, 670), 10, 2) # Draw Purple

    def GetLM(self, which = None): # B R Y P
        if which == 'B': # (00)
            dist = hypot(self.robot.x-70, self.robot.y-70)
            ang = -degrees(atan2(70-self.robot.y, 70-self.robot.x)) - self.robot.rotate
            return dist, ang
        elif which == 'R': # (10)
            dist = hypot(self.robot.x-970, self.robot.y-70)
            ang = -degrees(atan2(70-self.robot.y, 970-self.robot.x)) - self.robot.rotate
            return dist, ang
        elif which == 'Y': # (01)
            dist = hypot(self.robot.x-70, self.robot.y-670)
            ang = -degrees(atan2(670-self.robot.y, 70-self.robot.x)) - self.robot.rotate
            return dist, ang
        elif which == 'P': # (11)
            dist = hypot(self.robot.x-970, self.robot.y-670)
            ang = -degrees(atan2(670-self.robot.y, 970-self.robot.x)) - self.robot.rotate
            return dist, ang
        else:
            return None, None

    def RetLM(self):
        y = []
        for x in ('B', 'R', 'Y', 'P'):
            ang = self.GetLM(x)[1]
            if CompAng(ang, 0, self.fov/2.0):
                y.append(rnd.gauss(ang, 3))
            else:
                y.append(None)
        return y

def CompAng(ang, base, rng):
    xa = cos(radians(ang))
    ya = sin(radians(ang))
    xb = cos(radians(base))
    yb = sin(radians(base))
    xr = cos(radians(rng))
    yr = sin(radians(rng))

    d = hypot(xa-xb, ya-yb)
    c = hypot(xr-1, yr)

    return d < c