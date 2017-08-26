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

parser.add_argument(
 "--frequency_of_execution", # Full name
 "--f", # Abbreviation for the name
 type = float, # Type variable
 help = "Frequência de execução do programa, caso seja zero ira rodar sem interrupções.\\" \
		"Frequency of program execution, if zero will run without interruptions." # Description of the variable
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
from copy import copy

# Used class developed by RoboFEI-HT
from MainFunctions import * # Declaration the main functions.
from Blackboard import * # Class used to access shared memory.
from Robots import * # Class used to track robot.
from Landmark import * # Class used to track landmark.
from Ball import * # Class used to track ball.
from Speeds import * # Classes used to manage robot speed values.

# ---- Main Code ----

# Starting processes

killedProcess() # Recognize external kill

# Default values
parameters = {
	"robot_numbers": 8,
	"relation_measurement_and_robot": 80,
	"frequency_of_execution": 0.2,
}

# Reading "config.ini" values
conf = ConfigIni("Basic", "Settings")
parameters = conf.read(parameters)
if args.robot_numbers != None:
	parameters["robot_numbers"] = args.robot_numbers

if args.frequency_of_execution != None:
	parameters["frequency_of_execution"] = args.frequency_of_execution

if parameters['frequency_of_execution'] != 0:
	parameters['frequency_of_execution'] = 1.0/parameters['frequency_of_execution']

# List with velocities for each movement of the robot.
speeds = Speeds( )

mem = Blackboard( ) # Creating shared memory

land = Landmark(speeds) # Creating landmark object

ball = Ball(speeds) # Creating landmark object

# Creating robot objects
observation = []
robots = []
newrobots = []
for __ in xrange(parameters["robot_numbers"]):
	newrobots.append(Robots(speeds, observation))

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
		
	#	 datarobots = readDataRobots(mem, parameters["robot_numbers"])
		datarobots = [
			[1, 5, 0, 0],
			[1, 5, 0, 1],
			[2, 5, 0, 2],
			[2, 5, 0, 3],
			[2, 5, 0, 4],
			[1, 5, 0, 5],
			[2, 5, 0, 6],
			[1, 5, 0, 7],
			[2, 5, 0, 8],
			[2, 5, 0, 9],
			[2, 5, 0, 10],
			
			[1, 0, 0, 0],
			[1, 1, 1, 1],
			[1, 2, 2, 2],
			[2, 3, 3, 3],
			[1, 4, 4, 4],
			[2, 5, 5, 5],
			[1, 6, 6, 6],
			[1, 7, 7, 7],
			[1, 8, 8, 8],
			[2, 9, 9, 9],
			[2, 10, 10, 10],
			
			[2, 10, 10, 0],
			[2, 9, 9, 1],
			[2, 8, 8, 2],
			[2, 7, 7, 3],
			[3, 6, 6, 4],
			[3, 5, 5, 5],
			[2, 4, 4, 6],
			[3, 3, 3, 7],
			[3, 2, 2, 8],
			[3, 1, 1, 9],
			[2, 0, 0, 10],
			
			[2, 5, 5, 0],
			[3, 7, 6, 1],
			[3, 9, 7, 2],
			[2, 11, 8, 3],
			[2, 13, 9, 4],
			[3, 15, 10, 5],
			[3, 15, 10, 6],
			[2, 15, 10, 7],
			[3, 15, 10, 8],
			[3, 15, 10, 9],
			[3, 15, 10, 10],
		]
		
		if datarobots != []:
			oldtime = datarobots[0][3]
			robotstesting = copy(robots)
			
			obs = 0
			while(obs < len(datarobots)):
				print "Entrou", len(datarobots), "passo:", obs
				if oldtime != datarobots[obs][3]:
					print "Novos dados"
					robotstesting = copy(robots)
					oldtime = datarobots[obs][3]
				
				if robotstesting == []:
					print "Novo Robô"
					newrobots[0].insertObservation(datarobots[obs])
					robots.append(newrobots.pop(0))
					datarobots.remove(datarobots[obs])
					continue
				
				observation = datarobots[obs]
				
				print 'remove todos os elementos de robôs de cores erradas'
				
				sort(robots, reverse = True)
				
				if datarobots[0].weight < float(parameters['relation_measurement_and_robot'])/100:
					if newrobots != []:
						newrobots[0].insertObservation(datarobots[obs])
						robots.append(newrobots.pop(0))
						datarobots.remove(datarobots[obs])
						obs -= 1
						continue
				else:
					datarobots[0].insertObservation(datarobots[obs])
					datarobots.pop(0)
					datarobots.remove(datarobots[obs])
					obs -= 1
				
				obs += 1
						
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