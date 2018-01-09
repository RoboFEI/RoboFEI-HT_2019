#coding: utf-8

import os
import sys
import numpy as np
import sympy as sy
import time
sys.path.append('../../Blackboard/src/')
from SharedMemory import SharedMemory
from ConfigParser import ConfigParser

#############################################################################

class Imu:
    def __init__(self):
        config = ConfigParser()
        config.read('../../Control/Data/config.ini')
        self.mem_key = int(config.get('Communication', 'no_player_robofei'))*100

        self.bkb = SharedMemory()
        self.mem = self.bkb.shd_constructor(self.mem_key)
        
        self.Vx = 0
        self.Vy = 0
        self.Rx = 0
        self.Ry = 0 

        #######################################Calculo da matriz rotação do corpo da imu para o referencial######

        self.Y =  sy.Symbol('self.Y')   #Yaw
        self.P =  sy.Symbol('self.P')   #Pitch
        self.R =  sy.Symbol('self.R')   #roll

        R_i_v1 = sy.Matrix([[ sy.cos(self.Y), sy.sin(self.Y), 0],
                            [-sy.sin(self.Y), sy.cos(self.Y), 0],
                            [  0        ,     0     , 1]])

        R_v1_v2 = sy.Matrix([[sy.cos(self.P),  0, -sy.sin(self.P)],
                             [ 0        ,  1,          0    ],
                             [sy.sin(self.P),  0,  sy.cos(self.P)   ]])

        R_v2_B = sy.Matrix([[1,        0   ,       0    ],
                            [0,  sy.cos(self.R),  sy.sin(self.R)],
                            [0, -sy.sin(self.R), sy.cos(self.R)]])

        self.R_i_b = R_i_v1 * R_v1_v2 * R_v2_B



#################Leitura dos valores da IMU############################

    def Get_IMU_BKB(self, Acc, Euler):
        g = [[0], [0], [9.8]]           #Forças externas
        ValAcc = []
        ValEuler = []

        for i in Acc:                  #Aquisita valores da IMU, com valores em função da gravidade
            ValAcc.append(self.bkb.read_float(self.mem, i))
        for k in Euler:                  #Aquisiçao da orientaçao do corpo da IMU
            ValEuler.append(self.bkb.read_float(self.mem, k))
            
        self.R_i_b = self.R_i_b.subs([(self.Y , -ValEuler[2]), (self.P , -ValEuler[1]), (self.R , -ValEuler[0])])#Substitui os valores na matriz

        ValAcc = np.array(ValAcc)*9.8                   #Transforma gravidade[g] para m/s
        np.transpose(ValAcc)                        #Matriz transposta

        self.aI = np.multiply(self.R_i_b, ValAcc)+g   #Calcula a aceleração em relação ao referencial

#################Calculo da posição utilizando valores da IMU###########

    def IMU_CALC_POS(self):
        tf = time.time()                #Verifica o tempo atual (sec. Ponto flutuante). Nota: Nem todos os sistemas apresentam uma precisão alta em relação a tempo
        T = tf - self.ti                     #Calculo do período de calculo
        
        self.aI = np.asarray(self.aI, np.float)[0]

        self.Vx += T*(self.aI[0])       #Calculo da velocidade do movimento no eixo x. (m/s)
        self.Rx += T*self.Vx            #Calculo de posição relativa do robô no eixo x. (m)

        self.Vy += T*(self.aI[1])       #Calculo da velocidade do movimento no eixo y. (m/s)
        self.Ry += T*self.Vy            #Calculo de posição relativa do robô no eixo y. (m)

        self.ti = tf    

        os.system('cls')
        print('X = %f, Y = %f'%(self.Rx, self.Ry))
#################Programa principal#####################################

Imu = Imu()

ACELER = [ 'IMU_ACCEL_X',
        'IMU_ACCEL_Y',
        'IMU_ACCEL_Z']
        
EULER = ['IMU_EULER_X',
		'IMU_EULER_Y',
		'IMU_EULER_Z']
		
while (1):
    I = Imu.bkb.read_float(Imu.mem, 'WALK_PHASE')
    #if I != 0:
    Imu.ti = time.time()
    while(1):
        Imu.Get_IMU_BKB(ACELER, EULER)
        Imu.IMU_CALC_POS()
        
        
        
        
        
        
        
        
        
        
        
        
