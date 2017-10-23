#coding: utf-8

import numpy as np

LEG_SIDE_OFFSET = 37.0
THIGH_LENGTH = 93.0
CALF_LENGTH = 93.0
ANKLE_LENGTH = 33.5
LEG_LENGTH = 219.5
pi = 180

T = np.ones((4, 4))				#Matriz transformação de 0 ao ponto estudado
Mti = np.ones((4,4))

Pdh = np.array([[ pi,  0  , 0, 20],	#Caso a cinemática do robô mude, é necessário modificar os parâmetros de cinemática 
		[-pi,  0  , 0, 20],	#nesta matriz.
		[  0,  37 , 0, 35],
	        [  0,  93 , 0, 25],
	        [ pi,   0 , 0, 40],
		[  0,  93 , 0, 10]])

nrow, ncol = np.shape(Pdh)		

i = 0
while (i!=nrow):	
	Mti =          ([[np.cos(Pdh[i][3])                  ,-np.sin(Pdh[i][3])                  ,0                  ,Pdh[i][1]                  ],
	             	[np.sin(Pdh[i][3])*np.cos(Pdh[i][0]), np.cos(Pdh[i][3])*np.cos(Pdh[i][0]), -np.sin(Pdh[i][0]),-np.sin(Pdh[i][0])*Pdh[i][2]],
			[np.cos(Pdh[i][3])                  ,-np.sin(Pdh[i][3])                  ,0                  , np.cos(Pdh[i][0])*Pdh[i][2]],
	   	      	[0                                  ,0                                   ,0                  ,1                          ]])

	T *= Mti 
	i+=1

print (T)

