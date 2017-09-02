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
		
		__t = sym.symbols("t") # Declaring variable time
		
		p_x, p_y = sym.symbols("p_x, p_y")
		v_x, v_y = sym.symbols("v_x, v_y")
		a_x, a_y = sym.symbols("a_x, a_y")
		vr_x, vr_y, omegar = sym.symbols("vr_x, vr_y, \\omega\ r")
		R_p, R_v, R_a = sym.symbols("R_p R_v R_a")
		
		self.__B = sym.Matrix([
			[-__t*vr_x, 0, 0],
			[0, -__t*vr_y, 0],
			[0, 0, 0],
			[0, 0, 0],
			[0, 0, 0],
			[0, 0, 0],
		])
		
		self.__R = sym.Matrix(sym.Identity(6)*1000)
		
		np_x = p_x -__t*vr_x*sym.sin(sym.pi/2 - __t*omegar) - __t*vr_y*sym.cos(sym.pi/2 + __t*omegar)
		np_y = p_y -__t*vr_x*sym.cos(sym.pi/2 - __t*omegar) - __t*vr_y*sym.sin(sym.pi/2 + __t*omegar)
		# np_x, np_y = sym.symbols("np_x np_y")
		
		# Para movimentos
		Z = sym.Matrix([
			[p_x*sym.cos(omegar*__t)+p_y*sym.sin(omegar*__t) - __t*vr_x],
			[-p_x*sym.sin(omegar*__t)+p_y*sym.cos(omegar*__t) - __t*vr_y],
			[v_x*sym.cos(__t*omegar)+v_y*sym.sin(__t*omegar)],
			[-v_x*sym.sin(__t*omegar)+v_y*sym.cos(__t*omegar)],
			[a_x*sym.cos(__t*omegar)+a_y*sym.sin(__t*omegar)],
			[-a_x*sym.sin(__t*omegar)+a_y*sym.cos(__t*omegar)],
		])
		
		u = sym.Matrix([
			[vr_x],
			[vr_y],
			[sym.cos(omegar*__t)],
			[sym.sin(omegar*__t)],
		])
		
		B = sym.Matrix([
			[-__t, 0, p_x, p_y],
			[0, -__t, p_y, -p_x],
			[0, 0, v_x, v_y],
			[0, 0, v_y, -v_x],
			[0, 0, a_x, a_y],
			[0, 0, a_y, -a_x],
		])
		
		B, sym.Matrix([
			[p_x, 0, 0, 0, 0, 0],
			[p_y, 1, 0, 0, 0, 0],
			[0, 0, v_x, 0, 0, 0],
			[0, 0, 0, v_y, 0, 0],
			[0, 0, 0, 0, a_x, 0],
			[0, 0, 0, 0, 0, a_y],
		]).inv() * sym.Matrix([
			[0, 0, 0, p_y],
			[0, 0, 0, -p_x],
			[0, 0, 0, v_y],
			[0, 0, 0, -v_x],
			[0, 0, 0, a_y],
			[0, 0, 0, -a_x],
		])
		
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