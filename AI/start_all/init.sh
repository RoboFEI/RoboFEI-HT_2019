if [ ! "$(pidof -x watchdog.sh)" ] 
    then
       screen -S Watchdog -s ./watchdog.sh
else
       screen -r Watchdog
fi

