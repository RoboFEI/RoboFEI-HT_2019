# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append("../include")
sys.path.append("../src")

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from Basic import * # Class with implementations and basic variables

## Class to Speeds
# Class responsible for managing the robot's possible speeds (me).
class Speeds( ):
	
	# ---- Variables ----
	
	## __movementslist
	# Velocity list of robot movements.
	__movementslist = []
	
	## __B
	# Speed matrix $B_t$.
	__B = None
	
	## __R
	# Speed error matrix $R_t$.
	__R = None
	
	## Constructor Class
	# Initializes basic network parameters and creates standard speeds.
	def __init__(self):
		self.__movementslist.append({
			"U": sym.Matrix([
				[0, 0, 0,],
				[0, 0, 0,],
				[0, 0, 0,],
				[0, 0, 0,],
				[0, 0, 0,],
				[0, 0, 0,],
			]),
		
			"R": sym.Matrix(sym.Identity(6)*0)
		})
		
		self.__B = sym.Matrix([
			[0, 0, 0,],
			[0, 0, 0,],
			[0, 0, 0,],
			[0, 0, 0,],
			[0, 0, 0,],
			[0, 0, 0,],
		])
		
		self.__R = sym.Matrix(sym.Identity(6)*1000)
		
	## update
	# Adds average robot speeds or upgrades to speeds.
	# @param vector Observed speed.
	def update(self, vector):
		if vector[0] + 1 > len(self.__movementslist):
			while vector[0] + 1 > len(self.__movementslist):
				self.__movementslist.append(
					{
						"U": copy(self.__B),
						"R": copy(self.__R),
					}
				)
		
		self.__movementslist[vector[0]]["U"] = vector[1]
		self.__movementslist[vector[0]]["R"] = vector[2]
	
	## __getitem__
	# Returns the dictionary of motion vectors.
	# @param x Vector position to be accessed.
	# @return Returns the dictionary that will be used.
	def __getitem__(self, x):
		return self.__movementslist[x]