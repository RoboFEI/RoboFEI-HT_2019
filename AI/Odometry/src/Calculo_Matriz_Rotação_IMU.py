#coding: utf-8

import sympy as sy
import numpy as np

Y =  sy.Symbol('Y')   #Yaw
P =  sy.Symbol('P')   #Pitch
R =  sy.Symbol('R')   #roll

R_i_v1 = sy.Matrix([[ sy.cos(-Y), sy.sin(-Y), 0],
		            [-sy.sin(-Y), sy.cos(-Y), 0],
		            [  0,    0,   1]])

R_v1_v2 = sy.Matrix([[ sy.cos(-P),  0, -sy.sin(-P)],
		             [ 0,    1,   0  ],
		             [sy.sin(-P),  0,  sy.cos(-P)]])

R_v2_B = sy.Matrix([[1,     0   ,       0 ],
		            [0,  sy.cos(-R),  sy.sin(-R)],
		            [0, -sy.sin(-R), sy.cos(-R)]])

MR = R_i_v1 * R_v1_v2 * R_v2_B

T = sy.Matrix([1, 0, 1])
T.T

print(np.matrix(MR))
print(T)
