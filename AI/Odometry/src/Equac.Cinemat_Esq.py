#coding: utf-8

import sympy as sy
import numpy as np

#L4 = 93.0
#L5 = 93.0
#Lf = 33.5
#Ltx = 5
#Lty = 122.2
#Ltz = 37

O7 = sy.Symbol('O7')
O9 = sy.Symbol('O9')
O11 = sy.Symbol('O11')
O13 = sy.Symbol('O13')
O15 = sy.Symbol('O15')
O17 = sy.Symbol('O17')
L4 = sy.Symbol('L4')
L5 = sy.Symbol('L5')
T = sy.ones(6, 4)

DLL = sy.Matrix([[0	    , 0,  0, 	O7       ], 
			[-np.pi/2, 0,  0, O11-np.pi/2], 
			[-np.pi/2, 0,  0, 	O9	    ],
			[0	    ,93,  0,   O13      ],
			[0       ,93,  0, 	O17	    ],
			[np.pi/2 , 0,  0,   O15	    ]])
for i in range(6):
	T = T*sy.Matrix([[sy.cos(DLL[i, 3]), -sy.sin(DLL[i, 3]), 0, DLL[i, 1]],
				  [sy.sin(DLL[i, 3])*np.cos(DLL[i, 0]), sy.cos(DLL[i, 3])*np.cos(DLL[i, 0]), -np.sin(DLL[i, 0]),  0], 
				  [sy.sin(DLL[i, 3])*np.sin(DLL[i, 0]), sy.cos(DLL[i, 3])*np.sin(DLL[i, 0]), -sy.cos(DLL[i, 0]),  0],
				  [0, 0, 0, 1]])

print (sy.Matrix(T))
