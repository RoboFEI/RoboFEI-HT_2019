# coding: utf-8

#  ****************************************************************************
#  * @file: visualMemory.py
#  * @project: ROBOFEI-HT - FEI 😛
#  * @author: Vinicius Nicassio Ferreira
#  * @version: V0.0.1
#  * @created: 23/10/2017
#  * @e-mail: vinicius.nicassio@gmail.com
#  * @brief: Visual Memory
#  ****************************************************************************
#  Program to execute the Visual Memory process
#  ****************************************************************************

# ---- List of execution parameters ----

import argparse

parser = argparse.ArgumentParser(
    description='Visual Memory',
    epilog= 'Responsável pelo rastreamento do objeto no campo e manter a informação de posição dos objetos sempre atualizada.\\' \
        'Responsible for tracking the object in the field and keeping the position information of the objects always updated.'
)

parser.add_argument(
    '--numberrobots', # Full name
    '--nr', # Abbreviation for the name
    type = int, # Type variable
    help = 'Quantidade de robos no campo.\\' \
    'Number of robots in fild.' # Description of the variable
)

parser.add_argument(
    '--executionperiod', # Full name
    '--p', # Abbreviation for the name
    type = int, # Type variable
    help = 'Período de execução em milisegundos.\\' \
    'Runtime in milliseconds.' # Description of the variable
)

parser.add_argument(
    '--debug', # Full name
    '--d', # Abbreviation for the name
    action = "store_true", # Type variable
    help = 'Exibe as informações calculadas os parametros utilizados.\\' \
    'Displays the calculated information the parameters used.' # Description of the variable
)

parser.add_argument(
    '--savedata', # Full name
    '--sd', # Abbreviation for the name
    action = "store_true", # Type variable
    help = 'Gera dados sobre as previsões feitas.\\' \
    'Generates data on the forecasts made.' # Description of the variable
)

args = parser.parse_args()

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('./include')
sys.path.append('./src')

# Used class developed by RoboFEI-HT.
from Behavior import *

# ---- Preparing process ----

visualmemory = Behavior(args)

# ---- Run process ----

visualmemory.run( )

# ---- Finalizing process ----

visualmemory.end( )