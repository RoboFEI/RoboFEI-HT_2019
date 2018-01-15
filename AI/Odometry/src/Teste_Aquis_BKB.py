#coding: utf-8

import os
import sys
sys.path.append('../../Blackboard/src/')	#adicionando caminho para programa em outro diretório
from SharedMemory import SharedMemory		#Importa a classe do arquivo SharedMemory

from ConfigParser import ConfigParser		#Importando a classe ConfigParser
import numpy as np
import time as time
##########################################################################################

class Odometry:

	def __init__(self):

		# instantiate:
		config = ConfigParser()								#Instanciando um objeto a classe para ler arquivos 

		# looking for the file config.ini:
		config.read('../../Control/Data/config.ini')

		self.mem_key = int(config.get('Communication', 'no_player_robofei'))*100	#Lendo a comunicação e o número do robô 
		#Instantiate the BlackBoard's class:
		self.bkb = SharedMemory()							#Instanciando o obj a classe de memória compartilhada
		self.mem = self.bkb.shd_constructor(self.mem_key)
		self.Var_Mot = []
		
##################Leitura dos valores da IMU###############################################

	def Get_Bkb_Values(self, Item1, Item2):
 
		self.Mot = []	#Cria vetor que vai acessar e ler os valores dos motores da blackboard
		self.IMU = []
		k = 0
		
		for i in Item1:
			self.Mot.append(((self.bkb.read_int(self.mem, i)-self.Mot_Var[k])*0.005113269 + 0.52359877559))
			k += 1
		print self.Mot	
		for j in Item2:
			self.IMU.append(self.bkb.read_float(self.mem, j))	
		self.Mov =self.bkb.read_int(self.mem, 'WALK_PHASE')
			
###################Apresentaçao dos resultados#############################################
	def Mostra(self, Item1, Item2):
            for k in range(len(Item1)):
                print("Motor %d = %f" % (k, self.Mot[k]))
            for I in range(len(Item2)):
                print("IMU %d = %f" % (I, self.IMU[I]))
            print("phase: %f"%(self.Mov))
            time.sleep(0.1) 

            
###################Programa principal#######################################################
Odometry = Odometry()

Motores = ['Motor_Read_7',  #0						
		'Motor_Read_8',  #1
		'Motor_Read_9',  #2
		'Motor_Read_10', #3
		'Motor_Read_11', #4
		'Motor_Read_12', #5
		'Motor_Read_13', #6
		'Motor_Read_14', #7
		'Motor_Read_15', #8
		'Motor_Read_16', #9
		'Motor_Read_17', #10
		'Motor_Read_18'] #11
ACELER = [ 'IMU_ACCEL_X',
        'IMU_ACCEL_Y',
        'IMU_ACCEL_Z']

#######verificacao de erro inicial da posicao dos motores###
Odometry.Mot_Var = []	
for i in Motores:
	Odometry.Mot_Var.append(Odometry.bkb.read_int(Odometry.mem, i)*0.005113269 + 0.52359877559)
	
for i in range(len(Motores)):
	Odometry.Mot_Var[i] -= 512 #Variacao da posicao inicial com a teorica 
	
######Chamada dos calculos###########

while(1):
	Odometry.Get_Bkb_Values(Motores, ACELER)
	Odometry.Mostra(Motores, ACELER)
	
