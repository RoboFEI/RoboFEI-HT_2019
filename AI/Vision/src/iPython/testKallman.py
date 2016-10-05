# coding: utf-8
# %pylab inline
import sys
# import os
# from cv2 import __version__
# print "OpenCV ", __version__
# import cv2
from sympy import *
# import pandas as pd
# import numpy as np

init_printing()
reload(sys)  
sys.setdefaultencoding('utf8')

# Matriz de translação
t0 = Symbol('t0')
t1 = Symbol('t1')
t2 = Symbol('t2')

x0 = Symbol('x0')
x1 = Symbol('x1')
x2 = Symbol('x2')

v0 = Symbol('v0')
v1 = Symbol('v1')
v2 = Symbol('v2')

a0 = Symbol('a0')
a1 = Symbol('a1')
a2 = Symbol('a2')

v1 = (x1-x0)/(t1-t0)
v2 = (x2-x1)/(t2-t1)
v1, v2

a2 = (v2-v1)/(t2-t1)
simplify(a2)

xt = Symbol('x_t')
vt = Symbol('v_t')
t = Symbol('t')
a = Symbol('a')
xt1 = xt + v0t*t + 0.5*a*pow(t,2)
xt1



