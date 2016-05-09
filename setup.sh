blue='\e[0;34m'
NC='\e[0m' # No Color
red='\e[0;31m'
green='\e[0;32m' 

echo
echo  "This script will configure RoboFEI-HT software"
echo
read -p "Continue? (y/n) " -n 1 -r
echo 
if [[  $REPLY =~ ^[Nn]$ ]]
then
    exit 1
fi

read -p "How many robots do you want to compile? " -n 1 -r
echo 
if [[  $REPLY == 1 ]]
then
    echo -e "${blue} AI ${NC}"
    cd AI
    mkdir build
    cd build
    cmake ../
    make all
    make install
    cd ../..
fi

if [[  $REPLY > 1 ]]
then
    echo 'starting ' $REPLY ' robots'

    for ((i=2; i <= REPLY; i++));
    do
        cp -ar AI AI$i
        cd AI$i
        cd ../..
    done
fi

for ((i=1; i <= REPLY; i++));
do
    if [ i = 1 ]
    then
         cd AI
    else
        cd AI$i
    fi
    mkdir build
    cd build
    cmake ../
    make all
    make install
    cd ../..

echo -e "${blue} That's all folks! Have fun! ${NC}" 


