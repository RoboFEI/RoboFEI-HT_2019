#coding: utf-8

import sympy as sy
import numpy as np

#L4 = 93.0
#L5 = 93.0
#Lf = 33.5
#Ltx = 5
#Lty = 122.2
#Ltz = 37

r11 = sy.Symbol('r11')
r12 = sy.Symbol('r21')
r13 = sy.Symbol('r31')
r21 = sy.Symbol('r21')
r22 = sy.Symbol('r22')
r23 = sy.Symbol('r23')
r31 = sy.Symbol('r31')
r32 = sy.Symbol('r32')
r33 = sy.Symbol('r33')
Px = sy.Symbol('Px')
Py = sy.Symbol('Py')
Pz = sy.Symbol('Pz')
L4 = sy.Symbol('L4')
L5 = sy.Symbol('Lt5')
Lf = sy.Symbol('Lf')
Ltx = sy.Symbol('Ltx')
Lty = sy.Symbol('Lty')
Ltz = sy.Symbol('Ltz')

T_06 = sy.Matrix([[r11, r12, r13, Px],[r21, r22, r23, Py],[r31, r32, r33, Pz], [0, 0, 0, 1]])
T_0c = sy.Matrix([[0, -1, 0, -Ltx],[0, 0, -1, -Lty],[1, 0, 0, Ltz], [0, 0, 0, 1]])
T_6f = sy.Matrix([[1, 0, 0, Lf],[0, 1, 0, 0],[0, 0, 1, 0], [0, 0, 0, 1]])

T = T_0c*T_06*T_6f

print (np.matrix(T))
