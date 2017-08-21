# coding: utf-8

# ---- List of execution parameters ----

import argparse

parser = argparse.ArgumentParser(
 description="Visual Memory",
 epilog= "Responsável por rastrear todos os objetos detectáveis pela visão.\\" \
		 "Responsible for tracking all objects detectable by vision."
)

parser.add_argument(
 "--robot_numbers", # Full name
 "--rn", # Abbreviation for the name
 type = int, # Type variable
 help = "Número de robôs que serão rastreados.\\" \
		"Number of robots to be tracked." # Description of the variable
)

args = parser.parse_args()

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append("./include")
sys.path.append("./src")

# The standard libraries used in the Visual Memory System.
import numpy as np
import os
import time

# Used class developed by RoboFEI-HT
from MainFunctions import * # Declaration the main functions.
from Blackboard import * # Class used to access shared memory.
from Robots import * # Class used to track robot.
from Landmark import * # Class used to track landmark.
from Ball import * # Class used to track ball.
from Speeds import * # Classes used to manage robot speed values.
from ConfigIni import * # Used to read file "config.ini".

# ---- Main Code ----

# Starting processes

killedProcess() # Recognize external kill

# Default values
parameters = {
	"robot_numbers": 8,
	"frequency_of_execution": 0,
}

# Reading "config.ini" values
conf = ConfigIni("Basic", "Settings")
parameters = conf.read(parameters)
if args.robot_numbers != None:
	parameters["robot_numbers"] = args.robot_numbers

if parameters['frequency_of_execution'] != 0:
	parameters['frequency_of_execution'] = 1.0/parameters['frequency_of_execution']

# List with velocities for each movement of the robot.
speeds = Speeds( )

mem = Blackboard( ) # Creating shared memory

land = Landmark(speeds) # Creating landmark object

ball = Ball(speeds) # Creating landmark object

# Creating robot objects
robots = []
newrobots = []
for __ in xrange(parameters["robot_numbers"]):
	newrobots.append(Robots(speeds))

# Main loop

while True:
	try:
		# start timestamp
		start = time.time()
		
		# Reading data about the landmark.
		taglandmark = mem.read_float("VISION_LAND_TAG")
		
		if taglandmark != 0:
			# Read the values sent
			datalandmarks = readDataLandmarks(taglandmark, mem)
			speeds.update(land.update(datalandmarks))
			
		else:
			land.prediction( )
		
		datarobots = readDataRobots(mem, parameters["robot_numbers"])
		
	#	 if datarobots == []:
			
		# stop timestamp
		diff = time.time() - start
		
		if parameters["frequency_of_execution"] - diff > 0:
			time.sleep(parameters["frequency_of_execution"] - diff)
		
	except KeyboardInterrupt:
		os.system("clear") # Cleaning terminal
		print "Keyboard interrupt detected"
		break
	except VisualMemoryException as e:
		break

# Finishing processes

# Saving config values
if parameters['frequency_of_execution'] != 0:
	parameters['frequency_of_execution'] = 1.0/parameters['frequency_of_execution']
conf.finalize(parameters)