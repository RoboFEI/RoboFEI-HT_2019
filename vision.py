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
        field_of_view = 100
        vision_dist = 200  #we need to add as global variavel

        d = self.distD(r_x,r_y,x,y)
        r = self.distR(r_x,r_y,x,y)

        d=random.gauss(d,0.1*d/10)

        if((d < vision_dist) and self.compAng(r,rotate)):
            print 'Inside'
            print 'Distance ',d
            print 'Rotate ',-r
            bkb.write_float(mem,'VISION_DIST_BALL',d)
            bkb.write_float(mem,'VISION_ANGLE_BALL',-r)
            #bkb.write_int('VISION_SEARCH_BALL',0)
            return -r
        #else:
            #print 'Outside'


    def detect(self):
        self.view_obj(self,x,y,view_rot)



