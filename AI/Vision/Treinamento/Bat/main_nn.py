# coding: utf-8

#  ****************************************************************************
#  * @file: trainNN.py
#  * @project: ROBOFEI-HT - FEI 😛
#  * @author: Vinicius Nicassio Ferreira
#  * @version: V0.0.1
#  * @created: 23/10/2017
#  * @e-mail: vinicius.nicassio@gmail.com
#  * @brief: Vision
#  ****************************************************************************
#  Program to execute the Vision process
#  ****************************************************************************

# ---- List of execution parameters ----

import argparse

parser = argparse.ArgumentParser(
    description='Vision',
    epilog= 'Responsável por realizar as detecções de objetos utilizando a camera e rastrear os objetos na imagens utilizando os motores.\\' \
        'Responsible for performing object detections using the camera and tracking the objects in the imagens using the engines.'
)

parser.add_argument(
    '--thread', # Full name
    '--t', # Abbreviation for the name
    type = int, # Type variable
    help = 'Utiliza um video para execução do sistema de visão.\\' \
    'Uses a video for running the vision system.' # Description of the variable
)

parser.add_argument(
    '--maximumindividuals', # Full name
    '--m', # Abbreviation for the name
    type = int, # Type variable
    help = 'Utiliza um video para execução do sistema de visão.\\' \
    'Uses a video for running the vision system.' # Description of the variable
)

parser.add_argument(
    '--generations', # Full name
    '--g', # Abbreviation for the name
    type = int, # Type variable
    help = 'Utiliza um video para execução do sistema de visão.\\' \
    'Uses a video for running the vision system.' # Description of the variable
)

args = parser.parse_args()

# ---- Imports ----

# Libraries to be used.
# import threading
# from time import sleep
import sys
sys.path.append('./include')
sys.path.append('./src')

# Used class developed by RoboFEI-HT.
from Individual import *

# ---- Preparing process ----

# Dados de treinamento
intrain = (np.random.rand(1000)*100).reshape(-1, 1)
intrain = np.array(range(1000)).reshape(-1, 1)
# outtrain = (np.random.rand(1000)*100).reshape(-1, 1)
outtrain = intrain*2 + 10  # função

# Dados de teste
intest = (np.random.rand(1000)*100).reshape(-1, 1)
intest = np.array(range(1000)).reshape(-1, 1)
outtest = intest*2 + 10  # função
# intest = intrain
# outtest = outtrain

population = [ ]

if args.maximumindividuals is None:
    args.maximumindividuals = 50

if args.thread is None:
    args.thread = args.maximumindividuals/2

if args.generations is None:
    args.generations = 50

for __ in xrange(args.maximumindividuals):
    population.append(Individual( ))

# ---- Run process ----
for __ in xrange(args.generations):
    listthread = []
    for individual in population:
        individual.performance(intrain, outtrain.ravel( ), intest, outtest.ravel( ))

    population.sort(key=lambda x: x.weight, reverse=True)

    population = population[:len(population)/2]

    ###############  DEBUG #################################################
    print "\n*******************"
    for individual in population:
        print "weight:", individual.weight
        print "architecture: ", individual.network_architecture
    print "*******************\n"
    ###############  DEBUG #################################################

    aux = 0
    while len(population) < args.maximumindividuals:
        if np.random.rand() > 30.0/100:
            # print "Faz o cross"
            for son in population[aux].cross(population[aux+1]):
                population.append(son)
            aux += 2
        else:
            # print "Faz o x-man"
            population.append(
                population[aux].mutation()
            )
            aux += 1

###############  DEBUG #################################################
print "\n*******************"
for individual in population:
    print "weight:", individual.weight
    print "architecture: ", individual.network_architecture
print "*******************\n"
###############  DEBUG #################################################

# ---- Finalizing process ----
