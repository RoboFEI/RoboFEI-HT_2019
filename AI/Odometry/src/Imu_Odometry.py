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

        #######################################Calculo da matriz rotação do corpo da imu para o referencial######

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

        self.R_B_I = R_i_v1 * R_v1_v2 * R_v2_B  #Matriz rotação do corpo da imu para o referencial

#################Leitura dos valores da IMU############################

    def Get_IMU_BKB(self, Item):
        g = [[0], [0], [9.8]]           #Forças externas
        Valbkb = []

        for i in Item:                  #Aquisita valores da blackboard da IMU, com valores em função da gravidade
            Valbkb.append(self.bkb.read_int(self.mem, i))

        Valbkb.T                        #Matriz transposta
        Valbkb *= 9.8                   #Transformar a aceleração de gravidade para m/s
        self.aI = self.R_B_I*Valbkb+g   #Calcula a aceleração em relação ao referencial

#################Calculo da posição utilizando valores da IMU###########

    def IMU_CALC_POS(self):
        tf = time.time()                #Verifica o tempo atual (sec. Ponto flutuante). Nota: Nem todos os sistemas apresentam uma precisão alta em relação a tempo
        T = tf - ti                     #Calculo do período de calculo

        self.Vx += T*(self.aI[0])       #Calculo da velocidade do movimento no eixo x. (m/s)
        self.Rx += T*self.Vx            #Calculo de posição relativa do robô no eixo x. (m)

        self.Vy += T*(self.aI[1])       #Calculo da velocidade do movimento no eixo y. (m/s)
        self.Ry += T*self.Vy            #Calculo de posição relativa do robô no eixo y. (m)

        ti = tf

        os.system('cls')
        print('X = %f, Y = %f'%(Rx, Ry))
#################Programa principal#####################################

Imu = Imu()
IMU = [ 'IMU_ACCEL_X',
        'IMU_ACCEL_Y',
        'IMU_ACCEL_Z']
while (1):
    I = Imu.bkb.read_int(Imu.mem, 'WALK_PHASE')
    if I == 1:
        ti = time.time()
        while(1):
            Imu.Get_IMU_BKB(IMU)
            Imu.IMU_CALC_POS()
