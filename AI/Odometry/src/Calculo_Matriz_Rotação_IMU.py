#coding: utf-8

import sympy as sy
import numpy as np

cosY =  sy.Symbol('cos(-Y)')   #Yaw
sinY =  sy.Symbol('sin(-Y)')
cosP =  sy.Symbol('cos(-P)')   #Pitch
sinP =  sy.Symbol('sin(-P)')
cosR =  sy.Symbol('cos(-R)')   #roll
sinR =  sy.Symbol('sin(-R)')

R_i_v1 = sy.Matrix([[ cosY, sinY, 0],
                    [-sinY, cosY, 0],
                    [  0,    0,   1]])

R_v1_v2 = sy.Matrix([[cosP,  0, -sinP],
                     [ 0,    1,   0  ],
                     [sinP,  0,  cosP]])

R_v2_B = sy.Matrix([[1,    0 ,    0 ],
                    [0,  cosR,  sinR],
                    [0, -sinR, cosR]])

MR = R_i_v1 * R_v1_v2 * R_v2_B

T = sy.Matrix([1, 0, 1])
T.T

print(np.matrix(MR))
print(T)
