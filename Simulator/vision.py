import numpy as np
import os
import ctypes
from math import *
import random
from screen import *

class Vision():

    #----------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self.max_angle = False
        self.pan_right = True
        self.pan_left = False

        #Camera
        self.field_of_view = 101.75
        self.vision_dist = 300 #300 cm


    def view_left(self,view_rot,rotate,angle):
        view_rot = (view_rot+angle) % 360
        diff = abs(rotate-view_rot) % 360
        if (diff > 90) and (diff<270):
            view_rot = (view_rot-angle) % 360
            self.max_angle = True
            self.pan_right = True
            self.pan_left = False
            #print view_rot
        return view_rot

    def view_right(self,view_rot,rotate,angle):
        view_rot = (view_rot-angle) % 360
        diff = abs(rotate-view_rot)%360
        if (diff > 90) and (diff<270):
            view_rot = (view_rot+angle) % 360
            self.max_angle = True
            self.pan_right = False
            self.pan_left = True
            #print view_rot
        return view_rot


    def pan(self,view_rot,rotate):
        if self.pan_right == True:
            view_rot = self.view_right(view_rot,rotate,1)
        elif self.pan_left == True:
            view_rot = self.view_left(view_rot,rotate,1)
        return view_rot


    def hcc(self,x1,y1,x2,y2):
        return sqrt((x1-x2)**2 + (y1-y2)**2)


    def distD(self, x1, y1, x2, y2):
        return self.hcc(x1, y1, x2, y2)

    def distR(self, x1, y1, x2, y2):
        return atan2((y2-y1), (x2-x1))*180/pi
        # atan2 retorna angulo entre -pi e +pi

    def compAng(self, ang, base):
        angrange = 35
        base = -base
        if(base > 180-angrange or base < -180+angrange):
            if(ang > 0 and base < 0):
                return (ang < base + 360 + angrange) and (ang > base + 360 - angrange)
            elif (ang < 0 and base > 0):
                return (ang < base - 360 + angrange) and (ang > base - 360 - angrange)
        return (ang < base + angrange) and (ang > base - angrange)


    def view_obj(self,mem,bkb,r_x,r_y,x,y,rotate):

        d = self.distD(r_x,r_y,x,y)
        r = self.distR(r_x,r_y,x,y)

        #d=random.gauss(d,0.1*d/10)

        if((d < self.vision_dist) and self.compAng(r,rotate)):
            #print 'Inside'
            #print 'Distance ',d
            #print 'Rotate ',-r
            return (-r,d)
        else:
            #print 'Outside'
            return ("NF", "NF")  # Not Found

    def ball_detect(self, mem, bkb, view_rot, rotate, rX, rY, ballX, ballY):
        # if bkb.read_int(mem, 'VISION_BALL_CENTERED') == 0:  # and self.bkb.read_int(self.Mem, 'VISION_BALL_LOST') == 1
        #    view_rot = self.pan(view_rot,rotate)
        rot, dist = self.view_obj(mem, bkb, rX, rY, ballX, ballY, view_rot)
        if rot != "NF":
            bkb.write_int(mem, 'VISION_BALL_LOST', 0)  # ball is found
            if rotate > 180 and rotate < 360:
                rotate = rotate - 360
            rot = rot - rotate

            if rot > 180:
                rot = rot - 360

            elif rot < -180:
                rot = rot + 360

            ball_orient_wrt_robot = rot

            if rot > 90:
                rot = 90
            elif rot < -90:
                rot = -90
            view_rot_aux = rot + rotate

            # print 'ball_for_robot', ball_orient_wrt_robot
            # print 'view_rot_aux', int(view_rot_aux) % 360
            # print 'view_rot', int(view_rot)

            if (int(view_rot_aux) % 360) >= int(view_rot) - 1 and (int(view_rot_aux) % 360) <= int(view_rot) + 1:
                bkb.write_int(mem, 'VISION_BALL_PAN_ON', 0)  # stop searching
                bkb.write_float(mem, 'VISION_BALL_DIST', dist)
                bkb.write_float(mem, 'VISION_PAN_DEG', ball_orient_wrt_robot)
                return view_rot_aux
            else:
                bkb.write_int(mem, 'VISION_BALL_PAN_ON', 1)  # searching

        else:
            bkb.write_int(mem, 'VISION_BALL_LOST', 1)  # ball is lost


    def write_bkb_robot_position(self,mem,bkb,rot,dist,robotID):
        bkb.write_floatDynamic(mem,'VISION_RBT01_DIST',robotID,dist)
        bkb.write_floatDynamic(mem,'VISION_RBT01_ANGLE',robotID,-rot)



    def robot_detect(self,mem,bkb,view_rot, rotate, rX, rY, robotX, robotY,robotID,selfID):
#        if bkb.read_int(mem,'VISION_SEARCH_BALL')== 1:
        view_rot = self.pan(view_rot,rotate)
        rot, dist = self.view_obj(mem,bkb,rX,rY,robotX,robotY,view_rot)
        if rot != "NF":
            #print 'Robot B', selfID, 'found robot: ', robotID+1
            self.write_bkb_robot_position(mem,bkb,rot,dist,robotID)