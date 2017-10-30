# coding: utf-8

# ****************************************************************************
# * @file: extratc.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class extratc
# ****************************************************************************

# ---- Imports ----

# Libraries to be used.
import time
import sys
import os
os.chdir('../')
sys.path.append('./include')
sys.path.append('./src')

# Used class developed by RoboFEI-HT.
from DNN import * # Class that implements object detection using a deep neural network (DNN).

class Argumentos:
    dnn = True
    train = True

a = Argumentos()

dnn = DNN(a)

dicionario = {}
os.system("mkdir ./Train/images\ to\ classify")
for video in os.listdir("./Train/Videos"):
    cap = cv2.VideoCapture("./Train/Videos/"+video)
    while True:
        for __ in xrange(0, 4):
            __, dicionario["frame"] = cap.read()
        if dicionario["frame"] is None:
            break
        dicionario["time"] = time.localtime()
        dnn.detect(dicionario)
    os.system("rm ./Train/Videos/"+video)

try:
    images = [i.rsplit(".", 1)[0] for i in os.listdir("./Train/images to classify")]
    xmls = [i.rsplit(".", 1)[0] for i in os.listdir("./Train/annotations DNN")]
    images = [i for i in images if i not in xmls]
    for image in images:
        dicionario["frame"] = cv2.imread("./Train/images to classify/"+image+".png")
        dicionario["time"] = time.localtime()
        dnn.detect(dicionario)
        os.system("rm ./Train/images\ to\ classify/"+image.replace(":","\\:").replace(" ","\\ ")+".png")
    cv2.destroyAllWindows()
except:
    pass