#!/bin/bash
#!/RoboFEI-HT/build/bin

echo "vision"
echo 'export PYTHONPATH=~/caffe/python'
cd ../Vision/src/

python vision.py
