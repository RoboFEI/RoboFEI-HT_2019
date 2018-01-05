#coding: utf-8

import os
import sys
import numpy as np
import time

sys.path.append('../../BlackBoard/src/')
from SharedMemory import SharedMemory
from ConfigParser import ConfigParser

#############################################################################33

    class Imu:
        def __init__(self):
            config = ConfigParser()
            config,read('../../Control/Data/config.ini')
            self.mem_key = int(config.get('Communication', 'no_player_robofei'))*100

            self.bkb = SharedMemory()
            self.mem = self.bkb.shd_constructor(self.mem_key)

#################Leitura dos valores da IMU############################

        def Get_IMU_BKB(self, Item):
            self.Valbkb = []

            for i in Item:
                self.Valbkb.append(self.bkb.read_int(self.mem, i))

#################Calculo da posição utilizando valores da IMU###########

        def IMU_CALC_POS(self):
            tf = time.time()
            T = tf - ti

            self.V += T*(self.Valbkb[0])    #Calculo da velocidade do movimento no eixo x
            self.R += T*self.V              #Calculo de posição relativa do robô no eixo x

            self.V += T*(self.Valbkb[1])    #Calculo da velocidade do movimento no eixo y
            self.R += T*self.V              #Calculo de posição relativa do robô no eixo y

            ti = tf
#################Programa principal#####################################

    Imu = Imu()

    IMU = [ 'IMU_ACCEL_X',
            'IMU_ACCEL_Y']

    I = self.bkb.read_int(self.mem, PHASE)
    if I == 1
        ti = time.time()
        while(1):
            Imu.Get_IMU_BKB(IMU)
            Imu.IMU_CALC_POS()
