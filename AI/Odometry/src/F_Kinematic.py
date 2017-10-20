#coding: utf-8

import numpy as np

class F_Kinematic:

	def __init__(self):
		self.LEG_SIDE_OFFSET = 37.0
		self.THIGH_LENGTH = 93.0
		self.CALF_LENGTH = 93.0
		self.ANKLE_LENGTH = 33.5
		self.LEG_LENGTH = 219.5
		self.pi = 180

		self.Parm_DH = np.array([[ pi,  0, 0, th+pi],	#Indicar os indices de 'th'. 
					 [-pi,  0, 0, th-pi],
					 [  0, L4, 0, th   ],
					 [  0, L5, 0, th   ],
					 [ pi,  0, 0, th   ],
					 [  0, Lf, 0, th   ])

		self.MTr = np.array([[    cos(Th),            -sin(th),         0,            a      ],
				     [sin(Th)*cos(alfa), cos(th)*cos(alfa), -sin(alfa), -sin(alfa)*di],
				     [    cos(Th),            -sin(th),         0,       cos(alfa)*di],
				     [       0,                   0,            0,            1      ])
		
	def Forward_Kinematic(self):
		
	
