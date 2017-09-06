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
	
	## __u
	# Speed matrix $u_t$.
	__u = None
	
	## __R
	# Speed error matrix $R_t$.
	__R = None
	
	## Constructor Class
	# Initializes basic network parameters and creates standard speeds.
	def __init__(self):
		self.__movementslist.append({
			"speed": sym.Matrix([
				[0], # speed in x (vr_x)
				[0], # speed in y (vr_y)
				[0], # angular velocity (ωr)
			]),
				
			"x_speed": sym.Matrix([
				[0], # v_x
				[0], # v_y
				[0], # a_x
				[0], # a_y
			]),
				
			"U": sym.Matrix([
				[0], # vr_x
				[0], # vr_y
				[1], # cos(ωr*t)
				[0], # sin(ωr*t)
			]),
		
			"R": sym.Matrix(sym.Identity(6)*0)
		})
		
		__t = sym.symbols("t") # Declaring variable time
		
		p_x, p_y, v_x, v_y, a_x, a_y = sym.symbols("p_x, p_y, v_x, v_y, a_x, a_y") # Object state variables
		
		# Robot Speed Variables
		vr_x, vr_y, omegar = sym.symbols("vr_x, vr_y, \\omega\ r")
		
		# Kalman filter matrices
		self.__u = sym.Matrix([
			[vr_x],
			[vr_y],
			[sym.cos(omegar*__t)],
			[sym.sin(omegar*__t)],
		])
		
		self.__R = sym.Matrix(sym.Identity(6)*1000)
		
	## update
	# Adds average robot speeds or upgrades to speeds.
	# @param vector Observed speed.
	def update(self, vector):
		R_p = (p_x**2 + p_y**2)**0.5 # position vector module
		
		if vector[0] + 1 > len(self.__movementslist):
			while vector[0] + 1 > len(self.__movementslist):
				self.__movementslist.append({
					"speed": sym.Matrix([
						[0], # speed in x (vr_x)
						[0], # speed in y (vr_y)
						[0], # angular velocity (ωr)
					]),
	
					"x_speed": sym.Matrix([
						[0], # v_x
						[0], # v_y
						[0], # a_x
						[0], # a_y
					]),
	
					"U": sym.Matrix([
						[0], # vr_x
						[0], # vr_y
						[1], # cos(ωr*t)
						[0], # sin(ωr*t)
					]),
	
					"R": copy(self.__R)
				})
	
		self.__movementslist[vector[0]]["x_speed"] = vector[1]
		self.__movementslist[vector[0]]["R"] = vector[2]
	
		# Calculating ωr of the robot
		self.__movementslist[vector[0]]["speed"][2] = ((-a_x * abs(p_x))/(p_x * R_p)).subs([
			[p_x, self.__movementslist[vector[0]]["x_speed"][0]],
			[p_y, self.__movementslist[vector[0]]["x_speed"][1]],
			[a_x, self.__movementslist[vector[0]]["x_speed"][4]],
		])
	
		# Calculating vr_x of the robot
		self.__movementslist[vector[0]]["speed"][0] = (-omegar*p_x - v_y).subs([
			[p_x, self.__movementslist[vector[0]]["x_speed"][0]],
			[v_y, self.__movementslist[vector[0]]["x_speed"][3]],
			[omegar, self.__movementslist[vector[0]]["speed"][2]]
		])
	
		# Calculating vr_y of the robot
		self.__movementslist[vector[0]]["speed"][1] = (-omegar*p_y-v_x).subs([
			[p_y, self.__movementslist[vector[0]]["x_speed"][1]],
			[v_x, self.__movementslist[vector[0]]["x_speed"][2]],
			[omegar, self.__movementslist[vector[0]]["speed"][2]]
		])
	
		# Calculating matrix U
		self.__movementslist[vector[0]]["U"] = self.__u.subs([
			[vr_x, self.__movementslist[vector[0]]["speed"][0]],
			[vr_y, self.__movementslist[vector[0]]["speed"][1]],
			[omegar, self.__movementslist[vector[0]]["speed"][2]],
		])
	
	## __getitem__
	# Returns the dictionary of motion vectors.
	# @param x Vector position to be accessed.
	# @return Returns the dictionary that will be used.
	def __getitem__(self, x):
		return self.__movementslist[x]