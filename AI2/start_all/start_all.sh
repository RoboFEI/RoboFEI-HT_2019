#!/bin/bash
#!/RoboFEI-HT/build/bin

sudo echo "starting all processes"
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/RoboFEI-HT/build/lib
# export PATH=$PATH:~/RoboFEI-HT/build/bin
# source #HOME/.bashrc

#while true
#do
    #if [ ! "$(pidof imu)" ] 
    #then
    #   mate-terminal --title="IMU" -x sh -c './start_imu.sh' &
    #fi

   if [ ! "$(pidof -x start_vision.sh)" ] 
   then
        gnome-terminal --title="VISION" -x sh -c './start_vision.sh' &
   fi

    if [ ! "$(pidof -x start_decision.sh)" ]  
    then
        gnome-terminal --title="DECISION" -x sh -c './start_decision.sh' &
    fi

    if [ ! "$(pidof control)" ] 
    then
       gnome-terminal --title="CONTROL" -x sh -c 'echo 123456 | sudo -S ./start_control.sh' &
    fi

    if [ ! "$(pidof communication)" ] 
    then
       gnome-terminal --title="REFEREE" -x sh -c './start_comm.sh' &
    fi

    if [ ! "$(pidof -x start_commServer.sh)" ] 
    then
       gnome-terminal --title="COMM_SERVER" -x sh -c './start_commServer.sh' &
    fi

    if [ ! "$(pidof -x start_commClient.sh)" ] 
    then
       gnome-terminal --title="COMM_CLIENT" -x sh -c './start_commClient.sh' &
    fi

#    sleep 4
#done
