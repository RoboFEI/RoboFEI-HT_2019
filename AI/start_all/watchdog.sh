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
        sudo screen -d -m -S imu ./start_imu.sh
        echo Iniciando IMU
    fi

    if [ ! "$(pidof -x start_decision.sh)" ]  
    then
        sudo screen -d -m -S decision ./start_decision.sh
        echo Iniciando decision
    fi

    if [ ! "$(pidof -x start_control.sh)" ] 
    then
        sudo screen -d -m -S control ./start_control.sh
        echo Iniciando control
    fi

    if [ ! "$(pidof -x start_vision.sh)" ] 
    then
        sudo screen -d -m -S vision ./start_vision.sh
        echo Iniciando vision
    fi

    if [ ! "$(pidof -x start_comm.sh)" ] 
    then
        sudo screen -d -m -S communication ./start_comm.sh
        echo Iniciando communication
    fi

    if [ ! "$(pidof -x start_commServer.sh)" ] 
    then
        sudo screen -d -m -S commServer ./start_commServer.sh
        echo Iniciando Server communication
    fi

    if [ ! "$(pidof -x start_commClient.sh)" ] 
    then
        sudo screen -d -m -S commClient ./start_commClient.sh
        echo Iniciando Client communication
    fi

    echo ''
    sleep 5
done
