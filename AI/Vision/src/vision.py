# -*- coding: UTF8 -*-

import sys
sys.path.append("./src")
import numpy as np
#import os
import cv2
import ctypes
import argparse
import time
from math import log,exp,tan,radians
import thread
import imutils

#from BallVision import *
from DNN import *

import sys

""" Initiate the path to blackboard (Shared Memory)"""
sys.path.append('../../Blackboard/src/')
"""Import the library Shared memory """
from SharedMemory import SharedMemory 
""" Treatment exception: Try to import configparser from python. Write and Read from config.ini file"""
try:
    """There are differences in versions of the config parser
    For versions > 3.0 """
    from ConfigParser import ConfigParser
except ImportError:
    """For versions < 3.0 """
    from ConfigParser import ConfigParser 

""" Instantiate bkb as a shared memory """
bkb = SharedMemory()
""" Config is a new configparser """
config1 = ConfigParser()
""" Path for the file config.ini:"""
config1.read('../../Control/Data/config.ini')
""" Mem_key is for all processes to know where the blackboard is. It is robot number times 100"""
mem_key = int(config1.get('Communication', 'no_player_robofei'))*100 
"""Memory constructor in mem_key"""
Mem = bkb.shd_constructor(mem_key)


parser = argparse.ArgumentParser(description='Robot Vision', epilog= 'Responsavel pela deteccao dos objetos em campo / Responsible for detection of Field objects')
parser.add_argument('--visionball', '--vb', action="store_true", help = 'Calibra valor para a visao da bola')
parser.add_argument('--visionMask', '--vm', action="store_true", help = 'Calibra valor para a visao da bola')
parser.add_argument('--visionMorph1', '--vm1', action="store_true", help = 'Mostra a imagem da morfologia perto')
parser.add_argument('--visionMorph2', '--vm2', action="store_true", help = 'Mostra a imagem da morfologia medio')
parser.add_argument('--visionMorph3', '--vm3', action="store_true", help = 'Mostra a imagem da morfologia longe') 
parser.add_argument('--visionMorph4', '--vm4', action="store_true", help = 'Mostra a imagem da morfologia muito longe') 
parser.add_argument('--withoutservo', '--ws', action="store_true", help = 'Servos desligado')
parser.add_argument('--head', '--he', action="store_true", help = 'Configurando parametros do controle da cabeca')


#----------------------------------------------------------------------------------------------------------------------------------


class classConfig():

	def __init__(self):
		# Read config.ini
		self.Config = ConfigParser()
		x = 0
		y = 0
		raio = 0

		self.SERVO_PAN = None
		self.SERVO_TILT  = None

		self.SERVO_PAN_LEFT = None
		self.SERVO_PAN_RIGHT  = None

		self.SERVO_TILT_VALUE = None
		self.SERVO_PAN_VALUE = None

		self.kernel_perto = None
		self.kernel_perto2 = None
	
		self.kernel_medio = None
		self.kernel_medio2 = None

		self.kernel_longe = None
		self.kernel_longe2 = None

		self.kernel_muito_longe = None
		self.kernel_muito_longe2 = None

		self.x_left = None
		self.x_center_left = None
		self.x_center = None
		self.x_center_right = None
		self.x_right = None

		self.y_chute = None
		self.y_longe = None
		self.CheckConfig()



	def CheckConfig(self):
		# Read file config.ini
		while True:
			if self.Config.read('../Data/config.ini') != []:
				print 'Leitura do config.ini'
				self.CENTER_SERVO_PAN = 	self.Config.getint('Basic Settings', 'center_servo_pan')
				self.POSITION_SERVO_TILT  = 	self.Config.getint('Basic Settings', 'position_servo_tilt')

				self.SERVO_PAN_LEFT = 		self.Config.getint('Basic Settings', 'servo_pan_left')
				self.SERVO_PAN_RIGHT  = 	self.Config.getint('Basic Settings', 'servo_pan_right')

				self.SERVO_PAN_ID    = 		self.Config.getint('Basic Settings', 'PAN_ID')
				self.SERVO_TILT_ID   = 		self.Config.getint('Basic Settings', 'TILT_ID')

				self.DNN_type = 		self.Config.get('Basic Settings', 'dnn_type')

				self.white_threshould = 	self.Config.getint('Basic Settings', 'white_threshould')

				self.max_count_lost_frame =   self.Config.getint('Basic Settings', 'max_count_lost_frame') 

				self.kernel_perto =		self.Config.getint('Kernel Selection', 'kernel_perto')
				self.kernel_perto2 = 		self.Config.getint('Kernel Selection', 'kernel_perto2')
			
				self.kernel_medio = 		self.Config.getint('Kernel Selection','kernel_medio')
				self.kernel_medio2 = 		self.Config.getint('Kernel Selection','kernel_medio2')

				self.kernel_longe = 		self.Config.getint('Kernel Selection', 'kernel_longe')
				self.kernel_longe2 = 		self.Config.getint('Kernel Selection', 'kernel_longe2')

				self.kernel_muito_longe = 	self.Config.getint('Kernel Selection', 'kernel_muito_longe')
				self.kernel_muito_longe2 = 	self.Config.getint('Kernel Selection', 'kernel_muito_longe2')

				self.x_left = 			self.Config.getint('Distance Limits (Pixels)', 'Left_Region_Division')
				self.x_center = 		self.Config.getint('Distance Limits (Pixels)', 'Center_Region_Division')
				self.x_right = 			self.Config.getint('Distance Limits (Pixels)', 'Right_Region_Division')
				self.y_chute = 			self.Config.getint('Distance Limits (Pixels)', 'Down_Region_Division')
				self.y_longe = 			self.Config.getint('Distance Limits (Pixels)', 'Up_Region_Division')
				break

			else:
				print 'Falha na leitura do config.ini, criando arquivo\nVision Ball inexistente, criando valores padrao'
				self.Config = ConfigParser()
				self.Config.write('../Data/config.ini')

				self.Config.add_section('Basic Settings')
				self.Config.set('Basic Settings', 'center_servo_pan'       , str(512)+'\t\t\t;Center Servo PAN Position')
				self.Config.set('Basic Settings', 'position_servo_tilt'      , str(705)+'\t;Center Servo TILT Position')

				self.Config.set('Basic Settings', 'servo_pan_left'   , str(162)+'\t\t\t;Center Servo PAN Position')
				self.Config.set('Basic Settings', 'servo_pan_right'  , str(862)+'\t;Center Servo TILT Position')

				self.Config.set('Basic Settings', 'PAN_ID'                 , str(19)+'\t\t\t;Servo Identification number for PAN')
				self.Config.set('Basic Settings', 'TILT_ID'                , str(20)+'\t;Servo Identification number for TILT')

				self.Config.set('Basic Settings', 'dnn_type'                , "r_80_cv4_32_256.tar.gz"+'\t;Dnn type')
				self.Config.set('Basic Settings', 'white_threshould'        , str(200)+'\t;Threshould')

				self.Config.set('Basic Settings', 'max_count_lost_frame'        , str(10)+'\t;Threshould') 

				self.Config.add_section('Kernel Selection')
				self.Config.set('Kernel Selection', 'kernel_perto'    , str(39)+'\t\t\t;Kernel Erosion ball is closest the robot')
				self.Config.set('Kernel Selection', 'kernel_perto2'   , str(100)+'\t;Kernel Dilation ball is closest the robot')
				self.Config.set('Kernel Selection', 'kernel_medio' , str(22)+'\t\t\t;Kernel Erosion ball is very close to the robot')
				self.Config.set('Kernel Selection', 'kernel_medio2', str(80)+'\t;Kernel Dilation ball is very close to the robot')
				self.Config.set('Kernel Selection', 'kernel_longe'      , str(12)+'\t\t\t;Kernel Erosion ball is close to the robot')
				self.Config.set('Kernel Selection', 'kernel_longe2'     , str(40)+'\t;Kernel Dilation ball is close to the robot')
				self.Config.set('Kernel Selection', 'kernel_muito_longe'        , str(7)+'\t\t\t;Kernel Erosion ball is far from the robot')
				self.Config.set('Kernel Selection', 'kernel_muito_longe2'       , str(30)+'\t;Kernel Dilation ball is far from the robot')

				self.Config.add_section('Distance Limits (Pixels)')
				self.Config.set('Distance Limits (Pixels)', 'Left_Region_Division'         , str(280)+'\t\t\t;X Screen Left division')
				self.Config.set('Distance Limits (Pixels)', 'Center_Region_Division'       , str(465)+'\t\t\t;X Screen Center division')
				self.Config.set('Distance Limits (Pixels)', 'Right_Region_Division'        , str(703)+'\t\t\t;X Screen Right division')
				self.Config.set('Distance Limits (Pixels)', 'Down_Region_Division'         , str(549)+'\t\t\t;Y Screen Down division')
				self.Config.set('Distance Limits (Pixels)', 'Up_Region_Division'           , str(220)+'\t\t\t;Y Screen Up division')

				with open('../Data/config.ini', 'wb') as configfile:
					self.Config.write(configfile)


class ballStatus():

	def __init__(self, config):
		self.config = config

	def BallStatus(self, x,y,status):

		if status  == 1:
			#Bola a esquerda
			if (x <= self.config.x_left):
				bkb.write_float(Mem,'VISION_PAN_DEG', 60) # Posição da bola
				print ("Bola a Esquerda")

			#Bola ao centro esquerda
			if (x > self.config.x_left and x < self.config.x_center):
				bkb.write_float(Mem,'VISION_PAN_DEG', 30) # Variavel da telemetria
				print ("Bola ao Centro Esquerda")

			#Bola centro direita
			if (x < self.config.x_right and x > self.config.x_center):
				bkb.write_float(Mem,'VISION_PAN_DEG', -30) # Variavel da telemetria
				print ("Bola ao Centro Direita")

			#Bola a direita
			if (x >= self.config.x_right):
				bkb.write_float(Mem,'VISION_PAN_DEG', -60) # Variavel da telemetria
				print ("Bola a Direita")

		else: 
			if (status ==2):
				bkb.write_float(Mem,'VISION_PAN_DEG', 60) # Posição da bola
				print ("Bola a Esquerda")
			else:
				bkb.write_float(Mem,'VISION_PAN_DEG', -60) # Variavel da telemetria
				print ("Bola a Direita")


	#	#CUIDADO AO ALTERAR OS VALORES ABAIXO!! O código abaixo possui inversão de eixos!
	#	# O eixo em pixels é de cima para baixo ja as distancias são ao contrario.
	#	# Quanto mais alto a bola na tela menor o valor em pixels 
	#	# e mais longe estará a bola do robô
		#Bola abaixo
		if (y < self.config.y_longe):
			bkb.write_float(Mem,'VISION_TILT_DEG', 70) # Variavel da telemetria
			print ("Bola acima")
		#Bola ao centro
		if (y < self.config.y_chute and y > self.config.y_longe):
			bkb.write_float(Mem,'VISION_TILT_DEG', 45) # Variavel da telemetria
			print ("Bola Centralizada")
		#Bola acima
		if (y >= self.config.y_chute):
			bkb.write_float(Mem,'VISION_TILT_DEG', 0) # Variavel da telemetria
			print ("Bola abaixo")


def thread_DNN():
	time.sleep(1)

	while True:
#		script_start_time = time.time()

#		print "FRAME = ", time.time() - script_start_time
		start1 = time.time()

#===============================================================================
		ball = False
		frame_b, x, y, raio, ball, status= detectBall.searchball(frame, args2.visionMask, args2.visionMorph1, args2.visionMorph2, args2.visionMorph3, args2.visionMorph4)
		print "tempo de varredura = ", time.time() - start1
		if ball ==False:
			bkb.write_int(Mem,'VISION_LOST', 1)
		else:
			bkb.write_int(Mem,'VISION_LOST', 0)
			ballS.BallStatus(x,y,status)
		if args2.visionball:
			cv2.circle(frame_b, (x, y), raio, (0, 255, 0), 4)
			cv2.imshow('frame',frame_b)
#===============================================================================
#		print "tempo de varredura = ", time.time() - start
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	cap.release()
	cv2.destroyAllWindows()


#----------------------------------------------------------------------------------------------------------------------------------
#Inicio programa

if __name__ == '__main__':


#	args = vars(parser.parse_args())
	args2 = parser.parse_args()

	config = classConfig()

	tmpdir = unzip_archive("./nets/"+config.DNN_type)
	caffemodel = None
	deploy_file = None
	mean_file = None
	labels_file = None
	for filename in os.listdir(tmpdir):
		full_path = os.path.join(tmpdir, filename)
		if filename.endswith('.caffemodel'):
			caffemodel = full_path
		elif filename == 'deploy.prototxt':
			deploy_file = full_path
		elif filename.endswith('.binaryproto'):
			mean_file = full_path
		elif filename == 'labels.txt':
			labels_file = full_path
		else:
			print 'Unknown file:', filename

	assert caffemodel is not None, 'Caffe model file not found'
	assert deploy_file is not None, 'Deploy file not found'

###    # Load the model and images
	net = get_net(caffemodel, deploy_file, use_gpu=False)
	transformer = get_transformer(deploy_file, mean_file)
	_, channels, height, width = transformer.inputs['data']
	labels = read_labels(labels_file)

###    #create index from label to use in decicion action
	number_label =  dict(zip(labels, range(len(labels))))
	print number_label
###    #

	ballS = ballStatus(config)
	detectBall = objectDetect(net, transformer, mean_file, labels, args2.withoutservo, config, bkb, Mem)
#	detectBall.servo.writeWord(config.SERVO_TILT_ID,34, 70)#olha para o centro

	cap = cv2.VideoCapture(0) #Abrindo camera
        cap.set(3,1280) #720 1280 1920
        cap.set(4,720) #480 720 1080
	os.system("v4l2-ctl -d /dev/video0 -c focus_auto=0 && v4l2-ctl -d /dev/video0 -c focus_absolute=0")
	os.system("v4l2-ctl -d /dev/video0 -c saturation=200")

	try:
            thread.start_new_thread(thread_DNN, ())
	except:
            print "Error Thread"

	while True:

#		if bkb.read_int(Mem,'IMU_STATE')==1:
#			detectBall.servo.writeWord(config.SERVO_TILT_ID,34, 512)#olha para o centro
#			detectBall.servo.writeWord(config.SERVO_TILT_ID,32, 1023)#velocidade
#			detectBall.servo.writeWord(config.SERVO_PAN_ID,32, 1023)#velocidade
#			detectBall.servo.writeWord(config.SERVO_TILT_ID,30, config.POSITION_SERVO_TILT+350)#olha para o centro
#			time.sleep(0.5)
#			detectBall.servo.writeWord(config.SERVO_TILT_ID,34, 100)#olha para o centro
#			detectBall.servo.writeWord(config.SERVO_PAN_ID,30, config.CENTER_SERVO_PAN)#olha para o centro
#		else:
#			detectBall.servo.writeWord(config.SERVO_TILT_ID,30, config.POSITION_SERVO_TILT)#olha para o centro

		bkb.write_int(Mem,'VISION_WORKING', 1) # Variavel da telemetria

		ret, frame = cap.read()
		frame = frame[:,200:1100]


		time.sleep(0.01)

#===============================================================================
#===============================================================================
#===============================================================================
#===============================================================================
#===============================================================================
#===============================================================================
#===============================================================================
#===============================================================================
