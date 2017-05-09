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
            if CompAng(ang, 0, self.fov/2.0) and 0.25 >rnd.random():
                y.append(rnd.gauss(ang, 5.0))
            else:
                y.append(-999) # Return this if not seen the ball
        return y

    def GetBall(self):
        dist = hypot(self.robot.x-self.robot.ball.x, self.robot.y-self.robot.ball.y)
        ang = -degrees(atan2(self.robot.ball.y-self.robot.y, self.robot.ball.x-self.robot.x))-self.robot.rotate
        if CompAng(ang, 0, self.fov/2.0):
            return dist, ang
        else:
            return -1, -1

    def VisionProcess(self):
        control = self.bkb.read_int(self.Mem, 'DECISION_LOCALIZATION') # Variable which controls what the Localization does
        if control == 0:
            dist, ang = self.GetBall() # Returns the distance and angle to the ball
            dist = rnd.gauss(dist, dist/10.0) # Adds a gaussian error to the distance
            ang = rnd.gauss(ang, 3.0) # Adds a gaussian error to the angle measure

            self.bkb.write_float(self.Mem, 'VISION_BALL_DIST', dist) # Writes to the Black Board
            self.bkb.write_float(self.Mem, 'VISION_PAN_DEG', ang) # Writes to the Black Board
        elif control == 1:
            y = self.RetLM() # Gets the landmarks angles

            # Writes to the Black Board
            self.bkb.write_float(self.Mem,'VISION_BLUE_LANDMARK_DEG', y[0]) 
            self.bkb.write_float(self.Mem,'VISION_RED_LANDMARK_DEG', y[1])
            self.bkb.write_float(self.Mem,'VISION_YELLOW_LANDMARK_DEG', y[2])
            self.bkb.write_float(self.Mem,'VISION_PURPLE_LANDMARK_DEG', y[3])

    def test(self):
        y = []
        for x in ('B', 'R', 'Y', 'P'):
            ang = self.GetLM(x)[1]
            if CompAng(ang, 0, self.fov/2.0):
                y.append(ang)
            else:
                y.append(None) # Return this if not seen the ball
        y.append(self.robot.x)
        y.append(self.robot.y)
        y.append(self.robot.rotate)
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