#!/bin/bash

Blue='\e[1;34m'
Light_Green='\e[1;32m'
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

echo -e "${Blue}Criando data${NC}"
rm -R ./models/model/
rm -R data
mkdir data

echo -e "${Blue}Gerando csv do xml${NC}"
python rename.py
python xml_to_csv.py
sed -i "2,\$s@^@$(pwd)/imagensTrain/@" ./data/train_labels.csv

echo -e "${Blue}Gerando Label${NC}"
python generate_label.py

echo -e "${Blue}Gerando TFRecords${NC}"
mkdir models
mkdir ./models/research
python generate_tfrecord.py --csv_input=./data/train_labels.csv  --output_path=./models/research/train.record

echo -e "${Blue}Modelo utilizado${NC}"
mkdir ./models/train
mkdir ./models/model
mkdir ./models/eval
echo -e "${Blue}Qual rede ira utilizar: ${NC}"
tar -xvzf *.tar.gz -C ./models/model

echo -e "${Blue}Gerando arquivos de configuração${NC}"
n=$(grep -o 'id' ./data/object-detection.pbtxt | wc -l)
sed -i "s/NUMBER_OF_CLASSES/"$n"/g" ./models/model/ssd_mobilenet_v1.config
sed -i "s@PATH_TO_BE_CONFIGURED/model.ckpt@$(pwd)/models/model/mobilenet_v1_1.0_224.ckpt@g" ./models/model/ssd_mobilenet_v1.config
sed -i "s@PATH_TO_BE_CONFIGURED/pet_train.record@$(pwd)/models/research/train.record@g" ./models/model/ssd_mobilenet_v1.config
sed -i "s@PATH_TO_BE_CONFIGURED/pet_val.record@$(pwd)/models/research/train.record@g" ./models/model/ssd_mobilenet_v1.config
sed -i "s@PATH_TO_BE_CONFIGURED/pet_label_map.pbtxt@$(pwd)/data/object-detection.pbtxt@g" ./models/model/ssd_mobilenet_v1.config
# if [ "$(ls -A ./models/train)" ]; then
# 	sed -i "s/checkpoint: false/checkpoint: true/g" ./models/model/ssd_mobilenet_v1.config
# fi

echo -e "${Blue}Executando treinamento${NC}"
gnome-terminal --title="Workspace treinamento" -x sh -c 'tensorboard --logdir="$(pwd)"' &
./train.sh
