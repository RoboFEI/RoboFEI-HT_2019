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
		self.config = ConfigParser()								#Instanciando um objeto a classe para ler arquivos

		# looking for the file config.ini:
		self.config.read('../../Control/Data/config.ini')

		self.mem_key = int(self.config.get('Communication', 'no_player_robofei'))*100	#Lendo o número do robô
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
		self.ti = 0
		self.tf = 0
		self.L4 = 9.30	#[cm]
		self.L5 = 9.30
		self.Lf = 3.35
		self.Ltx = 0.50
		self.Lty = 12.22
		self.Ltz = 3.70
		self.Mot = []	#Cria vetor que vai acessar e ler os valores dos motores da blackboard
		self.IMU = []	#Cria vetor que vai acessar e ler os valores da IMU da blackboard
		self.Kinematic_rx = []
		self.Kinematic_ry = []
		self.Kinematic_lx = []
		self.Kinematic_ly = []
		self.Prx = 0
		self.Pry = 0
		self.Plx = 0
		self.Ply = 0


##################Leitura dos valores da IMU###############################################

	def Kinematics_Calc(self, Item1, Item2):
		while(self.bkb.read_int(self.mem, 'WALK_PHASE') != self.I+2 or self.bkb.read_int(self.mem, 'WALK_PHASE') != self.I-2):
			for i in Item1:		#Lê os valores dos motores, convertendo para graus e adiciona no vetor MOT
				self.Mot.append((self.bkb.read_int(self.mem, i))*0.005113269 + 0.52359877559)
			for k in Item2:                  #Aquisiçao da orientaçao do corpo da IMU
		  		self.IMU.append(self.bkb.read_float(self.mem, k))

##################Calculo cinemática########################################################
	
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
			r21 = -(-s11*s15+c11*c15*cabc)
			r31 = (s7*sabc-c7*s11*cabc)*c15-(c7*c11*s15)
			Pr_x = ((self.L4*s9+self.L5*sab)*s7-(self.L4*c9+self.L5*cab)*c7*s11)
			Pr_y = (-(self.L4*s9+self.L5*sab)*c7-(self.L4*c9+self.L5*cab)*s7*s11)
			Pr_z = ((self.L4*c9+self.L5*cab)*c11)
	
			self.Prx = self.Lf*r11 - self.Ltx - Pr_y
			self.Pry = self.Lf*r21 - self.Lty - Pr_z

########Cinemática_Perna_Esquerda#######
			l11 = -((-c8*sabc-s8*s12*cabc)*c16-s8*c12*s16)
			l21 = -(-s12*s16+c12*c16*cabc)
			Pl_x = ((self.L4*s10+self.L5*sab)*s8-(self.L4*c10+self.L5*cab)*c8*s12)
			Pl_y = (-(self.L4*s10+self.L5*sab)*c8-(self.L4*c10+self.L5*cab)*s8*s12)
			Pl_z = ((self.L4*c10+self.L5*cab)*c12)
	
			self.Plx = self.Lf*l11 - self.Ltx - Pl_y
			self.Ply = self.Lf*l21 - self.Lty - Pl_z
		
			self.Kinematic_rx.append(self.Prx)	#adiciona todos os valores no vetor
			self.Kinematic_ry.append(self.Pry)
			
			self.Kinematic_lx.append(self.Plx)
			self.Kinematic_ly.append(self.Ply)


##################Calculo_de_Posição########################################################

	def Position_Calc(self):
		if self.IMU[0]>=self.self.IMU[1]: 			#Corpo movendo para frente
			Max_rx = sy.Max(sy.Abs(self.Kinematic_rx))	#O maior dos valores abs
			pos = self.Kinematic_rx.index(Max_rx)		#Posicao desse maior valor
			
			Max_lx = sy.Max(sy.Abs(self.Kinematic_lx))	
			pos1 = self.Kinematic_lx.index(Max_lx)
		else:
			Max_ry = sy.Max(sy.Abs(self.Kinematic_ry))
			pos = self.Kinematic_ry.index(Max_ry)
			
			Max_ly = sy.Max(sy.Abs(self.Kinematic_ly))
			pos1 = self.Kinematic_ly.index(Max_ly)
			
		Max_Dist_rx = self.Kinematic_rx[pos]
		Max_Dist_ry = self.Kinematic_ry[pos]
		Max_Dist_lx = self.Kinematic_ly[pos1]
		Max_Dist_ly = self.Kinematic_ly[pos1]
		
		if self.j%2: 	#Calculo de posição a partir do movimento da perna direita
			Var_Posx_L = Max_Dist_lx - self.Posx_i_L 
			Var_Posy_L = Max_Dist_ly - self.Posy_i_L
			self.posx = self.posx + Var_Posx_L
			self.posy = self.posy + Var_Posy_L
			self.Posx_i_R = self.Prx
			self.Posy_i_R = self.Pry
			print("I = 0")
			
		else: 			#Calculo de posição a partir do movimento da perna esquerda
			Var_Posx_R = Max_Dist_rx - self.Posx_i_R	#Se não houver o calculo de variação e ela ocorrer no semiplano negativo, ao invés de somar a posição, irá decrementá-la, gerando um erro de cálculo
			Var_Posy_R = Max_Dist_ry - self.Posy_i_R
			self.posx = self.posx + Var_Posx_R
			self.posy = self.posy + Var_Posy_R
			self.Posx_i_L = self.Plx
			self.Posy_i_L = self.Ply
			print("I = 2")

##################Print_dos_valores########################################################

	def Show_Position(self):
		print ("%f, %f"% (self.Prx, self.Pry))
		print ("%f, %f"% (self.Plx, self.Ply))
		print("posx = %f \t posy = %f" % (self.posx, self.posy))	#Apresenta os valores valores calculados

###################Programa_principal#######################################################

Odometry = Odometry()

x = 0
k = 0
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

IMU = [ 'IMU_ACCEL_X',
        'IMU_ACCEL_Y',]

while(1):
	P = Odometry.bkb.read_int(Odometry.mem, 'WALK_PHASE')	
	if P != 0:
		while(1):
			RC = Odometry.bkb.read_int(Odometry.mem, 'IMU_STATE') #0: Robo em pe, 1: Robo caido
			Odometry.I = Odometry.bkb.read_int(Odometry.mem, 'WALK_PHASE')	
			if (Odometry.I, k ) == (2, 0):	#Pe esquerdo em contato com o chao
				Odometry.j = 0
				k = 1
				x = 1		#So executara o
			if (Odometry.I, k ) == (0, 1):	#Pe direito em contato com o chao 
				Odometry.j = 1
				k = 0
				x = 1
			if (x, RC) == (1, 0):	#Execuao 1 vez por passo se o robo estiver em pe
				Odometry.Kinematics_Calc(Motores, IMU)	#Lê valores dos motores e imu da blackboard
				Odometry.Position_Calc()  #Calcula a posição do robô a pela variação da cinemática
				Odometry.Show_Position()
				self.Kinematic_rx = []
				self.Kinematic_ry = []
				self.Kinematic_ly = []
				self.Kinematic_ly = []
 
 
