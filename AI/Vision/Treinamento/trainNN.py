# coding: utf-8

#  ****************************************************************************
#  * @file: trainNN.py
#  * @project: ROBOFEI-HT - FEI 😛
#  * @author: Vinicius Nicassio Ferreira
#  * @version: V0.0.1
#  * @created: 18/04/2018
#  * @e-mail: vinicius.nicassio@gmail.com
#  * @brief: trainNN
#  ****************************************************************************
#  Program to execute the training of neural networks
#  ****************************************************************************

# ---- List of execution parameters ----

import argparse

parser = argparse.ArgumentParser(
    description='Vision',
    epilog='Responsável por realizar as detecções de objetos utilizando a camera e rastrear os objetos na imagens utilizando os motores.\\'
    'Responsible for performing object detections using the camera and tracking the objects in the imagens using the engines.'
)

parser.add_argument(
    '--video',  # Full name
    '--v',  # Abbreviation for the name
    type=str,  # Type variable
    help='Utiliza um video para execução do sistema de visão.\\' \
    'Uses a video for running the vision system.'  # Description of the variable
)

parser.add_argument(
    '--camera',  # Full name
    '--c',  # Abbreviation for the name
    action="store_true",  # Type variable
    help='Calibra valor para a câmera.\\' \
    'Calibrates value for the camera.'  # Description of the variable
)

parser.add_argument(
    '--dnn',  # Full name
    action="store_true",  # Type variable
    help='Exibe a classificação e a marcação feita pela DNN e ajusta os parametros para \'train\'.\\' \
    'Displays a DNN sort and markup and set the parameters to \'train\'.'  # Description of the variable
)

parser.add_argument(
    '--train',  # Full name
    '--tr',  # Abbreviation for the name
    action="store_true",  # Type variable
    help='Salva as imagens que tiveram um baixo percentual de classificação e cria um XML de marcação.\\' \
    'Saves imagens that have a low rating percentage and creates a markup XML.'  # Description of the variable
)

parser.add_argument(
    '--robots',  # Full name
    '--rob',  # Abbreviation for the name
    action="store_true",  # Type variable
    help='adlks.\\' \
    'adlks.'  # Description of the variable
)

args = parser.parse_args()

# ---- Imports ----

# Libraries to be used.
import sys
import os
os.chdir('../../')  # Running in the Vision folder
sys.path.append('./include')
sys.path.append('./src')
sys.path.append('./Train/NN')

# Used class developed by RoboFEI-HT.
from Individual import *

# ---- Preparing process ----

# Dados de treinamento
intrain = (np.random.rand(1000)*100).reshape(-1, 1)
outtrain = intrain*2 + 10  # função

# Dados de teste
intest = (np.random.rand(1000)*100).reshape(-1, 1)
outtest = intest*2 + 10  # função

population = [ ]

for __ in xrange(10):
    population.append(Individual( ))

# ---- Run process ----
for __ in xrange(20):
    weight = []
    architectures = []

    for individual in population:
        individual.performance(intrain, outtrain.ravel( ), intest, outtest.ravel( ))
        weight.append(individual.weight)
        architectures.append(individual.network_architecture)

    # ordering architecture by the score Value
    weight, population = map(list, zip(*sorted(zip(weight, population), reverse=True)))

    arc = len(population)/2 # initial index of substitution of the architectures
    for individual in population[: (len(population)/2)]: # runs half of the population array
        population[arc].setArchitecture(individual.geneticAlgorithm())# substitui na parte excluida uma nova arquitetura
        arc += 1

#----Train and ordering the higthests architectures scores ----
weight = [] # reseting the weight and architectures arrays
architectures = []

for individual in population:
    individual.performance(intrain, outtrain.ravel( ), intest, outtest.ravel( ))
    weight.append(individual.weight)
    architectures.append(individual.network_architecture)

# ordering architecture by the score Value
weight, population = map(list, zip(*sorted(zip(weight, population), reverse=True)))

for individual in population:
    print "weight:", individual.weight
    print "architecture: ", individual.network_architecture
# ---- Finalizing process ----



    # ###############  DEBUG #################################################
    # print "\n*******************"
    # for individual in population:
    #     print "weight:", individual.weight
    #     print "architecture: ", individual.network_architecture
    # print "*******************\n"
    # ###############  DEBUG #################################################
    #
