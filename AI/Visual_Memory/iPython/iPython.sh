#!/bin/bash

./convertendo.sh
gnome-terminal -x sh -c 'export PYTHONPATH=~/caffe/python && export CAFFE_ROOT=~/caffe && echo "\33[0;34mIniciando iPython \33[0m" && jupyter notebook'
