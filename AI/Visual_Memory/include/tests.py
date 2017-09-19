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

## Vx = 1  Vy = 0.1  omega = 2
# lista = [
#     {"movement": 1, "target": 1, "pos": [+6.00, +3.00], "time": 0.0,},
##     {"movement": 1, "target": 1, "pos": [+5.55, +2.84], "time": 0.5,},
#     {"movement": 1, "target": 1, "pos": [+5.10, +2.69], "time": 1.0,},
#     {"movement": 1, "target": 1, "pos": [+4.65, +2.53], "time": 1.5,},
#     {"movement": 1, "target": 1, "pos": [+4.19, +2.37], "time": 2.0,},
##     {"movement": 1, "target": 1, "pos": [+3.74, +2.22], "time": 2.5,},
#     {"movement": 1, "target": 1, "pos": [+3.28, +2.06], "time": 3.0,},
#     {"movement": 1, "target": 1, "pos": [+2.82, +1.90], "time": 3.5,},
##     {"movement": 1, "target": 1, "pos": [+2.36, +1.74], "time": 4.0,},
#     {"movement": 1, "target": 1, "pos": [+1.90, +1.57], "time": 4.5,},
#     {"movement": 1, "target": 1, "pos": [+1.43, +1.41], "time": 5.0,},
#     {"movement": 1, "target": 1, "pos": [+0.96, +1.25], "time": 5.5,},
#     {"movement": 1, "target": 1, "pos": [+0.49, +1.09], "time": 6.0,},
##     {"movement": 1, "target": 1, "pos": [+0.02, +0.92], "time": 6.5,},
#     {"movement": 1, "target": 1, "pos": [-0.45, +0.76], "time": 7.0,},
##     {"movement": 1, "target": 1, "pos": [-0.93, +0.59], "time": 7.5,},
# ]

# Vx = 1  Vy = 0.1  omega = 0
lista = [
#     {"movement": 1, "target": 1, "pos": [+6.00, +3.00], "time": 0.0,},
    {"movement": 1, "target": 1, "pos": [+5.50, +2.95], "time": 0.5,},
#     {"movement": 1, "target": 1, "pos": [+5.00, +2.90], "time": 1.0,},
    {"movement": 1, "target": 1, "pos": [+4.50, +2.85], "time": 1.5,},
#     {"movement": 1, "target": 1, "pos": [+4.00, +2.80], "time": 2.0,},
    {"movement": 1, "target": 1, "pos": [+3.50, +2.75], "time": 2.5,},
    {"movement": 1, "target": 1, "pos": [+3.00, +2.70], "time": 3.0,},
    {"movement": 1, "target": 1, "pos": [+2.50, +2.65], "time": 3.5,},
    {"movement": 1, "target": 1, "pos": [+2.00, +2.60], "time": 4.0,},
    {"movement": 1, "target": 1, "pos": [+1.50, +2.55], "time": 4.5,},
#     {"movement": 1, "target": 1, "pos": [+1.00, +2.50], "time": 5.0,},
    {"movement": 1, "target": 1, "pos": [+0.50, +2.45], "time": 5.5,},
    {"movement": 1, "target": 1, "pos": [+0.00, +2.40], "time": 6.0,},
#     {"movement": 1, "target": 1, "pos": [-0.50, +2.35], "time": 6.5,},
    {"movement": 1, "target": 1, "pos": [-1.00, +2.30], "time": 7.0,},
#     {"movement": 1, "target": 1, "pos": [-1.50, +2.25], "time": 7.5,},
]

for x in xrange(len(lista)):
    lista[x]["pos"][0] += -land._parameters["vision_error"] + 2*land._parameters["vision_error"]*random.random()
    lista[x]["pos"][1] += -land._parameters["vision_error"] + 2*land._parameters["vision_error"]*random.random()

vx = 1
vy = 0

for data in lista:
    print data, "\n"
#     land.update(data)
    me.update(land.update(data))
    print land._predictedstate["x"].evalf(3), land._predictedstate["covariance"].evalf(3), "\n"
#     land.predict(tnow=data["time"]+1, movements=data["movement"])
#     print land._predictedstate["x"].evalf(3), land._predictedstate["covariance"].evalf(3), "\n"

land._end( )

print "time", lista[len(lista)-1]["time"]+0.5
land.predict(tnow=lista[len(lista)-1]["time"]+0.5, movements=data["movement"])
print land._predictedstate["x"].evalf(3), land._predictedstate["covariance"].evalf(3), "\n"

me[1]['x_speed']