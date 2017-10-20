#coding: utf-8

import sys
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

##################Leitura dos valores da IMU###############################################

	def Get_Bkb_Values(self, Item, Type):

		Var={'int': self.bkb.read_int,  'float':self.bkb.read_float}	#Verifica pelo argumento Type se o tipo a ser lido é int ou float
		self.Valbkb = []	#Cria vetor que vai acessar e ler os valores da BlackBoard

		for i in Item:
			self.Valbkb.append(Var[Type](self.mem, i))		#Substitui a frase para informar o tipo da leitura e guarda em Valbkb


##################Printe dos valores########################################################

	def Print(self):
		print(self.Valbkb)

###################Programa principal#######################################################
ValMot = Odometry()
ValIMU = Odometry()

Motores = [	'Motor_Read_7', 						
		'Motor_Read_8', 
		'Motor_Read_9', 
		'Motor_Read_10', 
		'Motor_Read_11',
		'Motor_Read_12', 
		'Motor_Read_13', 
		'Motor_Read_14',
		'Motor_Read_15',
		'Motor_Read_16',
		'Motor_Read_17',
		'Motor_Read_18']
IMU = [
		'IMU_EULER_X',
		'IMU_EULER_Y',
		'IMU_EULER_Z']

ValMot.Get_Bkb_Values(Motores, 'int')
ValIMU.Get_Bkb_Values(IMU, 'float')

ValMot.Print()
ValIMU.Print()








