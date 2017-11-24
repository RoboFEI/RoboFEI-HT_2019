#!/bin/bash

Blue='\e[0;34m'
Light_Red='\e[1;31m'
Light_Green='\e[1;32m'
NC='\e[0m' # No Color

#font colors:
#Black				0;30		Dark_Gray			1;30
#Blue					0;34		Light_Blue		1;34
#Green				0;32		Light_Green		1;32
#Cyan					0;36		Light_Cyan		1;36
#Red					0;31		Light_Red			1;31
#Purple				0;35		Light_Purple	1;35
#Brown/Orange	0;33		Yellow				1;33
#Light Gray		0;37		White					1;37

./limpar_all.sh

echo -e "${Blue}Apagando pastas e arquivos${NC}"
sleep 1
cd ..
find ./Data/ -not -iname README.md -not -iname "distance_network.sav" -not -iname "rede.tar.gz" -exec rm {} \;
rm -r ./Data/Rede
rm -r ./include
rm -r ./src
find ./Train/ -not -iname "*mobilenet*.tar.gz"  -not -iname "*README.md" -exec rm {} \;
rm vision.py

notify-send "Limpeza realizada" "Arquivos da memória visual apagado."
