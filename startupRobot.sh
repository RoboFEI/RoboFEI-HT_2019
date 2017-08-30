blue='\e[0;34m'
NC='\e[0m' # No Color
#font colors:
#Black        0;30     Dark Gray     1;30
#Blue         0;34     Light Blue    1;34
#Green        0;32     Light Green   1;32
#Cyan         0;36     Light Cyan    1;36
#Red          0;31     Light Red     1;31
#Purple       0;35     Light Purple  1;35
#Brown/Orange 0;33     Yellow        1;33
#Light Gray   0;37     White         1;37

echo -e "${blue} Configurando sistema...${NC}"
cp ./Config/bashrc ~/.bashrc
./Config/git-completion.bash ~/git-completion.bash
./Config/git-prompt.sh ~/git-prompt.sh
sleep 2

#updates/system changes
echo -e "${blue} Upgrade ${NC}"
sudo apt -y upgrade
echo -e "${blue} Update ${NC}"
sudo apt -y update

echo -e "${blue} Instalando softwares...${NC}"

sleep 2

#softwares
echo  -e "${blue} G++ ${NC}"
sudo apt -y install g++
echo  -e "${blue} gedit ${NC}"
sudo apt -y install gedit gedit-plugins
echo  -e "${blue} Gparted ${NC}"
sudo apt -y install gparted
echo  -e "${blue} NTP ${NC}"
sudo apt -y install ntp
echo -e "${blue} Gnome-system-tools ${NC}"
sudo apt -y install gnome-system-tools
echo -e "${blue} Git ${NC}"
sudo apt -y install git-core
sudo apt -y install gitk
echo -e "${blue} Boost ${NC}"
sudo apt -y install libboost-all-dev 
echo -e "${blue} SSH Server ${NC}"
sudo apt -y install openssh-server 
echo -e "${blue} SSH Client ${NC}"
sudo apt -y install openssh-client 
echo -e "${blue} FileZilla ${NC}"
sudo apt -y install filezilla
echo -e "${blue} Arduino ${NC}"
sudo apt -y install arduino
echo -e "${blue} Curses.h ${NC}"
sudo apt -y install libncurses5-dev
echo -e "${blue} FFMPEG ${NC}"
sudo add-apt-repository -y ppa:mc3man/gstffmpeg-keep
sudo apt -y update
sudo apt -y install ffmpeg gstreamer0.10-ffmpeg 
echo -e "${blue} Xindy ${NC}"
sudo apt -y install xindy
echo -e "${blue} cheese ${NC}"
sudo apt -y install cheese
echo -e "${blue} Core library dependencies (Robô Jimmy) ${NC}"
sudo apt -y install build-essential libncurses5-dev libjpeg-dev mplayer mplayer-skins
sudo apt -y install git-cola

#Ajuste do auto foco na camera
sudo apt -y install v4l-utils

#Screen
sudo apt -y install screen

#PS3/Bluetooth dependencies:
echo -e "${blue} PS3/Bluetooth dependencies (Robô Jimmy) ${NC}"
sudo apt -y install bluez-utils bluez-compat bluez-hcidump libusb-dev libbluetooth-dev joystick

#ConfigParser
sudo apt-get install python-configparser

#opencv
echo -e "${blue} Opencv dependências ${NC}"
sleep 1

sudo apt -y install scipy python-pygame

sudo apt -y autoremove libopencv-dev python-opencv
echo -e "${blue} Opencv dependências ${NC}"
sleep 1
sudo apt -y install build-essential cmake
sudo apt -y install qt5-default libvtk6-dev
sudo apt -y install zlib1g-dev libjpeg-dev libwebp-dev libpng-dev libtiff5-dev libjasper-dev libopenexr-dev libgdal-dev
sudo apt -y install libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev yasm libfaac-dev libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev libxine2-dev
sudo apt -y install libtbb-dev libeigen3-dev
sudo apt -y install python-dev python-tk python-numpy python3-dev python3-tk python3-numpy
sudo apt -y install ant default-jdk
sudo apt -y install doxygen sphinx-common texlive-latex-extra

#sudo apt -y install build-essential cmake pkg-config
#sudo apt -y install libjpeg62-dev 
#sudo apt -y install libtiff4-dev libjasper-dev
#sudo apt -y install  libgtk2.0-dev
#sudo apt -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
#sudo apt -y install libdc1394-22-dev
#sudo apt -y install libxine-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev 
#sudo apt -y install libtbb-dev
sudo apt -y install libqt4-dev

#pip
sudo apt -y install python-pip

sudo -H pip install imutils

sudo -H pip install --upgrade pip #Nao ha necessidade, a nao ser q a versao do pip seja muito antiga

#Construct 2.5.3
sudo pip install construct==2.5.3

#Upgrade numpy
sudo -H pip install --upgrade numpy

#Cython
sudo -H pip install Cython

#scikit-image
sudo -H pip install scikit-image

#Protobuth
sudo -H pip install protobuf

#============================Install Opencv 3===================================================================
light_Green='\e[1;32m'
NC='\e[0m' # No Color
#font colors:
#Black				0;30		Dark Gray			1;30
#Blue					0;34		Light Blue		1;34
#Green				0;32		Light Green		1;32
#Cyan					0;36		Light Cyan		1;36
#Red					0;31		Light Red			1;31
#Purple				0;35		Light Purple	1;35
#Brown/Orange	0;33		Yellow				1;33
#Light Gray		0;37		White					1;37

echo "${blue}Install Dependence${NC}"
sudo apt -y install build-essential
#sudo apt -y install aptitude
#sudo aptitude -y install libgtk2.0-dev
sudo apt -y install qt-sdk
sudo apt -y install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt -y install python-dev libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev


echo "${blue}Clone to GitHub${NC}"
sudo rm  -r ~/OpenCV3
mkdir ~/OpenCV3
cd ~/OpenCV3
git clone https://github.com/Itseez/opencv.git


echo "${blue}Run CMake${NC}"
cd opencv
mkdir release
cd release
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_TBB=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D WITH_V4L=ON -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=ON -D WITH_QT=ON -D WITH_GTK=ON -D WITH_OPENGL=ON ..

echo "${blue}Copile and install${NC}"
make -j4 # Numero de processadores na maquina
sudo make install

echo "${light_Green}Finalizado${NC}"
sudo rm  -r ~/OpenCV3
sleep 1
#=========================================================================================================================



#============================Install Caffe================================================================================
# General Dependencies
sudo apt -y install --no-install-recommends libboost-all-dev

sudo apt -y install libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev #Retirei a biblioteca libopencv-dev devido a possibilidade de conflito com a versao do opencv instalado

# Remaining dependencies
sudo apt -y install libgflags-dev libgoogle-glog-dev liblmdb-dev protobuf-compiler

#sudo apt install libopenblas-dev

# BLAS -- for better CPU performance
sudo apt -y install libatlas-base-dev

#scikit-image
sudo -H pip install scikit-image

#Protobuth
sudo -H pip install protobuf

cd

#Caffe
#git clone https://github.com/NVIDIA/caffe.git
git clone http://github.com/BVLC/caffe.git
cd caffe
cp Makefile.config.example Makefile.config
sed -i 's/.*CPU_ONLY := 1/CPU_ONLY := 1/g' Makefile.config # CPU only
sed -i 's/.*OPENCV_VERSION := 3/OPENCV_VERSION := 3/' Makefile.config # PENCV_VERSION 3
#sed -i 's/.*WITH_PYTHON_LAYER := 1/WITH_PYTHON_LAYER := 1/' Makefile.config # WITH_PYTHON_LAYER
#sed -i 's/.*USE_PKG_CONFIG := 1/USE_PKG_CONFIG := 1/' Makefile.config # USE_PKG_CONFIG
make -j4
make test
make runtest
make pycaffe
echo 'export PYTHONPATH=~/caffe/python' >> ~/.bashrc
echo 'export CAFFE_ROOT=~/caffe' >> ~/.bashrc
#=========================================================================================================================


echo -e "${blue} Autoremove ${NC}"
sudo apt -y autoremove

sudo apt install -f

echo -e "${blue} Update ${NC}"
sudo apt -y update

echo -e "${blue} Configuração realizada ${NC}"
