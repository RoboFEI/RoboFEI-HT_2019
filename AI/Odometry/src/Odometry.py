#coding: utf-8

import os
import sys
import numpy as np
import sympy as sy
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
		self.Euler_i = 0
		self.th =  sy.Symbol('self.th')	# simbolico para o angulo em torno do eixo Z
		self.Posxy_fix = sy.zeros((3, 1))	#Pos. refer. fixo (abs)
		
		self.MT_xy = sy.Matrix([[ sy.cos(self.th), sy.sin(self.th), 0],#Matriz rotacao ao redor de Z
					   	    [-sy.sin(self.th), sy.cos(self.th), 0],#Transf. de ref. movel para ref.fixo
					   	    [  0             ,       0        , 1]])
		 


##################Leitura dos valores da IMU###############################################

	def Get_Bkb_Values(self, Item1, Item2):

		self.Mot = []	#Cria vetor que vai acessar e ler os valores dos motores da blackboard
		self.IMU = []	#Cria vetor que vai acessar e ler os valores da IMU da blackboard
		k = 0

		for i in Item1:		#Lê os valores dos motores, convertendo para graus e adiciona no vetor MOT
			self.Mot.append((self.bkb.read_int(self.mem, i) - self.Mot_Ini[k])*0.0051232757)
			k += 1

		for j in Item2:		#Lê valores da IMU e adiciona no vetor IMU
			self.IMU.append(self.bkb.read_float(self.mem, j))

##################Calculo cinemática########################################################

	def Kinematics_Calc(self):

		L4 = 9.30	#[cm]
		L5 = 9.30
		Lf = 5.30
		Ltx = 0.50
		Lty = 10.50
		Ltz = 3.30
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
		slabc = np.sin(self.Mot[3]-self.Mot[7]+self.Mot[11])
		clabc = np.cos(self.Mot[3]-self.Mot[7]+self.Mot[11])
		clab = np.cos(self.Mot[3]-self.Mot[7])
		slab = np.sin(self.Mot[3]-self.Mot[7])
		cl14 = np.cos(-self.Mot[7])
		cl16 = np.cos(-self.Mot[9])
		cl12 = np.cos(-self.Mot[5])
		sl14 = np.sin(-self.Mot[7])
		sl16 = np.sin(-self.Mot[9])
		sl12 = np.sin(-self.Mot[5])

########Cinemática_Perna_Direita#######
	
		Pr_x = ((L4*s9+L5*sab)*s7-(L4*c9+L5*cab)*c7*s11) 
		Pr_y = (-(L4*s9+L5*sab)*c7-(L4*c9+L5*cab)*s7*s11) 
		Pr_z = ((L4*c9+L5*cab)*c11) 

		self.Pry = Lf*(c11*s15*s7 - c15*(-c7*sabc - cabc*s11*s7)) - Pr_y
		self.Prz = Lf*(-c11*c15*cabc + s11*s15) - Pr_z
		self.Prx = Lf*(-c11*c7*s15 + c15*(-c7*cabc*s11 + s7*sabc)) + Pr_x

########Cinemática_Perna_Esquerda#######
		
		Pl_x = ((L4*s10+L5*slab)*s8-(L4*c10+L5*clab)*c8*sl12) 
		Pl_y = (-(L4*s10+L5*slab)*c8-(L4*c10+L5*clab)*s8*sl12) 
		Pl_z = ((L4*c10+L5*clab)*cl12) 

		self.Ply = Lf*(cl12*sl16*s8 - cl16*(-c8*slabc - clabc*sl12*s8)) - Pl_y
		self.Plz = Lf*(-cl12*cl16*clabc + sl12*sl16) - Pl_z
		self.Plx = Lf*(-cl12*c8*sl16 + cl16*(-c8*clabc*sl12 + s8*slabc)) + Pl_x

##################Calculo_de_Posição########################################################

	def Position_Calc(self):
		if self.j%2: 	#Calculo de posição a partir do movimento da perna direita
			print ("I = 2")
			self.posx = self.posx + (self.Prx - self.Posx_i_R)	#I = 2
			self.posy = self.posy + (self.Pry - self.Posy_i_R)
			self.Posx_i_L = self.Plx
			self.Posy_i_L = self.Ply
			
		else: 	#Calculo de posição a partir do movimento da perna esquerda
			print ("I = 0")
			self.posx = self.posx + (self.Plx - self.Posx_i_L) 	#I = 0
			self.posy = self.posy + (self.Ply - self.Posy_i_L)
			self.Posx_i_R = self.Prx
			self.Posy_i_R = self.Pry
			
		if(self.IMU[0] > np.pi/2):
			Euler_imu_z = np.pi - self.IMU[0] 
		elif(self.IMU[0] < -np.pi/2):
			Euler_imu_z = -np.pi - self.IMU[0] 
		else:
			Euler_imu_z = self.IMU[0]
			
		Vec = np.sqrt(self.posx**2+self.posy**2)	#Vetor posicao ref. movel
		px = Vec*np.sin(Euler_imu_z)	#Desmembra o vetor em x
		py = Vec*np.cos(Euler_imu_z)	#Desmembra o vetor em y
		
		self.Posxy_fix[0, 0] += px
		self.Posxy_fix[1, 0] += py
						
		#self.MT_xy = sy.transpose(self.MT_xy.subs(self.th , self.IMU[0]))#Subs. val. Matriz transf. para ref. fixo	
		#Posxy_r = sy.Matrix([[self.posx], [self.posy], [0]])#Matriz pos. ref. movel
		#self.Posxy_abs = self.Posxy_abs+self.MT_xy*Posxy_r		#Transformando para pos. ref. fixo (pto 												inicial)

			
#Se não houver o calculo de variação e ela ocorrer no semiplano negativo, ao invés de somar a posição, irá decrementá-la, gerando um erro de cálculo

##################Print_dos_valores########################################################

	def Show_Position(self):
		print ("\n%f, %f, %f"% (self.Prx, self.Pry, self.Prz))
		print ("%f, %f, %f"% (self.Plx, self.Ply, self.Plz))
		#print("posx = %f \t posy = %f" % (self.Posxy_abs[0, 0], self.Posxy_abs[1, 0]))	#Apresenta os valores valores calculados
		print("posx = %f \t posy = %f" % (self.posx, self.posy))
		#print(self.IMU[0])

###################Programa_principal#######################################################

Odometry = Odometry()

x = 0
k = 1
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

IMU = [	'IMU_EULER_Z']

#######verificacao de erro inicial da posicao dos motores###
Odometry.Mot_Ini = []	
for i in Motores:
	Odometry.Mot_Ini.append(Odometry.bkb.read_int(Odometry.mem, i))
	#Odometry.Mot_Ini.append(512)
	
######Chamada dos calculos###########

while(1):
	RC = Odometry.bkb.read_int(Odometry.mem, 'IMU_STATE') #0: Robo em pe, 1: Robo caido
	I = Odometry.bkb.read_int(Odometry.mem, 'WALK_PHASE')	
	if (I, k ) == (2, 0):	#Pe esquerdo em contato com o chao
		Odometry.j = 0
		k = 1
		x = 1		#So executara o
	if (I, k ) == (0, 1):	#Pe direito em contato com o chao 
		Odometry.j = 1
		k = 0
		x = 1
	if (x, RC) == (1, 0):	#Execuao 1 vez por passo se o robo estiver em pe
		Odometry.Get_Bkb_Values(Motores, IMU)	#Lê valores dos motores e imu da blackboard
		Odometry.Kinematics_Calc()#Realiza o calculo de cinemática direita
		Odometry.Position_Calc()  #Calcula a posição do robô a pela variação da cinemática
		Odometry.Show_Position()
		x = 0
 
 
