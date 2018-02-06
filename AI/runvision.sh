#!/bin/bash
PYTHONPATH=~/models/research/slim:~/models/research/object_detection:~/models/research:$PYTHONPATH

cd Vision/
python vision.py --dnn --v /home/fei/Videos/Ex2/Back/03_rob.mp4