# coding: utf-8

# ini-iPython

## Executando no diretório principal

import os
os.chdir('/home/vinicius/Dropbox/Projeto Mestrado/Codigos/RoboFEI-HT_Debug/AI/Visual_Memory') #Executando na pasta Visual_Memory
import sys
sys.path.append('./include')
sys.path.append('./src')
sys.path.append('./iPython')
# end-iPython

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the vision system.

# Used class developed by RoboFEI-HT.
from Landmark import *
from Robots import *

me = Speeds( )
land = Landmark(me)
rob = Robots(me)

import random
random.seed(time.time())

## Vx = 1  Vy = 0.1  omega = 0
# lista = [
#     [{"movement": 1, "pos": [+6.00, +3.00], "time": 0.0,}, {"movement": 1, "pos": [+7.00, +0.00], "time": 0.0,}],
#     [{"movement": 1, "pos": [+5.50, +2.95], "time": 0.5,}, {"movement": 1, "pos": [+6.50, -0.05], "time": 0.5,}],
#     [{"movement": 1, "pos": [+5.00, +2.90], "time": 1.0,}, {"movement": 1, "pos": [+6.00, -0.10], "time": 1.0,}],
#     [{"movement": 1, "pos": [+4.50, +2.85], "time": 1.5,}, {"movement": 1, "pos": [+5.50, -0.15], "time": 1.5,}],
#     [{"movement": 1, "pos": [+4.00, +2.80], "time": 2.0,}, {"movement": 1, "pos": [+5.00, -0.20], "time": 2.0,}],
#     [{"movement": 1, "pos": [+3.50, +2.75], "time": 2.5,}, {"movement": 1, "pos": [+4.50, -0.25], "time": 2.5,}],
#     [{"movement": 1, "pos": [+3.00, +2.70], "time": 3.0,}, {"movement": 1, "pos": [+4.00, -0.30], "time": 3.0,}],
#     [{"movement": 1, "pos": [+2.50, +2.65], "time": 3.5,}, {"movement": 1, "pos": [+3.50, -0.35], "time": 3.5,}],
#     [{"movement": 1, "pos": [+2.00, +2.60], "time": 4.0,}, {"movement": 1, "pos": [+3.00, -0.40], "time": 4.0,}],
#     [{"movement": 1, "pos": [+1.50, +2.55], "time": 4.5,}, {"movement": 1, "pos": [+2.50, -0.45], "time": 4.5,}],
#     [{"movement": 1, "pos": [+1.00, +2.50], "time": 5.0,}, {"movement": 1, "pos": [+2.00, -0.50], "time": 5.0,}],
#     [{"movement": 1, "pos": [+0.50, +2.45], "time": 5.5,}, {"movement": 1, "pos": [+1.50, -0.55], "time": 5.5,}],
#     [{"movement": 1, "pos": [+0.00, +2.40], "time": 6.0,}, {"movement": 1, "pos": [+1.00, -0.60], "time": 6.0,}],
#     [{"movement": 1, "pos": [-0.50, +2.35], "time": 6.5,}, {"movement": 1, "pos": [+0.50, -0.65], "time": 6.5,}],
#     [{"movement": 1, "pos": [-1.00, +2.30], "time": 7.0,}, {"movement": 1, "pos": [+0.00, -0.70], "time": 7.0,}],
#     [{"movement": 1, "pos": [-1.50, +2.25], "time": 7.5,}, {"movement": 1, "pos": [-0.50, -0.75], "time": 7.5,}],
# ]

## Vx = 1  Vy = 0 omega = 0  vox = 1 voy = 1
# lista = [
#     [{"movement": 1, "pos": [+6.00, +3.00], "time": 0.0,}, {"movement": 1, "pos": [+7.00, +0.00], "time": 0.0,}],
#     [{"movement": 1, "pos": [+5.50, +3.00], "time": 0.5,}, {"movement": 1, "pos": [+7.00, -0.50], "time": 0.5,}],
#     [{"movement": 1, "pos": [+5.00, +3.00], "time": 1.0,}, {"movement": 1, "pos": [+7.00, -1.00], "time": 1.0,}],
#     [{"movement": 1, "pos": [+4.50, +3.00], "time": 1.5,}, {"movement": 1, "pos": [+7.00, -1.50], "time": 1.5,}],
#     [{"movement": 1, "pos": [+4.00, +3.00], "time": 2.0,}, {"movement": 1, "pos": [+7.00, -2.00], "time": 2.0,}],
#     [{"movement": 1, "pos": [+3.50, +3.00], "time": 2.5,}, {"movement": 1, "pos": [+7.00, -2.50], "time": 2.5,}],
#     [{"movement": 1, "pos": [+3.00, +3.00], "time": 3.0,}, {"movement": 1, "pos": [+7.00, -3.00], "time": 3.0,}],
#     [{"movement": 1, "pos": [+2.50, +3.00], "time": 3.5,}, {"movement": 1, "pos": [+7.00, -3.50], "time": 3.5,}],
#     [{"movement": 1, "pos": [+2.00, +3.00], "time": 4.0,}, {"movement": 1, "pos": [+7.00, -4.00], "time": 4.0,}],
#     [{"movement": 1, "pos": [+1.50, +3.00], "time": 4.5,}, {"movement": 1, "pos": [+7.00, -4.50], "time": 4.5,}],
#     [{"movement": 1, "pos": [+1.00, +3.00], "time": 5.0,}, {"movement": 1, "pos": [+7.00, -5.00], "time": 5.0,}],
#     [{"movement": 1, "pos": [+0.50, +3.00], "time": 5.5,}, {"movement": 1, "pos": [+7.00, -5.50], "time": 5.5,}],
#     [{"movement": 1, "pos": [+0.00, +3.00], "time": 6.0,}, {"movement": 1, "pos": [+7.00, -6.00], "time": 6.0,}],
#     [{"movement": 1, "pos": [-0.50, +3.00], "time": 6.5,}, {"movement": 1, "pos": [+7.00, -6.50], "time": 6.5,}],
#     [{"movement": 1, "pos": [-1.00, +3.00], "time": 7.0,}, {"movement": 1, "pos": [+7.00, -7.00], "time": 7.0,}],
#     [{"movement": 1, "pos": [-1.50, +3.00], "time": 7.5,}, {"movement": 1, "pos": [+7.00, -7.50], "time": 7.5,}],
# ]

## Vx = 1  Vy = 0.1 omega = 2  vox = 1 voy = 1
# lista = [
#     [{"movement": 1, "pos": [+6.00, +3.00], "time": 0.0,}, {"movement": 1, "pos": [+7.00, +0.00], "time": 0.0,}],
#     [{"movement": 1, "pos": [+5.55, +2.84], "time": 0.5,}, {"movement": 1, "pos": [+7.01, +0.32], "time": 0.5,}],
#     [{"movement": 1, "pos": [+5.10, +2.69], "time": 1.0,}, {"movement": 1, "pos": [+7.03, +0.63], "time": 1.0,}],
#     [{"movement": 1, "pos": [+4.65, +2.53], "time": 1.5,}, {"movement": 1, "pos": [+7.07, +0.90], "time": 1.5,}],
#     [{"movement": 1, "pos": [+4.19, +2.37], "time": 2.0,}, {"movement": 1, "pos": [+7.12, +1.17], "time": 2.0,}],
#     [{"movement": 1, "pos": [+3.74, +2.22], "time": 2.5,}, {"movement": 1, "pos": [+7.18, +1.41], "time": 2.5,}],
#     [{"movement": 1, "pos": [+3.28, +2.06], "time": 3.0,}, {"movement": 1, "pos": [+7.26, +1.64], "time": 3.0,}],
#     [{"movement": 1, "pos": [+2.82, +1.90], "time": 3.5,}, {"movement": 1, "pos": [+7.35, +1.84], "time": 3.5,}],
#     [{"movement": 1, "pos": [+2.36, +1.74], "time": 4.0,}, {"movement": 1, "pos": [+7.45, +2.03], "time": 4.0,}],
#     [{"movement": 1, "pos": [+1.90, +1.57], "time": 4.5,}, {"movement": 1, "pos": [+7.56, +2.20], "time": 4.5,}],
#     [{"movement": 1, "pos": [+1.43, +1.41], "time": 5.0,}, {"movement": 1, "pos": [+7.69, +1.43], "time": 5.0,}],
#     [{"movement": 1, "pos": [+0.96, +1.25], "time": 5.5,}, {"movement": 1, "pos": [+7.82, +2.46], "time": 5.5,}],
#     [{"movement": 1, "pos": [+0.49, +1.09], "time": 6.0,}, {"movement": 1, "pos": [+7.96, +2.57], "time": 6.0,}],
# ]

# Vx = 1  Vy = 0.1 omega = 22.5°  vox = 1 voy = 1
lista = [
    [{"movement": 1, "pos": [+6.00, +3.00], "time": 0.0,}, {"movement": 1, "pos": [+7.00, +0.00], "time": 0.0,}],
    [{"movement": 1, "pos": [+5.97, +1.72], "time": 0.5,}, {"movement": 1, "pos": [+6.95, +1.02], "time": 0.5,}],
    [{"movement": 1, "pos": [+5.69, +0.38], "time": 1.0,}, {"movement": 1, "pos": [+6.77, -2.24], "time": 1.0,}],
    [{"movement": 1, "pos": [+5.16, -0.99], "time": 1.5,}, {"movement": 1, "pos": [+6.40, -3.63], "time": 1.5,}],
    [{"movement": 1, "pos": [+4.36, -2.32], "time": 2.0,}, {"movement": 1, "pos": [+5.78, -5.15], "time": 2.0,}],
    [{"movement": 1, "pos": [+3.33, -3.57], "time": 2.5,}, {"movement": 1, "pos": [+4.86, -6.76], "time": 2.5,}],
    [{"movement": 1, "pos": [+2.07, -4.70], "time": 3.0,}, {"movement": 1, "pos": [+3.60, -8.39], "time": 3.0,}],
    [{"movement": 1, "pos": [+0.61, -5.65], "time": 3.5,}, {"movement": 1, "pos": [+1.98, -9.97], "time": 3.5,}],
    [{"movement": 1, "pos": [-1.00, -6.40], "time": 4.0,}, {"movement": 1, "pos": [+0.00, -11.4], "time": 4.0,}],
]

for x in xrange(len(lista)-1):
    lista[x][0]["pos"][0] += -land._parameters["vision_error"] + 2*land._parameters["vision_error"]*random.random()
    lista[x][0]["pos"][1] += -land._parameters["vision_error"] + 2*land._parameters["vision_error"]*random.random()
    
    lista[x][1]["pos"][0] += -land._parameters["vision_error"] + 2*land._parameters["vision_error"]*random.random()
    lista[x][1]["pos"][1] += -land._parameters["vision_error"] + 2*land._parameters["vision_error"]*random.random()

for dataland, datarob in lista[:-1]:
#     print dataland, "\n"
    me.update(land.update(dataland))
#     print land._predictedstate["x"].evalf(3), land._predictedstate["covariance"].evalf(3), "\n"
    
    print datarob, "\n"
    rob.update(datarob)
    print rob._predictedstate["x"].evalf(3), rob._predictedstate["covariance"].evalf(3), "\n"

land._end( )
rob._end( )

print "Data:", lista[len(lista)-1][1]
rob.predict(lista[len(lista)-1][1]["time"], lista[len(lista)-1][1]["movement"])
print rob._predictedstate["x"].evalf(3), rob._predictedstate["covariance"].evalf(3), "\n"

me[1]['x_speed']

me[1]['R'].evalf(3)