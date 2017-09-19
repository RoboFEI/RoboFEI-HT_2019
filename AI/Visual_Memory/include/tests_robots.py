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

# Vx = 1  Vy = 0.1  omega = 0
lista = [
    [{"movement": 1, "pos": [+6.00, +3.00], "time": 0.0,}, {"movement": 1, "pos": [+7.00, +0.00], "time": 0.0,}],
    [{"movement": 1, "pos": [+5.50, +2.95], "time": 0.5,}, {"movement": 1, "pos": [+6.50, -0.05], "time": 0.5,}],
    [{"movement": 1, "pos": [+5.00, +2.90], "time": 1.0,}, {"movement": 1, "pos": [+6.00, -0.10], "time": 1.0,}],
    [{"movement": 1, "pos": [+4.50, +2.85], "time": 1.5,}, {"movement": 1, "pos": [+5.50, -0.15], "time": 1.5,}],
    [{"movement": 1, "pos": [+4.00, +2.80], "time": 2.0,}, {"movement": 1, "pos": [+5.00, -0.20], "time": 2.0,}],
    [{"movement": 1, "pos": [+3.50, +2.75], "time": 2.5,}, {"movement": 1, "pos": [+4.50, -0.25], "time": 2.5,}],
    [{"movement": 1, "pos": [+3.00, +2.70], "time": 3.0,}, {"movement": 1, "pos": [+4.00, -0.30], "time": 3.0,}],
    [{"movement": 1, "pos": [+2.50, +2.65], "time": 3.5,}, {"movement": 1, "pos": [+3.50, -0.35], "time": 3.5,}],
    [{"movement": 1, "pos": [+2.00, +2.60], "time": 4.0,}, {"movement": 1, "pos": [+3.00, -0.40], "time": 4.0,}],
    [{"movement": 1, "pos": [+1.50, +2.55], "time": 4.5,}, {"movement": 1, "pos": [+2.50, -0.45], "time": 4.5,}],
    [{"movement": 1, "pos": [+1.00, +2.50], "time": 5.0,}, {"movement": 1, "pos": [+2.00, -0.50], "time": 5.0,}],
    [{"movement": 1, "pos": [+0.50, +2.45], "time": 5.5,}, {"movement": 1, "pos": [+1.50, -0.55], "time": 5.5,}],
    [{"movement": 1, "pos": [+0.00, +2.40], "time": 6.0,}, {"movement": 1, "pos": [+1.00, -0.60], "time": 6.0,}],
    [{"movement": 1, "pos": [-0.50, +2.35], "time": 6.5,}, {"movement": 1, "pos": [+0.50, -0.65], "time": 6.5,}],
    [{"movement": 1, "pos": [-1.00, +2.30], "time": 7.0,}, {"movement": 1, "pos": [+0.00, -0.70], "time": 7.0,}],
    [{"movement": 1, "pos": [-1.50, +2.25], "time": 7.5,}, {"movement": 1, "pos": [-0.50, -0.75], "time": 7.5,}],
]

for x in xrange(len(lista)-1):
    lista[x][0]["pos"][0] += -land._parameters["vision_error"] + 2*land._parameters["vision_error"]*random.random()
    lista[x][0]["pos"][1] += -land._parameters["vision_error"] + 2*land._parameters["vision_error"]*random.random()
    
    lista[x][1]["pos"][0] += -land._parameters["vision_error"] + 2*land._parameters["vision_error"]*random.random()
    lista[x][1]["pos"][1] += -land._parameters["vision_error"] + 2*land._parameters["vision_error"]*random.random()

for dataland, datarob in lista:
#     print dataland, "\n"
    me.update(land.update(dataland))
#     print me[1]["x_speed"], me[1]["R"], "\n"
    
    print datarob, "\n"
    rob.update(datarob)
    print rob._predictedstate["x"].evalf(3), rob._predictedstate["covariance"].evalf(3), "\n"

land._end( )
rob._end( )

me[1]['x_speed'], me[1]['R']