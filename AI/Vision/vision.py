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

args = parser.parse_args()

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('./include')
sys.path.append('./src')

# Used class developed by RoboFEI-HT.
from Orchestrator import *

# ---- Preparing process ----

vision = Orchestrator(args)

# ---- Run process ----

vision.run( )

# ---- Finalizing process ----

vision.end( )

# import tarfile

# import tarfile
# tar = tarfile.open("./Data/Rede.tar.gz")
# tar.extractall(path="./Data/Rede")
# tar.close()