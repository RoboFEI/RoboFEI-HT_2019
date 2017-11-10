#!/bin/bash
#!/RoboFEI-HT/build/bin

echo "vision"
export PYTHONPATH=~/caffe/python
export CAFFE_ROOT=~/caffe
cd ../Vision/src/

python vision.py 
