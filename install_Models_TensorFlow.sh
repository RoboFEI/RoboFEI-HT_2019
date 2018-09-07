#!/bin/bash

blue='\e[1;34m'
light_Green='\e[1;32m'
red='\033[0;31m'
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


echo -e "${blue}Atualizando programas${NC}";
sleep 1
sudo apt -y -f install
sudo apt -y update
sudo apt -y upgrade
# instructions from https://developer.nvidia.com/cuda-downloads (linux -> x86_64 -> Ubuntu -> 16.04 -> deb (network))


#echo -e "${blue}Install CUDA Toolkit v8.0${NC}";
#sleep 1
#wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_8.0.61-1_amd64.deb
#if sudo dpkg --install cuda-repo-ubuntu1604_8.0.61-1_amd64.deb && sudo apt-get update && sudo apt-get install cuda-8-0; then
#	echo -e "${red}Cuda Toolkit succesfully installed";
#	echo "PATH=/usr/local/cuda-8.0/bin${PATH:+:${PATH}}" >> ~/.bashrc;
#fi


#echo -e "${blue}Install cuDNN v6.0${NC}";
#sleep 1
#CUDNN_TAR_FILE="cudnn-8.0-linux-x64-v6.0.tgz";
#if wget http://developer.download.nvidia.com/compute/redist/cudnn/v6.0/${CUDNN_TAR_FILE} && tar -xzvf ${CUDNN_TAR_FILE} && sudo cp -P cuda/include/cudnn.h /usr/local/cuda-8.0/include && sudo cp -P cuda/lib64/libcudnn* /usr/local/cuda-8.0/lib64/ && sudo chmod a+r /usr/local/cuda-8.0/lib64/libcudnn*; then
#	echo -e "${red}cuDNN succesfully installed";
#fi


#echo -e "${blue}Install libcupti-dev${NC}";
#sleep 1
#if sudo apt-get install cuda-command-line-tools && export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-9.0/lib64 && sudo apt install libcupti-dev
#if sudo apt-get install libcupti-dev; then
	# set environment variables
#	echo 'export PATH=/usr/local/cuda-8.0/bin${PATH:+:${PATH}}' >> ~/.bashrc
#	echo 'export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> ~/.bashrc
#	echo -e "${red}libcupti-dev succesfully installed";
#fi


#echo -e "${blue}Install pip${NC}";
#if pip -V || pip3 -V; then
#	echo -e "${red}pip already installed";
#fi
#else
#	sudo apt-get install python-pip python-dev # for Python 2.7
#fi


#echo -e "${blue}Install TensorFlow v1.3${NC}";
#pip install --upgrade tensorflow      # for Python 2.7
#if sudo pip install tensorflow-gpu; then  # Python 2.7;  GPU support
#	echo -e "${red}TensorFlow succesfully installed";
#fi
#else
#	sudo pip  install --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.3.0-cp27-none-linux_x86_64.whl
   # Python 2.7
#fi


echo -e "${blue}Install Protoc_3.5.1${NC}";
mkdir ~/protoc_3.5.1
cd ~/protoc_3.5.1
if wget https://github.com/google/protobuf/releases/download/v3.5.1/protoc-3.5.1-linux-x86_64.zip && sudo chmod 775 protoc-3.5.1-linux-x86_64.zip && unzip protoc-3.5.1-linux-x86_64.zip; then
	echo -e"${red}Protocol buffers succesfully installed"
fi

#Or run 'sudo pip install protobuf==3.5.1'


echo -e "${blue}Clone Models${NC}";
cd ~/
git clone https://github.com/tensorflow/models.git

##############################


echo -e "${blue}Install Models${NC}";
# From ~/models/research/
cd ~/models/research/
	~/protoc_3.5.1/bin/protoc object_detection/protos/*.proto --python_out=.
echo "export PYTHONPATH=~/models/research/slim:~/models/research/object_detection/utils:~/models/research:\$PYTHONPATH" >> ~/.bashrc;


##############################


echo -e "${blue}Clone labelImg${NC}";
cd ~/
git clone https://github.com/tzutalin/labelImg

echo -e "${blue}Install labelImg${NC}";
cd ~/labelImg/
if sudo -H apt install pyqt4-dev-tools && sudo -H pip install lxml && make qt4py2; then
	echo -e"${red}labelImg succesfully installed"
fi


echo "export PATH=~/.local/bin:\$PATH" >> ~/.bashrc;
echo -e "cd ~/labelImg/\n\npython labelImg.py" >> ~/.local/bin/labelImg;
chmod 775 ~/.local/bin/labelImg


echo -e "${blue}Atualizando programas${NC}";
sleep 1
sudo apt -y -f install
sudo apt -y update
sudo apt -y upgrade
