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
#--naive_imu: naive behavior with orientation and revolve around ball
#--naive_imu_dec_turning: naive behavior with orientation and pass
python decision.py --naive_imu_dec_turning
