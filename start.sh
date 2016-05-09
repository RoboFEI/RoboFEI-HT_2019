#!/bin/bash

echo "starting RoboFEI-HT Soccer Simulator"
cd Simulator/
gnome-terminal --title "Simulator" -x sh -c 'python main_simulator.py' &
cd ..

echo "Starting first robot AI"
cd AI/Communication/src
gnome-terminal --title "sending" -e "python sending.py"
gnome-terminal --title "receiving" -e "python receiving.py"
cd ../../Decision/src
gnome-terminal --title "decision naive" -e "python decision.py -ni"
cd ../../..

#echo "starting 6 robots"

#for f in {2..6}
#do 
#   cp -ar AI AI$f
#    cd AI$f/Control/Data
#    sed -i -e 's/no_player_robofei = 1/no_player_robofei = '$f'/' config.ini
#    cd ../../..
#done


#for f in {2..6}
#do
#    cd AI$f/Communication/src
#    gnome-terminal --title "sending" -e "python sending.py"
#    gnome-terminal --title "receiving" -e "python receiving.py"
#    cd ../../Decision/src
#    gnome-terminal --title "decision naive" -e "python decision.py -ni"
#    cd ../../..
#done





