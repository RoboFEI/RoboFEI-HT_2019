import numpy as np
import os
import ctypes
import pygame
from math import *
import random
from screen import *

class VISION():
    #----------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, robot):
        self.robot = robot # Saves the robot object's address

        self.bkb = self.robot.bkb # Holds Blackboard's address
        self.Mem = self.robot.Mem # Holds memory key

        self.fov = 72 + 180 # Total field of view in degrees

    def Draw(self, where):
        nx = self.robot.x + 1000 * cos(radians(self.fov/2.0 - self.robot.rotate))
        ny = self.robot.y + 1000 * sin(radians(self.fov/2.0 - self.robot.rotate))
        pygame.draw.line(where, (0, 0, 0), (self.robot.x, self.robot.y), (nx, ny), 1)

        nx = self.robot.x + 1000 * cos(radians(-self.fov/2.0 - self.robot.rotate))
        ny = self.robot.y + 1000 * sin(radians(-self.fov/2.0 - self.robot.rotate))
        pygame.draw.line(where, (0, 0, 0), (self.robot.x, self.robot.y), (nx, ny), 1)

    def GetLM(self):
        pass
