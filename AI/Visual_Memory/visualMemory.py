# coding: utf-8

# ---- List of execution parameters ----

import argparse

parser = argparse.ArgumentParser(
 description='Robot Vision',
 epilog= 'Responsável pela detecção dos objetos em campo./Responsible for detection of field objects.'
)

parser.add_argument('--robot_numbers', # Full name
				 '--rn', # Abbreviation for the name
				 type = int, # Type variable
				 help = 'Calibra valor para a câmera.\\' \
						'Calibrates value for the camera.' # Description of the variable
				)

args = parser.parse_args()

print args.robot_numbers

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('./include')
sys.path.append('./src')

# The standard libraries used in the Visual Memory System.
import numpy as np
import os

# Used class developed by RoboFEI-HT
from MainFunctions import * # Declaration the main functions.
from Blackboard import * # Class used to access shared memory.
from Robots import * # Class used to track robot.
from Landmark import * # Class used to track landmark.
from Ball import * # Class used to track ball.
from ConfigIni import * # Used to read file 'config.ini'.

# ---- Main Code ----

# Starting processes

killedProcess() # Recognize external kill

# Default values
parameters = {
	"robot_numbers": 8
}

# Reading 'config.ini' values
conf = ConfigIni("Basic", "Settings")
parameters = conf.read(parameters)

mem = Blackboard( ) # Creating shared memory

land = Landmark( ) # Creating landmark object

ball = Ball( ) # Creating landmark object

# Creating robot objects
robots = []
for __ in xrange(parameters['robot_numbers']):
	robots.append(Robots( ))

# Main loop

while True:
	try:
		1+2*5+4+78/5*78+7-7+87
	except KeyboardInterrupt:
		os.system('clear') # Cleaning terminal
		print "Keyboard interrupt detected"
		break
	except VisionException as e:
		break

# Finishing processes

# Saving config values
conf.finalize(parameters)
