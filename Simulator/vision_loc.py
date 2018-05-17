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
        self.headpan = -90 # Pan position
        self.panpos = 0 # Chosen pan position

        self.maxtilt = 64 # Max tilt
        self.mintilt = 16 # Min tilt
        self.maxpan = 90 # Max pan
        self.minpan = -90 # Min pan

        self.headspd = 90 # Max head speed, in degrees per second

        # Observation points
        self.vpoints = v

        self.behave = 0

        self.get = False

        self.text = ""
        self.index = 0
        self.count = -1

        self.timestamp = 0

        # self.robot.x = 350
        # self.robot.y = 350
        # self.robot.rotate = 0

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
            # y = [90,60,30,0,-30,-60,-90]
            # y = [90, 0, -90, 0]
            y = [0]
            x = y[self.behave]
            self.pan(pos=x)

            if np.abs(self.headpan-x) < 1:
                self.behave = (self.behave + 1) % len(y)
                if time.time() - self.timestamp >= 1:
                    self.get = True
                    self.timestamp = time.time()
        else:
            if hp != 999:
                self.pan(pos=hp)

            if np.abs(self.headpan-hp) < 1:
                self.get = True
                self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', 999)

    # Draw the field of view of the robot
    def draw(self, where):
        # # Computes distances
        # f = self.robotheight/np.tan(np.radians(self.headtilt-self.vfov))
        # n = self.robotheight/np.tan(np.radians(self.headtilt+self.vfov))

        # # Computes point distances
        # dn = n/np.cos(np.radians(self.hfov))
        # df = f/np.cos(np.radians(self.hfov))

        # # Array of points
        # points = []

        # # Create points
        # for d in [dn, df]:
        #     for a in [self.hfov, -self.hfov]:
        #         x = self.robot.x + d * np.cos(np.radians(-self.robot.rotate + self.headpan + a))
        #         y = self.robot.y + d * np.sin(np.radians(-self.robot.rotate + self.headpan + a))
        #         points.append((x,y))

        # # Draw the points
        # for a in [0, 3]:    
        #     for b in [1, 2]:
        #         pygame.draw.line(where, (255,255,255), points[a], points[b], 1)

        for point in v:
            # Compute the point 

            dist = point[0] #+ np.random.normal(0,point[0][0]/10.)
            # Compute the direction of the point
            angle = -self.robot.rotate + self.headpan + point[1] #+ np.random.normal(0,2)

            # Compute the position in the world of the point
            x = self.robot.x + dist * np.cos(np.radians(angle)) #+ np.random.normal(0,1)
            y = self.robot.y + dist * np.sin(np.radians(angle)) #+ np.random.normal(0,1)

            pygame.draw.circle(where, self.robot.color, (int(x),int(y)), 2, 0)
            # pygame.draw.circle(where, (0,0,0), (int(x),int(y)), 2, 0)

        pass

    # Return the notable variables for localization, as a vector
    def GetField(self):
        ret = []

        # For each point
        for point in self.vpoints:
            # Compute the point distance
            dist = point[0] + np.random.normal(0,point[0]/10.)
            # Compute the direction of the point
            angle = -self.robot.rotate + self.headpan + point[1] + np.random.normal(0,2)

            # Compute the position in the world of the point
            x = self.robot.x + dist * np.cos(np.radians(angle)) + np.random.normal(0,1)
            y = self.robot.y + dist * np.sin(np.radians(angle)) + np.random.normal(0,1)

            if .3 > np.random.random():
                if 0.5 < np.random.random():
                    ret.append(1) 
                else:
                    ret.append(0)

            # Verify if it is in or out of the field
            elif 0 <= x and x <= 1040 and 0 <= y and y <= 740:
                ret.append(1)
            else:
                ret.append(0)
                
        # Return the points values
        return ret

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
    jump = True
    change = True
    def VisionProcess(self):
        # if time.time() % 60 < 1:
        #     if self.jump:
        #         self.robot.x = np.random.randint(70, 970)
        #         self.robot.y = np.random.randint(70, 670)
        #         self.robot.rotate = np.random.randint(-180, 180)
        #         self.jump = False
        # else:
        #     self.jump = True

        # if time.time() % 13 < 1:
        #     if self.change:
        #         self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', [11, 1, 0, 8, 11, 17, 0, 18, 11, 6, 0, 7, 11, 2, 0, 3, 11, 9, 0, 14][np.random.randint(12)])
        #         self.change = False
        # else:
        #     self.change = True

        # if self.count == 0:
        #     self.text += str(time.time()) + " " + str(self.robot.x) + " " + str(self.robot.y) + " " + str(self.robot.rotate) + "\n"
        #     self.count = 20
        # else:
        #     self.count -= 1

        # bhv = self.bkb.read_int(self.Mem, 'VISION_WORKING')
        # if bhv == 10101:
        #     self.robot.x = 200
        #     self.robot.y = 670
        #     self.robot.rotate = 90
        #     self.count = 0
        #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 11100)
        #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 0)
        # elif bhv == 10102:
        #     self.robot.x = 70
        #     self.robot.y = 500
        #     self.robot.rotate = 0
        #     self.count = 0
        #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 11100)
        #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 0)
        # elif bhv == 11011:
        #     self.index += 1
        #     with open('/home/fei/Dropbox/Masters/Experiment/robot'+str(self.index), 'w') as file:
        #         file.write(self.text)
        #     self.text = ""
        #     self.count = -1
        #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 11110)
        #     self.bkb.write_int(self.Mem, 'VISION_WORKING', 0)
        # elif bhv == 11111:
        #     exit()

        self.headBehave()
        self.headmotion()
        # goals = self.GetGoalPosts()
        # dots = self.GetField()

        if self.get:
            self.get = False
            size = 5.
            aux = np.zeros(32)
            for i in xrange(int(size)):
                aux += np.array(self.GetField())
            aux /= size
            abs_aux = np.rint(aux)
            mean_aux = np.mean(np.abs(aux-abs_aux))

            self.bkb.write_int(self.Mem, 'iVISION_FIELD', write(abs_aux))
            
            if self.headpan <= -89:
                hpan = -90 - mean_aux
            elif -61 <= self.headpan and self.headpan <= -59:
                hpan = -60 - mean_aux
            elif -31 <= self.headpan and self.headpan <= -29:
                hpan = -30 - mean_aux
            elif -1 <= self.headpan and self.headpan <= 1:
                hpan = 0 + mean_aux
            elif 29 <= self.headpan and self.headpan <= 31:
                hpan = 30 + mean_aux
            elif 59 <= self.headpan and self.headpan <= 61:
                hpan = 60 + mean_aux
            elif 89 <= self.headpan:
                hpan = 90 + mean_aux

            self.bkb.write_float(self.Mem, 'fVISION_FIELD', hpan)

        # if sum(dots) != 0:
            # self.bkb.write_int(self.Mem, 'iVISION_FIELD', write(dots))

        # for x in [('VISION_FIRST_GOALPOST', goals[0]), ('VISION_SECOND_GOALPOST', goals[1]), ('VISION_THIRD_GOALPOST', goals[2]), ('VISION_FOURTH_GOALPOST', goals[3]), ('VISION_PAN_DEG', self.headpan)]:
            # self.bkb.write_float(self.Mem, *x)

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

import numpy as np

def fun(dist, ang):
    c = dist * np.cos(np.radians(ang))

    v = np.degrees(np.arctan(50./c)) - 17.4

    return ang, v

def points(v):
    ret = []

    for x in v:
        ret.append(fun(*x))

    return ret

v = [(1,0),
     (9999999,0),

     (100,-45),
     (200,-45),
     (300,-45),

     (70,-30),
     (140,-30),
     (300,-30),
     (530,-30),

     (80,-20),
     (180,-20),
     (420,-20),

     (90,-10),
     (150,-10),
     (300,-10),

     (50,0),
     (100,0),
     (200,0),
     (500,0),

     (90,10),
     (150,10),
     (300,10),

     (80,20),
     (190,20),
     (430,20),

     (70,30),
     (140,30),
     (300,30),
     (530,30),

     (100,45),
     (200,45),
     (300,45)]
