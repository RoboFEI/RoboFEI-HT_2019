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

		for i in Item1:
			self.Mot.append((self.bkb.read_int(self.mem, i))*0.005113269 + 0.52359877559)#Substitui a frase para informar o tipo da leitura e guarda em Valbkb e transforma a leitura em graus.
			
#		for i in Item1:             #For para aquisitar apenas os valores da imu sem tratamento
#			self.Mot.append(self.bkb.read_int(self.mem, i))	
		for j in Item2:
			self.IMU.append(self.bkb.read_float(self.mem, j))

##################Calculo cinemática########################################################

	def Kinematics_Right_Left_Leg(self):

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

		r11 = (s7*sabc-c7*s11*cabc)*c15-c7*c11*s15
		r21 = (-c7*sabc-s7*s11*cabc)*c15-s7*c11*s15
		r31 = -s11*s15+c11*c15*cabc

		r12 = -(s7*sabc-c7*s11*cabc)*s15-c7*c11*s15
		r22 = -(-c7*sabc-s7*s11*cabc)*s15-s7*c11*s15
		r32 = -s11*s15-c11*s15*cabc

		r13 = s7*cabc+c7*s11*sabc
		r23 = c7*cabc+s7*s11*sabc
		r33 = c11*sabc

		self.Prx = (L4*s9+L5*sab)*s7-(L4*c9+L5*cab)*c7*s11 + Lf*r11	#Position Right leg x
		self.Pry = (L4*s9+L5*sab)*s7-(L4*c9+L5*cab)*c7*s11 + Lf*r21	#Position Right leg y
		#Prz = (L4*s9+L5*cab)*c11 + Lf*r31			#Position Right leg z

########Cinemática_Perna_Esquerda#######

		l11 = (s8*slabc-c8*s12*clabc)*c16-c8*c12*s16
		l21 = (-c8*slabc-s8*s12*clabc)*c16-s8*c12*s16
		l31 = -s12*s16+c12*c16*clabc

		l12 = -(s8*slabc-c8*s12*clabc)*s16-c8*c12*s16
		l22 = -(-c8*slabc-s8*s12*clabc)*s16-s8*c12*s16
		l32 = -s12*s16-c12*s16*clabc

		l13 = s8*clabc+c8*s18*slabc
		l23 = c8*clabc+s8*s12*slabc
		l33 = c12*slabc

		self.Plx = (L4*s10+L5*slab)*s8-(L4*c10+L5*clab)*c8*s12 + Lf*l11	#Position Right leg x
		self.Ply = (L4*s10+L5*slab)*s8-(L4*c10+L5*clab)*c8*s12 + Lf*l21	#Position Right leg y
		#Plz = (L4*s10+L5*clab)*c12 + Lf*l31				#Position Right leg z

##################Calculo da Posição########################################################

	def Position_Calc(self):
		if self.j%2: 
			Var_Posx_L = self.Plx - self.Posx_i_L #Se não houver o calculo de variação e ela ocorrer no semiplano negativo, ao invés de somar a posição, irá decrementá-la, gerando um erro de cálculo
			Var_Posy_L = self.Ply - self.Posy_i_L 
			self.posx = self.posx + Var_Posx_L
			self.posy = self.posy + Var_Posy_L
			self.Posx_i_R = self.Prx
			self.Posy_i_R = self.Pry
			self.j-=1
		else:
			Var_Posx_R = self.Prx - self.Posx_i_R
			Var_Posy_R = self.Pry - self.Posy_i_R
			self.posx = self.posx + Var_Posx_R 
			self.posy = self.posy + Var_Posy_R
			self.Posx_i_L = self.Plx
			self.Posy_i_L= self.Ply
			self.j+=1

##################Printe dos valores########################################################

	def Show_Position(self):
	
	    	print("\nposx = %f \t posy = %f" % (self.posx, self.posy))

#    	    print("\nPlx = %f \t Ply = %f" % (self.Plx, self.Ply))
#           print("\nPrx = %f \t Pry = %f" % (self.Prx, self.Pry))
        
###################Programa principal#######################################################

Odometry = Odometry()

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
	Odometry.Get_Bkb_Values(Motores, IMU)
	time.sleep(0.08)
	Odometry.Kinematics_Right_Left_Leg()
	Odometry.Position_Calc()
	Odometry.Show_Position()




