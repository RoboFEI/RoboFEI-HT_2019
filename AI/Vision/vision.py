# coding: utf-8

#  ****************************************************************************
#  * @file: vision.py
#  * @project: ROBOFEI-HT - FEI 😛
#  * @author: Vinicius Nicassio Ferreira
#  * @version: V0.0.1
#  * @created: 23/10/2017
#  * @e-mail: vinicius.nicassio@gmail.com
#  * @brief: Visual Memory
#  ****************************************************************************
#  Program to execute the Vision process
#  ****************************************************************************

# ---- List of execution parameters ----

import argparse

parser = argparse.ArgumentParser(
    description='Vision',
    epilog= 'Responsável por realizar as detecções de objetos utilizando a camera e rastrear os objetos na imagens utilizando os motores.\\' \
        'Responsible for performing object detections using the camera and tracking the objects in the images using the engines.'
)

parser.add_argument(
    '--camera', # Full name
    '--c', # Abbreviation for the name
    action = "store_true", # Type variable
    help = 'Calibra valor para a câmera.\\' \
    'Calibrates value for the camera.' # Description of the variable
)

parser.add_argument(
    '--dnn', # Full name
    action = "store_true", # Type variable
    help = 'Exibe a classificação e a marcação feita pela DNN e ajusta os parametros para \'train\'.\\' \
    'Displays a DNN sort and markup and set the parameters to \'train\'.' # Description of the variable
)

parser.add_argument(
    '--train', # Full name
    '--tr', # Abbreviation for the name
    action = "store_true", # Type variable
    help = 'Salva as imagens que tiveram um baixo percentual de classificação e cria um XML de marcação.\\' \
    'Saves images that have a low rating percentage and creates a markup XML.' # Description of the variable
)

args = parser.parse_args()

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('./include')
sys.path.append('./src')

# Used class developed by RoboFEI-HT.
from Orchestrator import *

# ---- Preparing process ----

if args.train == True:
    args.dnn = True

vision = Orchestrator(args)

# ---- Run process ----

vision.run( )

# ---- Finalizing process ----

vision.end( )