# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the vision system.

# Used class developed by RoboFEI-HT.
from Landmark import *

me = Speeds( )
land = Landmark(me)

import random
random.seed(time.time())

# Vx = 1.4  Vy = -0.1  omega = 5
lista = [
    {"movement": 1, "target": 1, "pos": [+6.00, -1.00], "time": 0.0,},
    {"movement": 1, "target": 1, "pos": [+5.63, -1.11], "time": 0.25,},
    {"movement": 1, "target": 1, "pos": [+5.25, -1.21], "time": 0.5,},
    {"movement": 1, "target": 1, "pos": [+4.87, -1.32], "time": 0.75,},
    {"movement": 1, "target": 1, "pos": [+4.49, -1.42], "time": 1.0,},
    {"movement": 1, "target": 1, "pos": [+4.11, -1.52], "time": 1.25,},
    {"movement": 1, "target": 1, "pos": [+3.72, -1.62], "time": 1.5,},
    {"movement": 1, "target": 1, "pos": [+3.33, -1.73], "time": 1.75,},
    {"movement": 1, "target": 1, "pos": [+2.94, -1.83], "time": 2.0,},
    {"movement": 1, "target": 1, "pos": [+2.54, -1.93], "time": 2.25,},
    {"movement": 1, "target": 1, "pos": [+2.14, -2.02], "time": 2.5,},
    {"movement": 1, "target": 1, "pos": [+1.74, -2.12], "time": 2.75,},
    {"movement": 1, "target": 1, "pos": [+1.34, -2.22], "time": 3.0,},
    {"movement": 1, "target": 1, "pos": [+0.52, -2.41], "time": 3.5,},
]

for x in xrange(len(lista)):
    lista[x]["pos"][0] += -land._parameters["vision_error"] + 2*land._parameters["vision_error"]*random.random()
    lista[x]["pos"][1] += -land._parameters["vision_error"] + 2*land._parameters["vision_error"]*random.random()

vx = 1
vy = 0

for data in lista:
    print data, "\n"
    me.update(land.update(data))
    print land._predictedstate["x"].evalf(3), land._predictedstate["covariance"].evalf(3), "\n"
#     land.predict(tnow=data["time"]+1, movements=data["movement"])
#     print land._predictedstate["x"].evalf(3), land._predictedstate["covariance"].evalf(3), "\n"

land._end( )

land.predict(tnow=lista[len(lista)-1]["time"]+2.5, movements=data["movement"])
print land._predictedstate["x"].evalf(3), land._predictedstate["covariance"].evalf(3), "\n"

me[1]['x_speed']