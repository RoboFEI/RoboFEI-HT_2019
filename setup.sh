blue='\e[0;34m'
NC='\e[0m' # No Color
red='\e[0;31m'
green='\e[0;32m' 

re='^[0-9]+$' # Is number

echo
echo  "This script will configure RoboFEI-HT software"
echo
if [ -z "$1" ]; then
    read -p "Continue? (y/n) " -n 1 -r
    echo 

    if [[  $REPLY =~ ^[Nn]$ ]] 
    then
        exit 1
    fi
fi

if [[ "$1" == "S" || "$2" == "S" || "$3" == "S" || "$1" == "s" || "$2" == "s" || "$3" == "s" ]]; then
	MODE="S"
else
	if [[ "$1" == "R" || "$2" == "R" || "$3" == "R" || "$1" == "r" || "$2" == "r" || "$3" == "r" ]]; then
		MODE="R"
	else
		  echo "Will this setup be used for Simulation or Real robot (S/R)? "
		  read MODE
	fi
fi

if [  $MODE == "S" ] || [  $MODE == "s" ];
then
    echo -e "${blue} ***** SIMULATION MODE ***** ${NC}"
	if ! [[ $1 =~ $re || $2 =~ $re ]] ; then
		read -p "How many robots do you want to compile? "
		echo 
	else
		if [[ $1 =~ $re ]]; then
			REPLY=$1
		fi
		if [[ $2 =~ $re ]]; then
			REPLY=$2
		fi
	fi
	echo
	if [ $REPLY == 1 ]; then
		echo -e "${blue} AI ${NC}"
		echo -e "${blue} Installing serial ${NC}"
	    cd AI/IMU/serial
	    mkdir build
	    cd build
	    cmake ../
	    make all
	    sudo make install
	    cd ../../..
		echo
		echo -e "${blue} Installing whole software ${NC}"
		cd AI
		mkdir build
		cd build
		cmake ../
		make all
		make install
		cd ..
		cd Control/Data
		sed -i -e 's/no_player_robofei = [0-30]*/no_player_robofei = 1 /' config.ini
		cd ../../..
	fi

	if [ $REPLY -gt 1 ]; then
		echo 'starting ' $REPLY ' robots'
		cd AI
		mkdir build
		cd build
		cmake ../
		make all
		make install
		cd ..
		cd Control/Data
		sed -i -e 's/no_player_robofei = [0-30]*/no_player_robofei = 1 /' config.ini
		cd ../../..
		for ((i = 2; i <= $REPLY; i++)); do
		    cp -ar AI AI$i
		    cd AI$i/Control/Data
		    sed -i -e 's/no_player_robofei = [0-30]*/no_player_robofei = '$i'/' config.ini
		    cd ../../..
		done
	fi

	for ((i = 1; i <= "$REPLY"; i++)); do
		if [ $i == 1 ]; then
		    cd AI
		else
		    cd AI$i
		fi	
		echo -e "${blue} Installing whole software ${NC}"
		mkdir build
		cd build
		cmake ../
		make all
		make install
		cd ../..
	done
else
	echo -e "${blue} ***** REAL MODE ***** ${NC}"
	sleep 1
	echo -e "${blue} Installing serial ${NC}"
	cd AI/IMU/serial
	mkdir build
	cd build
	cmake ../
	make all
	sudo make install
	cd ../../..

	echo -e "${blue} Installing whole software ${NC}"
	cd AI
	mkdir build
	cd build
	cmake ../
	make all
	make install
	cd ../../
	sudo echo  -e "Creating rules for recognizing device${red} IMU${NC}"
	cat <<EOF > 41-ftdi-imu.rules
	KERNEL=="ttyUSB?", SUBSYSTEMS=="usb", ATTRS{idVendor}=="067b",  ATTRS{idProduct}=="2303", MODE="0777", SYMLINK+="robot/imu"
EOF
	chmod +x 41-ftdi-imu.rules
	sudo echo  -e "Copying file${blue} 41-ftdi-imu.rules${NC} to ${green}/etc/udev/rules.d${NC}"
	sudo cp  41-ftdi-imu.rules  /etc/udev/rules.d
    rm 41-ftdi-imu.rules

	sudo echo  -e "Creating rules for recognizing devices${red} Servo${NC}"
    sudo python ./AI/Control/Linux/device/renamePort.py

	sudo echo  "Restarting udev"
	sudo service udev restart

	cd  AI/Control/Data/

	sudo echo "Starting robots configuration"
	if ! [[ $1 =~ $re || $2 =~ $re || $3 =~ $re ]] ; then
		sudo echo "Insert robot number: "
		read NUM
	else
		if [[ $1 =~ $re ]]; then
			NUM=$1
		fi
		if [[ $2 =~ $re ]]; then
			NUM=$2
		fi
		if [[ $3 =~ $re ]]; then
			NUM=$3
		fi
	fi
	case $NUM in
	  1) sudo echo "Robot 1 ..."
		 if [[ "$1" == "G" || "$2" == "G" || "$3" == "G" || "$1" == "g" || "$2" == "g" || "$3" == "g" ]]; then
			 CONF="y"
		 else
			 if [[ "$1" == "F" || "$2" == "F" || "$3" == "F" || "$1" == "f" || "$2" == "f" || "$3" == "f" ]]; then
				 CONF="n"
			 else
				 sudo echo "Artificial Grass [Y/N]: "
				 read CONF
			 fi
		 fi
		 if [ "$CONF" = "y" ]
		 then
		    ln -sf ../../conf_robos/01/grama/* .
		    ln -sf ../../conf_robos/01/vision/config.ini ../../Vision/Data/config.ini
		    ln -sf ../../conf_robos/01/vision/Vector.npy ../../Vision/Data/Vector.npy
		    cp ../../conf_robos/01/vision/ball.tar.gz ../../Vision/Data/ball.tar.gz
		    echo "grass files copied!"
		 elif [ "$CONF" = "n" ]
		 then
		    ln -sf ../../conf_robos/01/chao/* .
		    ln -sf ../../conf_robos/01/vision/config.ini ../../Vision/Data/config.ini
		    ln -sf ../../conf_robos/01/vision/Vector.npy ../../Vision/Data/Vector.npy
		    cp ../../conf_robos/01/vision/ball.tar.gz ../../Vision/Data/ball.tar.gz
		    echo "flat floor files copied!"
		 else
		     echo "invalid choice"
		 fi;;

	  2) sudo echo "Robot 2 ..."
		 if [[ "$1" == "G" || "$2" == "G" || "$3" == "G" || "$1" == "g" || "$2" == "g" || "$3" == "g" ]]; then
			 CONF="y"
		 else
			 if [[ "$1" == "F" || "$2" == "F" || "$3" == "F" || "$1" == "f" || "$2" == "f" || "$3" == "f" ]]; then
				 CONF="n"
			 else
				 sudo echo "Artificial Grass [Y/N]: "
				 read CONF
			 fi
		 fi
		 if [ "$CONF" = "y" ]
		 then
		    ln -sf ../../conf_robos/02/grama/* .
		    ln -sf ../../conf_robos/02/vision/config.ini ../../Vision/Data/config.ini
		    ln -sf ../../conf_robos/02/vision/Vector.npy ../../Vision/Data/Vector.npy
		    cp ../../conf_robos/02/vision/ball.tar.gz ../../Vision/Data/ball.tar.gz
		    echo "grass files copied!"
		 elif [ "$CONF" = "n" ]
		 then
		    ln -sf ../../conf_robos/02/chao/* .
		    ln -sf ../../conf_robos/02/vision/config.ini ../../Vision/Data/config.ini
		    ln -sf ../../conf_robos/02/vision/Vector.npy ../../Vision/Data/Vector.npy
		    cp ../../conf_robos/02/vision/ball.tar.gz ../../Vision/Data/ball.tar.gz
		    echo "flat floor files copied!"
		 else
		     echo "invalid choice"
		 fi;;

	  3) sudo echo "Robot 3 ..."
		 if [[ "$1" == "G" || "$2" == "G" || "$3" == "G" || "$1" == "g" || "$2" == "g" || "$3" == "g" ]]; then
			 CONF="y"
		 else
			 if [[ "$1" == "F" || "$2" == "F" || "$3" == "F" || "$1" == "f" || "$2" == "f" || "$3" == "f" ]]; then
				 CONF="n"
			 else
				 sudo echo "Artificial Grass [Y/N]: "
				 read CONF
			 fi
		 fi
		 if [ "$CONF" = "y" ]
		 then
		    ln -sf ../../conf_robos/03/grama/* .
		    ln -sf ../../conf_robos/03/vision/config.ini ../../Vision/Data/config.ini
		    ln -sf ../../conf_robos/03/vision/Vector.npy ../../Vision/Data/Vector.npy
		    cp ../../conf_robos/03/vision/ball.tar.gz ../../Vision/Data/ball.tar.gz
		    echo "grass files copied!"
		 elif [ "$CONF" = "n" ]
		 then
		    ln -sf ../../conf_robos/03/chao/* .
		    ln -sf ../../conf_robos/03/vision/config.ini ../../Vision/Data/config.ini
		    ln -sf ../../conf_robos/03/vision/Vector.npy ../../Vision/Data/Vector.npy
		    cp ../../conf_robos/03/vision/ball.tar.gz ../../Vision/Data/ball.tar.gz
		    echo "flat floor files copied!"
		 else
		     echo "invalid choice"
		 fi;;

	  4) sudo echo "Robot 4 ..."
		 if [[ "$1" == "G" || "$2" == "G" || "$3" == "G" || "$1" == "g" || "$2" == "g" || "$3" == "g" ]]; then
			 CONF="y"
		 else
			 if [[ "$1" == "F" || "$2" == "F" || "$3" == "F" || "$1" == "f" || "$2" == "f" || "$3" == "f" ]]; then
				 CONF="n"
			 else
				 sudo echo "Artificial Grass [Y/N]: "
				 read CONF
			 fi
		 fi
		 if [ "$CONF" = "y" ]
		 then
		    ln -sf ../../conf_robos/04/grama/* .
		    ln -sf ../../conf_robos/04/vision/config.ini ../../Vision/Data/config.ini
		    ln -sf ../../conf_robos/04/vision/Vector.npy ../../Vision/Data/Vector.npy
		    cp ../../conf_robos/04/vision/ball.tar.gz ../../Vision/Data/ball.tar.gz
		    echo "grass files copied!"
		 elif [ "$CONF" = "n" ]
		 then
		    ln -sf ../../conf_robos/04/chao/* .
		    ln -sf ../../conf_robos/04/vision/config.ini ../../Vision/Data/config.ini
		    ln -sf ../../conf_robos/04/vision/Vector.npy ../../Vision/Data/Vector.npy
		    cp ../../conf_robos/04/vision/ball.tar.gz ../../Vision/Data/ball.tar.gz
		    echo "flat floor files copied!"
		 else
		     echo "invalid choice"
		 fi;;
	  
	  *) sudo echo "Invalid robot number!" ;;
	esac
fi

cd ../../..

echo -e "${blue} That's all folks! Have fun! ${NC}" 
