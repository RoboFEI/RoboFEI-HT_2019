#!/bin/bash
#!/RoboFEI-HT/build/bin

echo "starting decision"
cd ..
cd Decision/src/
#choose robot behavior: 
#-a: attacker
#-q: quarterback
#-g: golie:
#no arguments: hybrid 
python decision.py
