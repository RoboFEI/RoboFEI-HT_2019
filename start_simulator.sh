#!/bin/bash

read -p "How many robots do you want to start? "
echo 
echo 'starting ' $REPLY ' robots'

echo "starting RoboFEI-HT Soccer Simulator"
cd Simulator/
gnome-terminal --title "Simulator" -x sh -c 'python main_simulator.py' &
cd ..

cd AI/Communication/src
gnome-terminal --title "sending" -e "python sending.py"
gnome-terminal --title "receiving" -e "python receiving.py"
cd ../../Localization/src
gnome-terminal --title "localization" -e "python Localization.py -g"
cd ../../Decision/src
gnome-terminal --title "decision naive" -e "python decision.py -g"
cd ../../build/Communication/
gnome-terminal --title="referee" -x sh -c './communication' &
cd ../../..


if [  $REPLY -gt 1 ]; then
    for ((i = 2; i <= $REPLY; i++)); do
        cd AI$i/Communication/src
        gnome-terminal --title "sending" -e "python sending.py"
        gnome-terminal --title "receiving" -e "python receiving.py"
        cd ../../Localization/src
        gnome-terminal --title "localization" -e "python Localization.py -g"
        cd ../../Decision/src
        gnome-terminal --title "decision naive" -e "python decision.py -l"
        cd ../../build/Communication/
        gnome-terminal --title="referee" -x sh -c './communication' &
        cd ../../..
        done
fi
