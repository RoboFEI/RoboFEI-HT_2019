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

#--naive: naive behavior
#--naive_imu: naive behavior with orientation and pass, but the robot closest to ball goes to it.
#--naive_imu_dec_turning: naive behavior with orientation and pass
#python decision.py --naive_imu_dec_turning
#python decision.py -nidt
#python decision.py -ni
python decision.py
