# coding: utf-8

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

        self.headspd = 180 # Max head speed, in degrees per second

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
        self.headtilt += np.sign(self.tiltpos-self.headtilt) * np.min([abs(self.tiltpos-self.headtilt) * self.clk, self.headspd]) / self.clk
        self.headpan += np.sign(self.panpos-self.headpan) * np.min([abs(self.panpos-self.headpan) * self.clk, self.headspd]) / self.clk

        self.headtilt = np.min([self.maxtilt, np.max([self.mintilt, self.headtilt])])
        self.headpan = np.min([self.maxpan, np.max([self.minpan, self.headpan])])

    # Reactive head behavior
    def headBehave(self):
        hp = self.bkb.read_int(self.Mem, 'DECISION_LOCALIZATION')

        if hp == -999:
            self.robot.x, self.robot.y, self.robot.rotate = 130, 540, -135
            self.jump = False

        if hp == -999:
            # y = [90,60,30,0,-30,-60,-90]
            y = [0, 90, 0, -90]
            # y = [0]
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

            f = ((8, 1032), (60, 680))
            # f = ((0, 1040), (0, 740))

            if .3 > np.random.random():
                if 0.5 < np.random.random():
                    ret.append(1) 
                else:
                    ret.append(0)

            # Verify if it is in or out of the field
            elif f[0][0] <= x and x <= f[0][1] and f[1][0] <= y and y <= f[1][1]:
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

    def GetFieldRet(self):
        if self.get:
            self.get = False
            size = 5.
            aux = np.zeros(10)
            for i in xrange(int(size)):
                aux += np.array(self.GetField())
            aux /= size
            abs_aux = np.rint(aux)
            mean_aux = np.mean(np.abs(aux-abs_aux))

            self.bkb.write_int(self.Mem, 'iVISION_FIELD', write(abs_aux))
            
            if self.headpan <= -89:
                hpan = -90 - mean_aux
            elif -1 <= self.headpan and self.headpan <= 1:
                hpan = 0 + mean_aux
            elif 89 <= self.headpan:
                hpan = 90 + mean_aux
            else:
                hpan = 0

            self.bkb.write_float(self.Mem, 'fVISION_FIELD', hpan)

    def GetDist(self):
        if self.get:
            self.get = False
            if self.robot.rotate > 180:
                orient = self.robot.rotate - 360
            else:
                orient = self.robot.rotate

            alpha = np.abs(-orient + self.headpan) # x -> 1040
            beta = np.abs(90 - orient + self.headpan) # y -> 0
            gamma = np.abs(-90 - orient + self.headpan) # y -> 740
            delta = min(np.abs(180 - orient + self.headpan), np.abs(-180 - orient + self.headpan))  # x -> 0
            
            dist = 9999

            if alpha < 90:
                dist = min(dist, (1040-self.robot.x)/np.cos(np.radians(alpha)))
            if beta < 90:
                dist = min(dist, self.robot.y/np.cos(np.radians(beta)))
            if gamma < 90:
                dist = min(dist, (740-self.robot.y)/np.cos(np.radians(gamma)))
            if delta < 90:
                dist = min(dist, self.robot.x/np.cos(np.radians(delta)))
            
            mean_aux = 1./max(self.robot.radius, dist)
            
            if self.headpan <= -89:
                hpan = -90 - mean_aux
            elif -1 <= self.headpan and self.headpan <= 1:
                hpan = 0 + mean_aux
            elif 89 <= self.headpan:
                hpan = 90 + mean_aux
            else:
                hpan = 0
            self.bkb.write_float(self.Mem, 'fVISION_FIELD', hpan)

    # Vision Process!
    jump = True
    change = True
    exp = 0
    save = []
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

        # bhv = self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING')
        # if bhv >= 100 and bhv < 110: # Setup the robot
        #     print 'vision_loc: Setting up experiment!'
        #     self.robot.x = 250
        #     self.robot.y = 670
        #     self.robot.rotate = 90
        #     self.exp = bhv - 100
        #     self.save = []
        #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', bhv+10)

        # if bhv == 200 or bhv == 600:
        #     self.save.append([time.time(), self.robot.x, self.robot.y, self.robot.rotate])

        # if bhv == 600:
        #     print 'vision_loc: Jump!'
        #     self.robot.x = 650
        #     self.robot.y = 670
        #     self.robot.rotate = 90
        #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 200)

        # if bhv >= 300 and bhv < 400:
        #     print 'vision_loc: Saving.'
        #     i = bhv - 300
        #     np.save('/home/aislan/Dropbox/Masters/Dissertação/Experiments/simulated/robot'+str(self.exp * 100 + i), np.array(self.save))
        #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', bhv+100)

        # if bhv == 900:
        #     print 'vision_loc: Finished by the mindcontroller!'
        #     self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 910)
        #     exit()

        self.headBehave()
        self.headmotion()

        self.GetFieldRet()

        # if self.exp == 1:
        #     goals = self.GetGoalPosts()
        #     for x in [('VISION_FIRST_GOALPOST', goals[0]), ('VISION_SECOND_GOALPOST', goals[1]), ('VISION_THIRD_GOALPOST', goals[2]), ('VISION_FOURTH_GOALPOST', goals[3]), ('VISION_PAN_DEG', self.headpan)]:
        #         self.bkb.write_float(self.Mem, *x)
        # elif self.exp == 2:
        #     self.GetFieldRet()
        # else:
        #     self.GetDist()

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
    for i in range(10):
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

v = [(100,-45),
     (200,-45),
     (300,-45),

     (50,0),
     (100,0),
     (200,0),
     (400,0),

     (100,45),
     (200,45),
     (300,45)]
