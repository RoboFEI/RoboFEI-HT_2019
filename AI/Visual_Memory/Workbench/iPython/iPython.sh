#!/bin/bash

./convertendo.sh
gnome-terminal -x sh -c 'export PYTHONPATH=~/caffe/python && export CAFFE_ROOT=~/caffe && export PYTHONPATH=~/models/research/slim:~/models/research/object_detection:~/models/research:$PYTHONPATH && export PATH=~/.local/bin:$PATH && echo "\33[0;34mIniciando iPython \33[0m" && jupyter notebook'
