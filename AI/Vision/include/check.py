# coding: utf-8

# ****************************************************************************
# * @file: check.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class check
# ****************************************************************************

# ---- Imports ----

# Libraries to be used.
import time
import sys
import os
os.chdir('../')
sys.path.append('./include')
sys.path.append('./src')

xmls = [i.rsplit(".", 1)[0] for i in os.listdir("./Train/annotations DNN")][:10]
xmls

os.system("mkdir ./Train/imagens\ to\ check")
for files in xmls:
    os.system("mv ./Train/images\ to\ classify/"+files.replace(":", "\\:").replace(" ", "\\ ")+".png ./Train/imagens\ to\ check")

os.system("~/labelImg/labelImg.py")

os.system("mkdir ./Train/annotations")
os.system("mkdir ./Train/imagesTrain")
os.system("mv ./Train/imagens\ to\ check/* ./Train/imagesTrain")