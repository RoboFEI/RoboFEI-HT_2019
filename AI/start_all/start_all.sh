#!/bin/bash
#!/RoboFEI-HT/build/bin

trap finalizando INT HUP TERM

function finalizando()
{
clear
echo Matando processos

if [ "$(pidof -x start_imu.sh)" ]
then
    sudo kill $(pidof -x start_imu.sh)
fi

if [ "$(pidof -x start_vision.sh)" ]
then
    sudo kill $(pidof -x start_vision.sh)
fi

if [ "$(pidof -x start_decision.sh)" ]
then
    sudo kill $(pidof -x start_decision.sh)
fi
    
if [ "$(pidof -x start_control.sh)" ]
then
    sudo kill $(pidof -x start_control.sh)
fi
    
if [ "$(pidof -x start_comm.sh)" ]
then
    sudo kill $(pidof -x start_comm.sh)
fi
    
if [ "$(pidof -x start_commServer.sh)" ]
then
    sudo kill $(pidof -x start_commServer.sh)
fi
    
if [ "$(pidof -x start_commClient.sh)" ]
then
    sudo kill $(pidof -x start_commClient.sh)
fi
exit 0
}

sudo echo "starting all processes"
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/RoboFEI-HT/build/lib
# export PATH=$PATH:~/RoboFEI-HT/build/bin
# source #HOME/.bashrc

while true
do
    if [ ! "$(pidof -x start_imu.sh)" ]
    then
        gnome-terminal --title="IMU" -x sh -c './start_imu.sh' &
        echo Iniciando IMU
    fi

    if [ ! "$(pidof -x start_decision.sh)" ]  
    then
        gnome-terminal --title="DECISION" -x sh -c './start_decision.sh' &
        echo Iniciando decision
    fi

    if [ ! "$(pidof -x start_vision.sh)" ] 
    then
        gnome-terminal --title="VISION" -x sh -c './start_vision.sh' &
        echo Iniciando vision
    fi

    if [ ! "$(pidof -x start_comm.sh)" ] 
    then
        gnome-terminal --title="COMMUNICATION" -x sh -c './start_comm.sh' &
        echo Iniciando communication
    fi

    if [ ! "$(pidof -x start_commServer.sh)" ] 
    then
        gnome-terminal --title="COMMSERVER" -x sh -c './start_commServer.sh' &
        echo Iniciando Server communication
    fi

    if [ ! "$(pidof -x start_commClient.sh)" ] 
    then
        gnome-terminal --title="COMMCLIENT" -x sh -c './start_commClient.sh' &
        echo Iniciando Client communication
    fi

    if [ ! "$(pidof -x start_control.sh)" ] 
    then
        sleep 1
        gnome-terminal --title="CONTROL" -x sh -c './start_control.sh' &
        echo Iniciando control
    fi

    echo ''
    sleep 2
done
