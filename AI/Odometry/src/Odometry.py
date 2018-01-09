#coding: utf-8

import os
import sys
import numpy as np
import time
sys.path.append('../../Blackboard/src/')	#adicionando caminho para programa em outro diretório
from SharedMemory import SharedMemory		#Importa a classe do arquivo SharedMemory
from ConfigParser import ConfigParser		#Importando a classe ConfigParser

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

		self.posx = 0
		self.posy = 0
		self.j = 0		#Se j for par, a perna direita está em movimento, se for ímpar, a perna esquerda está em movimento
		self.Posx_i_R = 0
		self.Posy_i_R = 0
		self.Posx_i_L = 0
		self.Posy_i_L = 0

##################Leitura dos valores da IMU###############################################

	def Get_Bkb_Values(self, Item1, Item2):

		self.Mot = []	#Cria vetor que vai acessar e ler os valores dos motores da blackboard
		self.IMU = []	#Cria vetor que vai acessar e ler os valores da IMU da blackboard

		for i in Item1:		#Lê os valores dos motores, convertendo para graus e adiciona no vetor MOT
			self.Mot.append((self.bkb.read_int(self.mem, i))*0.005113269 + 0.52359877559)

		for j in Item2:		#Lê valores da IMU e adiciona no vetor IMU
			self.IMU.append(self.bkb.read_float(self.mem, j))

##################Calculo cinemática########################################################

	def Kinematics_Calc(self):

		L4 = 93.0
		L5 = 93.0
		Lf = 33.5
		s7 = np.sin(self.Mot[0])
		s8 = np.sin(self.Mot[1])
		s9 = np.sin(self.Mot[2])
		s10 = np.sin(self.Mot[3])
		s11 = np.sin(self.Mot[4])
		s12 = np.sin(self.Mot[5])
		s13 = np.sin(self.Mot[6])
		s14 = np.sin(self.Mot[7])
		s15 = np.sin(self.Mot[8])
		s16 = np.sin(self.Mot[9])
		s17 = np.sin(self.Mot[10])
		s18 = np.sin(self.Mot[11])
		c7 = np.cos(self.Mot[0])
		c8 = np.cos(self.Mot[1])
		c9 = np.cos(self.Mot[2])
		c10 = np.cos(self.Mot[3])
		c11 = np.cos(self.Mot[4])
		c12 = np.cos(self.Mot[5])
		c13 = np.cos(self.Mot[6])
		c14 = np.cos(self.Mot[7])
		c15 = np.cos(self.Mot[8])
		c16 = np.cos(self.Mot[9])
		c17 = np.cos(self.Mot[10])
		c18 = np.cos(self.Mot[11])
		sabc = np.sin(self.Mot[2]+self.Mot[6]+self.Mot[10])
		cabc = np.cos(self.Mot[2]+self.Mot[6]+self.Mot[10])
		cab = np.cos(self.Mot[2]+self.Mot[6])
		sab = np.sin(self.Mot[2]+self.Mot[6])
		slabc = np.sin(self.Mot[3]+self.Mot[7]+self.Mot[11])
		clabc = np.cos(self.Mot[3]+self.Mot[7]+self.Mot[11])
		clab = np.cos(self.Mot[3]+self.Mot[7])
		slab = np.sin(self.Mot[3]+self.Mot[7])

########Cinemática_Perna_Direita#######

		r11 = -((-c7*sabc-s7*s11*cabc)*c15-s7*c11*s15)
		r12 = -(-(-c7*sabc-s7*s11*cabc)*s15-s7*c11*c15)
		r13 = -(-c7*cabc+s7*s11*sabc)

		r21 = -(-s11*s15+c11*c15*cabc)
		r22 = -(-s11*c15-c11*s15*cabc)
		r23 = -(-c11*sabc)

		r31 = (s7*sabc-c7*s11*cabc)*c15-(c7*c11*s15)
		r32 = -(s7*sabc-c7*s11*cabc)*s15-c7*c11*c15
		r33 = s7*cabc+c7*s11*sabc

		Prx = ((L4*s9+L5*sab)*s7-(L4*c9+L5*cab)*c7*s11)
		Pry = (-(L4*s9+L5*sab)*c7-(L4*c9+L5*cab)*s7*s11)
		#Prz = ((L4*c9+L5*cab)*c11)

########Cinemática_Perna_Esquerda#######

		l11 = -((-c8*sabc-s8*s12*cabc)*c16-s8*c12*s16)
		l12 = -(-(-c8*sabc-s8*s12*cabc)*s16-s8*c12*c16)
		l13 = -(-c8*cabc+s8*s12*sabc)

		l21 = -(-s12*s16+c12*c16*cabc)
		l22 = -(-s12*c16-c12*s16*cabc)
		l23 = -(-c12*sabc)

		l31 = (s8*sabc-c8*s12*cabc)*c16-(c8*c12*s16)
		l32 = -(s8*sabc-c8*s12*cabc)*s16-c8*c12*c16
		l33 = s8*cabc+c8*s12*sabc

		Plx = ((L4*s10+L5*sab)*s8-(L4*c10+L5*cab)*c8*s12)
		Ply = (-(L4*s10+L5*sab)*c8-(L4*c10+L5*cab)*s8*s12)
		#Plz = ((L4*c10+L5*cab)*c12)

##################Calculo_de_Posição########################################################

	def Position_Calc(self):
		if self.j%2: 								#Calculo de posição a partir do movimento da perna direita
			Var_Posx_L = self.Plx - self.Posx_i_L 	#Se não houver o calculo de variação e ela ocorrer no semiplano negativo, ao invés de somar a posição, irá decrementá-la, gerando um erro de cálculo
			Var_Posy_L = self.Ply - self.Posy_i_L
			self.posx = self.posx + Var_Posx_L
			self.posy = self.posy + Var_Posy_L
			self.Posx_i_R = self.Prx
			self.Posy_i_R = self.Pry
			self.j-=1
		else: 										#Calculo de posição a partir do movimento da perna esquerda
			Var_Posx_R = self.Prx - self.Posx_i_R
			Var_Posy_R = self.Pry - self.Posy_i_R
			self.posx = self.posx + Var_Posx_R
			self.posy = self.posy + Var_Posy_R
			self.Posx_i_L = self.Plx
			self.Posy_i_L= self.Ply
			self.j+=1

##################Print_dos_valores########################################################

	def Show_Position(self):

		os.system('cls')		#Limpa a tela do terminal antes de escrever os novos valores
    	print("\nposx = %f \t posy = %f" % (self.posx, self.posy))	#Apresenta os valores valores calculados

###################Programa_principal#######################################################

Odometry = Odometry()

x = 0
Motores = [	'Motor_Read_7',  #0
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

IMU = [	'IMU_EULER_Z']

while(1):
	I = Odometry.bkb.read_int(Odometry.mem, 'WALK_PHASE')	#Lê valor da flag Phase da blackboard.

	if I == 1:			#Indica que a flag "phase" foi acionada, assim, teoricamente o robô completou seu ciclo de passo

		if x == 0:		#X: Variável de controle, para que o programa execute a cinemática apenas 1 vez a cada passo
			Odometry.Get_Bkb_Values(Motores, IMU)	#Lê valores dos motores e imu da blackboard
			Odometry.Kinematics_Calc()				#Realiza o calculo de cinemática direita
			Odometry.Position_Calc()				#Calcula a posição do robô a pela variação da cinemática
			Odometry.Show_Position()
			x = 1									#Permite que o cálculo seja realizado apenas uma vez

	if I == 0:
		x = 0
