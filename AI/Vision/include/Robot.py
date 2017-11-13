# coding: utf-8

# ****************************************************************************
# * @file: Robot.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class Robot
# ****************************************************************************

# ---- Imports ----

# The standard libraries used in the vision system.

# The standard libraries used in the visual memory system.
import cv2 # OpenCV library used for image processing.

# Used class developed by RoboFEI-HT.

from DNN import *

def plot(img):

image = cv2.imread("/home/vinicius/Dropbox/Projeto Mestrado/Codigos/RoboFEI-HT_Debug/AI/Vision/Workbench/iPython/Competicao.jpg")
plot(image)

class argumentos:
    camera = False
    dnn = False
    train = False

a = argumentos()

classific = DNN(a)

observation = {}
observation['frame'] = image.copy()

observation['objetos'] = classific.detect(observation)
observation['objetos'] = observation['objetos'][observation['objetos'].classes != "robot"].reset_index()
del observation['objetos']["index"]
observation['objetos']

frame = image.copy()
for __, __, pos in observation['objetos'].values[:1]:
    cv2.circle(
        frame,
        tuple(
            np.resize(
                np.array(pos)*np.array(frame.shape[:2]+frame.shape[:2]),
                (2,2)
            ).mean(axis=0).astype(int)
        )[::-1],
        20,
        (255, 0, 255),
        -1,
    )
plot(frame)

for i in xrange(len(observation['objetos'])):
    observation['objetos']["boxes"][i] = np.resize(
        np.array(observation['objetos'].loc[i, "boxes"])*np.array(image.shape[:2]+image.shape[:2]),
        (2,2)
    ).mean(axis=0).astype(int).tolist()
observation['objetos']

## Class Robot
# .
class Robot( ):
    
    # ---- Variables ----
    
    ## Constructor Class
    def __init__(self):
        pass