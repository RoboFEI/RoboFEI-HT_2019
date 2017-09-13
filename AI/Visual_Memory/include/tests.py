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

lista = [
	{"movement": 1, "target": 1, "pos": [14, 0], "time": 1.0,},
	{"movement": 1, "target": 1, "pos": [9.5, 0], "time": 2.0,},
	{"movement": 1, "target": 1, "pos": [6.0, 0], "time": 3.0,},
	{"movement": 1, "target": 1, "pos": [3.5, 0], "time": 4.0,},
	{"movement": 1, "target": 1, "pos": [2.0, 0], "time": 5.0,},
	{"movement": 1, "target": 1, "pos": [1.5, 0], "time": 6.0,},
	{"movement": 1, "target": 1, "pos": [1.5, 0], "time": 7.0,},
	{"movement": 1, "target": 1, "pos": [1.5, 0], "time": 8.0,},
	{"movement": 1, "target": 1, "pos": [1.5, 0], "time": 9.0,},
	{"movement": 1, "target": 1, "pos": [1.5, 0], "time": 10.0,},
]

for x in xrange(len(lista)):
	lista[x]["pos"][0] += -land._parameters["vision_error"] + 2*land._parameters["vision_error"]*random.random()

vx = 1
vy = 0

for data in lista:
	print data, "\n"
	land.update(data)
	print land._predictedstate["x"].evalf(3), land._predictedstate["covariance"].evalf(3), "\n"
	land.predict(tnow=data["time"]+1, movements=data["movement"])
	print land._predictedstate["x"].evalf(3), land._predictedstate["covariance"].evalf(3), "\n"

land._end( )

land.predict(tnow=20.0, movements=data["movement"])
print land._predictedstate["x"].evalf(2), land._predictedstate["covariance"].evalf(2), "\n"