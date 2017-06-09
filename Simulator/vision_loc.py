import numpy as np
import scipy.special as sp
import os
import ctypes
import pygame
from math import *
import random as rnd
from screen import *
import time

class VISION():
    #----------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, robot, clk=30.):
        self.robot = robot # Saves the robot object's address
        # print self.robot.x, self.robot.y
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

        self.behave = 0

        self.get = True

        self.dots = []

        self.text = ""
        self.index = 0
        self.count = -1

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
        hp = self.bkb.read_int(self.Mem, 'DECISION_LOCALIZATION')

        if hp == -999:
            y = [90,60,30,0,-30,-60,-90]
            x = y[self.behave]
            self.pan(pos=x)

            if np.abs(self.headpan-x) < 1:
                self.behave = (self.behave + 1) % len(y)
                self.get = True
        elif hp == 999:
            pass
        else:
            self.pan(pos=hp)

            if np.abs(self.headpan-hp) < 1:
                self.get = True
                self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', 999)

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

        # Draw dots
        for p in self.dots:
            pygame.draw.circle(where, (0,0,0), p, 2, 0)            

    # Return the observed integral of the world
    def Field(self):
        vec = np.array(self.RndGenerate()).transpose() # Takes the random generated angles
        left = 0 # Counts how many dots are green
        right = 0

        total = 0
        
        h = self.robotheight + np.random.normal(0,1) # Adds error to the robot's height
        pan = np.radians(self.headpan + np.random.normal(0, 1)) # Adds error to the horizontal angles
        tilt = np.radians(self.headtilt + np.random.normal(0,1)) # Adds error to the vertical angles

        self.dots = []

        for i in vec:
            dist = (h / np.tan(tilt + i[0]))/np.cos(i[1]) # Computes the point distance
            ang = - np.radians(self.robot.rotate) + i[1] + pan # Computes the point angle
            px = self.robot.x + dist * np.cos(ang) # Computes point x position
            py = self.robot.y + dist * np.sin(ang) # Computes point y position

            self.dots.append((int(px),int(py))) # Saves dots to be seen on simulator's screen
            
            if 0 <= px and px <= 1040 and 0 <= py and py <= 740 and np.random.random() > 0.05:
                # If the dot is "green", save it.
                if total < 1000:
                    left += 1
                else:
                    right += 1
            total += 1

        return 1000 * max(1, min(999, left)) + max(1, min(999, right))

    # Generates random points and returns their angles in radians
    def RndGenerate(self):
        # Fixed to 2000 points
        vrnd = np.random.random([2000])
        hrnd = np.random.random([2000])
        a = -np.arctan((0.7+0.2*hrnd[:1000]) * np.tan(np.radians(self.hfov)))
        b = np.arctan((0.7+0.2*hrnd[1000:]) * np.tan(np.radians(self.hfov)))
        hp = np.concatenate((a, b))

        vp = np.arctan(1/((0.9*vrnd+0.05)*(1/np.tan(np.radians(17.4-self.vfov))-1/np.tan(np.radians(17.4+self.vfov)))+1/np.tan(np.radians(17.4+self.vfov))))-np.radians(17.4)
        # Computes and returns the random generated angles
        return vp, hp

    # Return the distance and direction of a given point
    def GetPoint(self, point):
        # Compute the vectorial distance
        dx = point[0] - self.robot.x
        dy = self.robot.y - point[1]
        
        # Computes the scalar distance
        dist = np.hypot(dx, dy)
        ang = np.degrees(np.arctan2(dy, dx))-self.robot.rotate

        # Normalizes angle
        if ang < -180:
            ang += 360
        elif ang > 180:
            ang -= 360

        # Verifies if the angle is inside the field of view
        if -self.hfov-self.headpan <= ang and ang <= self.hfov-self.headpan:
            # 
            f = self.robotheight/np.tan(np.radians(self.headtilt-self.vfov))
            n = self.robotheight/np.tan(np.radians(self.headtilt+self.vfov))

            # Computes point distances
            dn = n/np.cos(np.radians(ang+self.headpan))
            df = f/np.cos(np.radians(ang+self.headpan))

            # Verifies if the distance is in range
            if (1 + sp.erf((min(df,700)-dist)/(np.sqrt(2)*10))) * (1 - sp.erf((max(10,dn)-dist)/(np.sqrt(2)*1))) / 4 >= np.random.random():
                return np.random.normal(ang, 1)
        return -999

    # Return the measure of all seen goalposts
    def GetGoalPosts(self):
        ret = []
        # For each goal post

        for x in [(70,280), (70,460), (970,280), (970,460)]: # (520,370) field center
            # Computes the angle
            ret.append(self.GetPoint(x))
            # exit()

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
        # self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', -999)

        if self.count == 0:
            self.text += str(time.time()) + " " + str(self.robot.x) + " " + str(self.robot.y) + " " + str(self.robot.rotate) + "\n"
            self.count = 20
        else:
            self.count -= 1

        bhv = self.bkb.read_int(self.Mem, 'VISION_WORKING')
        if bhv == 10101:
            self.robot.x = 200
            self.robot.y = 670
            self.robot.rotate = 90
            self.count = 0
            self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 11100)
            self.bkb.write_int(self.Mem, 'VISION_WORKING', 0)
        elif bhv == 10102:
            self.robot.x = 70
            self.robot.y = 500
            self.robot.rotate = 0
            self.count = 0
            self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 11100)
            self.bkb.write_int(self.Mem, 'VISION_WORKING', 0)
        elif bhv == 11011:
            self.index += 1
            with open('/home/fei/Dropbox/Masters/Experiment/robot'+str(self.index), 'w') as file:
                file.write(self.text)
            self.text = ""
            self.count = -1
            self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 11110)
            self.bkb.write_int(self.Mem, 'VISION_WORKING', 0)
        elif bhv == 11111:
            exit()

        self.headBehave()
        self.headmotion()
        goals = self.GetGoalPosts()

        if self.get:
            self.get = False
            if self.panpos < 0:
                self.bkb.write_int(self.Mem, 'VISION_FIELD', int(1000000 * self.panpos - self.Field()))
            else:
                self.bkb.write_int(self.Mem, 'VISION_FIELD', int(1000000 * self.panpos + self.Field()))
        
        for x in [('VISION_FIRST_GOALPOST', goals[0]), ('VISION_SECOND_GOALPOST', goals[1]), ('VISION_THIRD_GOALPOST', goals[2]), ('VISION_FOURTH_GOALPOST', goals[3]), ('VISION_PAN_DEG', self.headpan)]:
            self.bkb.write_float(self.Mem, *x)

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