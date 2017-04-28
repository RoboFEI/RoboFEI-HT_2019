import numpy as np
import os
import ctypes
import pygame
from math import *
import random as rnd
from screen import *

class VISION():
    #----------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, robot, clk=30.):
        self.robot = robot # Saves the robot object's address
        print self.robot.x, self.robot.y
        self.robotheight = 50 # Height in centimeters

        self.bkb = self.robot.bkb # Holds Blackboard's address
        self.Mem = self.robot.Mem # Holds memory key

        self.vfov = 14.58 # Vertical field of view
        self.hfov = 26.13 # Horizontal field of view

        self.clk = clk

        self.headtilt = 17.4 # Tilt position
        self.tiltpos = 17.4 # Chosen tilt position, default 17.4
        self.headpan = 0 # Pan position
        self.panpos = 0 # Chosen pan position

        self.maxtilt = 64 # Max tilt
        self.mintilt = 16 # Min tilt
        self.maxpan = 90 # Max pan
        self.minpan = -90 # Min pan

        self.headspd = 30 # Max head speed, in degrees per second

        # Observation points
        self.vpoints = []
        for j in [-14, -13.5]:
            for i in [-20, -13.5, -7, 0, 7, 13.5, 20]:
                self.vpoints.append((i, j))
        for i in [-20, -13.5, 0, 13.5, 20]:
            self.vpoints.append((i, -12.5))                
        for j in [-11, -7.5]:
            for i in [-20, -7, 7, 20]:
                self.vpoints.append((i, j))
        self.vpoints.append((-13.5, 0))
        self.vpoints.append((13.5, 0))
        self.vpoints.append((0, 9))

        self.behave = 0

    # Changes the tilt's position
    def tilt(self, diff=None, pos=None):
        if diff: # Adds a difference
            self.tiltpos += diff
        elif pos: # Changes the position
            self.tiltpos = pos

    # Changes the pan's position
    def pan(self, diff=None, pos=None):
        if diff != None: # Adds a difference
            self.panpos += diff
        elif pos != None: # Changes the position
            self.panpos = pos

    # Updates the head position
    def headmotion(self):
        self.headtilt += np.sign(self.tiltpos-self.headtilt) * np.min([abs(self.tiltpos-self.headtilt), self.headspd]) / self.clk
        self.headpan += np.sign(self.panpos-self.headpan) * np.min([abs(self.panpos-self.headpan), self.headspd]) / self.clk

        self.headtilt = np.min([self.maxtilt, np.max([self.mintilt, self.headtilt])])
        self.headpan = np.min([self.maxpan, np.max([self.minpan, self.headpan])])

    # Reactive head behavior
    def headBehave(self):
        x = [90,0,-90,0][self.behave]
        self.pan(pos=x)

        if self.headpan > 89 and self.behave == 0:
            self.behave = 1
        elif self.headpan < 1 and self.behave == 1:
            self.behave = 2
        elif self.headpan < -89 and self.behave == 2:
            self.behave = 3
        elif self.headpan > -1 and self.behave == 3:
            self.behave = 0
        

    # Draw the field of view of the robot
    def draw(self, where):
        # Computes distances
        f = self.robotheight/np.tan(np.radians(self.headtilt-self.vfov))
        n = self.robotheight/np.tan(np.radians(self.headtilt+self.vfov))

        # Computes point distances
        dn = n/np.cos(np.radians(self.hfov))
        df = f/np.cos(np.radians(self.hfov))

        # Array of points
        points = []

        # Create points
        for d in [dn, df]:
            for a in [self.hfov, -self.hfov]:
                x = self.robot.x + d * np.cos(np.radians(-self.robot.rotate + self.headpan + a))
                y = self.robot.y + d * np.sin(np.radians(-self.robot.rotate + self.headpan + a))
                points.append((x,y))

        # Draw the points
        for a in [0, 3]:
            for b in [1, 2]:
                pygame.draw.line(where, (255,255,255), points[a], points[b], 1)

        for point in self.vpoints:
            # Compute the point distance
            dist = (self.robotheight/np.tan(np.radians(self.headtilt+point[1])))/np.cos(np.radians(point[0]))
            # Compute the direction of the point
            angle = -self.robot.rotate+self.headpan+point[0]

            # Compute the position in the world of the point
            x = self.robot.x + dist * np.cos(np.radians(angle))
            y = self.robot.y + dist * np.sin(np.radians(angle))

            pygame.draw.line(where, (255,255,255), (x,y), (x,y), 1)

    # Return the notable variables for localization, as a vector
    def GetField(self):
        ret = []

        # Saves the heads position
        if self.headpan > 80: # If it is to the left
            ret.append(0)
            ret.append(1)
        elif self.headpan < -80: # If it is to the right
            ret.append(1)
            ret.append(0)
        elif -5 <= self.headpan and self.headpan <= 5: # If it is forward
            ret.append(1)
            ret.append(1)
        else:
            return 32*[0]

        # For each point
        for point in self.vpoints:
            # Compute the point distance
            dist = (self.robotheight/np.tan(np.radians(self.headtilt+point[1])))/np.cos(np.radians(point[0]))
            # Compute the direction of the point
            angle = -self.robot.rotate+self.headpan+point[0]

            # Compute the position in the world of the point
            x = self.robot.x + dist * np.cos(np.radians(angle))
            y = self.robot.y + dist * np.sin(np.radians(angle))

            # Verify if it is in or out of the field
            if 0 <= x and x <= 1040 and 0 <= y and y <= 740:
                ret.append(1)
            else:
                ret.append(0)
                
        # Return the points values
        return ret

    # Return the distance and direction of a given point
    def GetPoint(self, point):
        # Compute the vectorial distance
        dx = point[0] - self.robot.x
        dy = point[1] - self.robot.y
        # Computes the scalar distance
        dist = np.hypot(dx, dy)
        ang = -np.degrees(np.arctan2(dy, dx))-self.robot.rotate

        # Normalizes angle
        if ang < -180:
            ang += 360

        # Verifies if the angle is inside the field of view
        if -self.hfov <= ang and ang <= self.hfov:
            # 
            f = self.robotheight/np.tan(np.radians(self.headtilt-self.vfov))
            n = self.robotheight/np.tan(np.radians(self.headtilt+self.vfov))

            # Computes point distances
            dn = n/np.cos(np.radians(ang))
            df = f/np.cos(np.radians(ang))

            # Verifies if the distance is in range
            if dn <= dist and dist <= df:
                return np.random.normal(ang, 3)
        return -999

    # Return the measure of all seen goalposts
    def GetGoalPosts(self):
        ret = []
        # For each goal post
        for x in [(70,280), (70,460), (970,280), (970,460)]:
            # Computes the angle
            ret.append(self.GetPoint(x))

        # Sort the angles
        ret.sort(reverse=True)
        return ret

    # Return the position of the ball, maybe
    def GetBall(self):
        dist = hypot(self.robot.x-self.robot.ball.x, self.robot.y-self.robot.ball.y)
        ang = -degrees(atan2(self.robot.ball.y-self.robot.y, self.robot.ball.x-self.robot.x))-self.robot.rotate
        if CompAng(ang, 0, self.fov/2.0):
            return dist, ang
        else:
            return -1, -1

    # Vision Process!
    def VisionProcess(self):
        self.headBehave()
        self.headmotion()
        goals = self.GetGoalPosts()
        dots = self.GetField()
        for x in [('VISION_FIRST_GOALPOST', goals[0]), ('VISION_SECOND_GOALPOST', goals[1]), ('VISION_THIRD_GOALPOST', goals[2]), ('VISION_FOURTH_GOALPOST', goals[3])]:
            self.bkb.write_float(self.Mem, *x)

        self.bkb.write_int(self.Mem, 'VISION_FIELD', write(dots))

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

def write(v):
    x = 0
    for i in range(32):
        x += int(v[i]) << i
    # print v
    return x