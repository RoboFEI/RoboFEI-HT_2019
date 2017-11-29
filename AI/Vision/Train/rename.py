# coding: utf-8

import time
import sys
import os
os.chdir('../')
sys.path.append('./include')
sys.path.append('./src')

image = 1
names = [i.rsplit(".", 1)[0].replace(" ", "\ ") for i in os.listdir("./Train/imagensTrain")]
for name in names:
#     print name
    sub = "sed -i 's/"+ name.replace("\ ", " ") +"/image"+ str(image).zfill(5) +"/g' ./Train/annotations/"+ name +".xml"
#     print sub
    os.system(sub)
    jpg = "mv ./Train/imagensTrain/"+ name +".jpg ./Train/imagensTrain/image"+ str(image).zfill(5) +".jpg"
#     print jpg
    os.system(jpg)
    xml = "mv ./Train/annotations/"+ name +".xml ./Train/annotations/image"+ str(image).zfill(5) +".xml"
#     print xml
    os.system(xml)
#     raw_input()
    image +=1