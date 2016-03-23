blue='\e[0;34m'
NC='\e[0m' # No Color
red='\e[0;31m'
green='\e[0;32m' 

echo
sudo echo  "This script will configure bashrc file and install RoboFEI-HT software"
echo
read -p "Continue? (y/n) " -n 1 -r
echo 
if [[  $REPLY =~ ^[Nn]$ ]]
then
    exit 1
fi

echo -e "${blue} Installing whole software ${NC}"
mkdir build

cd build

cmake ../

make all

make install

cd ..

echo -e "${blue} That's all folks! Have fun! ${NC}" 


