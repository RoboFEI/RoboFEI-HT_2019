# coding: utf-8

#  ----------------------------------------------------------------------------
#  ****************************************************************************
#  * @file: visualMemory.py
#  * @project: ROBOFEI-HT - FEI 😛
#  * @author: Vinicius Nicassio Ferreira
#  * @version: V0.0.1
#  * @created: 22/09/2017
#  * @e-mail: vinicius.nicassio@gmail.com
#  * @brief: Visual Memory
#  ****************************************************************************
#  Program to execute the Visual Memory process
#  ****************************************************************************

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('./include')
sys.path.append('./src')

# Used class developed by RoboFEI-HT.
from Behavior import *

# ---- Preparing process ----

visualmemory = Behavior( )

# ---- Run process ----

visualmemory.run( )

# ---- Finalizing process ----

visualmemory.end( )