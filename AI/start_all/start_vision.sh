#!/bin/bash
#!/RoboFEI-HT/build/bin

echo "vision"
export PYTHONPATH=~/models/research/slim:~/models/research/object_detection/utils:~/models/research
export PYTHONPATH=$PYTHONPATH:~/models/research/slim:~/models/research/object_detection:~/models/research
cd ../Vision/src/

python vision.py 
