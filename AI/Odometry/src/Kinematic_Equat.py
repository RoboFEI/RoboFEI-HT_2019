#coding: utf-8

import sympy as sy
import numpy as np

#L4 = 93.0
#L5 = 93.0
#Lf = 33.5
#Ltx = 5
#Lty = 122.2
#Ltz = 37

s7 = sy.Symbol('s7')
s9 = sy.Symbol('s9')
s11 = sy.Symbol('s11')
s13 = sy.Symbol('s13')
s15 = sy.Symbol('s15')
s17 = sy.Symbol('s17')
c7 = sy.Symbol('c7')
c9 = sy.Symbol('c9')
c11 = sy.Symbol('c11')
c13 =sy.Symbol('c13')
c15 = sy.Symbol('c15')
c17 = sy.Symbol('c17')
sabc = sy.Symbol('sabc')
cabc = sy.Symbol('cabc')
cab = sy.Symbol('cab')
sab = sy.Symbol('sab')
Px = sy.Symbol('Px')
Py = sy.Symbol('Py')
Pz = sy.Symbol('Pz')

L4 = sy.Symbol('L4')
L5 = sy.Symbol('L5')
Lf = sy.Symbol('Lf')
Ltx = sy.Symbol('Ltx')
Lty = sy.Symbol('Lty')
Ltz = sy.Symbol('Ltz')


T_06 = sy.Matrix([[(s7*sabc-c7*s11*cabc)*c15-(c7*c11*s15), -(s7*sabc-c7*s11*cabc)*s15-c7*c11*c15, s7*cabc+c7*s11*sabc, ((L4*s9+L5*sab)*s7-(L4*c9+L5*cab)*c7*s11)],[(-c7*sabc-s7*s11*cabc)*c15-s7*c11*s15, -(-c7*sabc-s7*s11*cabc)*s15-s7*c11*c15, -c7*cabc+s7*s11*sabc, (-(L4*s9+L5*sab)*c7-(L4*c9+L5*cab)*s7*s11)],[-s11*s15+c11*c15*cabc, -s11*c15-c11*s15*cabc, -c11*sabc, (L4*c9+L5*cab)*c11], [0, 0, 0, 1]])
T_c0 = sy.Matrix([[0, -1, 0, -Ltx],[0, 0, -1, -Lty],[1, 0, 0, Ltz], [0, 0, 0, 1]])
T_6f = sy.Matrix([[1, 0, 0, Lf],[0, 1, 0, 0],[0, 0, 1, 0], [0, 0, 0, 1]])

T = T_c0*T_06*T_6f

print (np.matrix(T))
