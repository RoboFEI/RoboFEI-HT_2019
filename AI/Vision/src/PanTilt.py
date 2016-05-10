import cv2
import time

from servo import Servo
from PID import *
import matplotlib.pyplot as plt



import sys
sys.path.append('../../Blackboard/src/')
from SharedMemory import SharedMemory 
bkb = SharedMemory()
KEY = 0
Mem = bkb.shd_constructor(KEY)

class Pantilt (object):

	servo = None #Para controle dos servos

	cen_posTILT = None #Centro do Tilt
	cen_posPAN = None #Centro do Pan
	
	min_posTILT = None #Min do Tilt
	min_posPAN = None #Min do Pan
	
	max_posTILT = None #Max do Tilt
	max_posPAN = None #Max do Pan
	
	__Config = None #Leitura arquivo
	__args = None
	
	# Ganhos
	__p_pan = None
	__i_pan = None
	__d_pan = None
	
	__p_tilt = None
	__i_tilt = None
	__d_tilt = None
	
	__p_speed = None
	__min_speed = None
	
	# Find
	__list_find = None
	__old_list_find = None
	__pos_find = 0
	__lost = 1
	
	# Controlador
	__ControllerPan = None
	__ControllerTilt = None
	
	# DEFINES SERVOS
	__VAL_MIN = 6
	__VAL_MAX = 8
	__SERVO_PAN = 19
	__SERVO_TILT = 20
	__STATUS = 24
	__GOAL_POS = 30
	__SPEED = 32
	__PRESENT_POS = 36

#----------------------------------------------------------------------------------------------------------------------------------

	def __init__(self, args, Config):
		
		self.__Config = Config
		self.__readConfig()
		
		self.__args = args
		
		# Abrindo servos e configurando
		if args.withoutservo == False:
			self.servo = Servo(self.cen_posPAN, self.cen_posTILT)
			self.min_posPAN = self.servo.readWord(self.__SERVO_PAN, self.__VAL_MIN)
			self.max_posPAN = self.servo.readWord(self.__SERVO_PAN, self.__VAL_MAX)
			self.min_posTILT = self.servo.readWord(self.__SERVO_TILT, self.__VAL_MIN)
			self.max_posTILT = self.servo.readWord(self.__SERVO_TILT, self.__VAL_MAX)
		
		# Criando controlador
		self.__ControllerPan = PID(self.__p_pan, self.__i_pan, self.__d_pan)
		self.__ControllerPan.setPoint(0)
		
		self.__ControllerTilt = PID(self.__p_tilt, self.__i_tilt, self.__d_tilt)
		self.__ControllerTilt.setPoint(0)
		
		self.servo.writeWord(self.__SERVO_PAN, self.__SPEED, self.__min_speed)
		self.servo.writeWord(self.__SERVO_TILT, self.__SPEED, self.__min_speed)
		
		if args.head == True:
			self.__setVarredura()
			
			cv2.namedWindow('Video - Bola')
			cv2.createTrackbar('P Pan','Video - Bola',0,1000,self.__nothing)
			cv2.createTrackbar('I Pan','Video - Bola',0,1000,self.__nothing)
			cv2.createTrackbar('D Pan','Video - Bola',0,100,self.__nothing)
			
			cv2.createTrackbar('P Tilt','Video - Bola',0,1000,self.__nothing)
			cv2.createTrackbar('I Tilt','Video - Bola',0,1000,self.__nothing)
			cv2.createTrackbar('D Tilt','Video - Bola',0,100,self.__nothing)
		
			cv2.createTrackbar('Min vel','Video - Bola',0,1023,self.__nothing)
			
			cv2.createTrackbar('Mod','Video - Bola',0,3,self.__nothing)
		
			#Setando valoeres iniciais
			cv2.setTrackbarPos('P Pan','Video - Bola', int(self.__p_pan*100))
			cv2.setTrackbarPos('I Pan','Video - Bola', int(self.__i_pan*100))
			cv2.setTrackbarPos('D Pan','Video - Bola', int(self.__d_pan*1000))
			
			cv2.setTrackbarPos('P Tilt','Video - Bola', int(self.__p_tilt*100))
			cv2.setTrackbarPos('I Tilt','Video - Bola', int(self.__i_tilt*100))
			cv2.setTrackbarPos('D Tilt','Video - Bola', int(self.__d_tilt*1000))
			
			cv2.setTrackbarPos('Min vel','Video - Bola', self.__min_speed)
			
			cv2.setTrackbarPos('Mod','Video - Bola', 0)
			self.lastmod = -1

#----------------------------------------------------------------------------------------------------------------------------------

	def mov(self,status, posHead):
		if self.__args.head == True:
			self.__p_pan = cv2.getTrackbarPos('P Pan','Video - Bola')/100.0
			self.__i_pan = cv2.getTrackbarPos('I Pan','Video - Bola')/100.0
			self.__d_pan = cv2.getTrackbarPos('D Pan','Video - Bola')/1000.0
			
			self.__p_tilt = cv2.getTrackbarPos('P Tilt','Video - Bola')/100.0
			self.__i_tilt = cv2.getTrackbarPos('I Tilt','Video - Bola')/100.0
			self.__d_tilt = cv2.getTrackbarPos('D Tilt','Video - Bola')/1000.0
			
			self.__min_speed = cv2.getTrackbarPos('Min vel','Video - Bola')
			
			mod = cv2.getTrackbarPos('Mod','Video - Bola')
			
			if self.__min_speed == 0:
				self.__min_speed = 1
				cv2.setTrackbarPos('Min vel','Video - Bola', 1)
			
			self.__ControllerPan.setKp(self.__p_pan)
			self.__ControllerPan.setKi(self.__i_pan)
			self.__ControllerPan.setKd(self.__d_pan)
			
			self.__ControllerTilt.setKp(self.__p_tilt)
			self.__ControllerTilt.setKi(self.__i_tilt)
			self.__ControllerTilt.setKd(self.__d_tilt)
			
			if self.lastmod != mod:
				if mod == 0:
					self.servo.writeByte(self.__SERVO_PAN,self.__STATUS, 0)
					self.servo.writeByte(self.__SERVO_TILT,self.__STATUS, 0)
				elif mod == 2:
					self.servo.writeByte(self.__SERVO_PAN,self.__STATUS, 0)
					self.servo.writeByte(self.__SERVO_TILT,self.__STATUS, 1)
					self.servo.writeWord(self.__SERVO_TILT, self.__SPEED, self.__min_speed)
				elif mod == 1:
					self.servo.writeByte(self.__SERVO_PAN,self.__STATUS, 1)
					self.servo.writeByte(self.__SERVO_TILT,self.__STATUS, 0)
					self.servo.writeWord(self.__SERVO_PAN, self.__SPEED, self.__min_speed)
				elif mod == 3:
					self.servo.writeByte(self.__SERVO_PAN,self.__STATUS, 1)
					self.servo.writeByte(self.__SERVO_TILT,self.__STATUS, 1)
					self.servo.writeWord(self.__SERVO_PAN, self.__SPEED, self.__min_speed)
					self.servo.writeWord(self.__SERVO_TILT, self.__SPEED, self.__min_speed)
				self.__ControllerPan.setIntegrator(0)
				self.__ControllerPan.setDerivator(0)
				self.__ControllerTilt.setIntegrator(0)
				self.__ControllerTilt.setDerivator(0)
				self.lastmod = mod
		
		if status[0] == 2:
			if status[1] != 0 and status[2] != 0 and self.__lost == 0:
				posHead = self.__segue(status)
			else:
				if self.__args.head == False or self.servo.readByte(self.__SERVO_PAN,self.__STATUS) == 1:
					self.servo.writeWord(self.__SERVO_PAN,
															self.__GOAL_POS,
															posHead[0])
				if self.__args.head == False or self.servo.readByte(self.__SERVO_TILT,self.__STATUS) == 1:
					self.servo.writeWord(self.__SERVO_TILT,
															self.__GOAL_POS,
															posHead[1])
				self.__lost = 0
		else:
			self.__lost = 1
			self.__ControllerPan.setIntegrator(0)
			self.__ControllerPan.setDerivator(0)
			self.__ControllerTilt.setIntegrator(0)
			self.__ControllerTilt.setDerivator(0)
			posHead = self.__find(status)
	
		return posHead

#----------------------------------------------------------------------------------------------------------------------------------

	def __readConfig(self):
		while True:
			if 'Offset'not in self.__Config.sections():
				print "Offset inexistentes, crinado valores padrao"
				self.__Config.add_section('Offset')
				self.__Config.set('Offset', 'ID_19', str(430)+'\t;Offset Tilt')
				self.__Config.set('Offset', 'ID_20', str(540)+'\t;Offset Pan\n;Valores para o robo olhando para frente')
				
				with open('../Data/config.ini', 'wb') as configfile:
					self.__Config.write(configfile)
				
				self.__Config.read('../Data/config.ini')

			else:
				self.cen_posTILT = self.__Config.getint('Offset', 'ID_19')
				self.cen_posPAN = int(self.__Config.get('Offset', 'ID_20').rpartition(';')[0])
				break
			
		while True:
			if 'Head' not in self.__Config.sections():
				print "Head inexistente, crinado valores padrao"
				self.__Config.add_section('Head')
				self.__Config.set('Head', 'p_pan', str(0.0)+'\t;Ganho proporcinal para controle da posicao no pan')
				self.__Config.set('Head', 'i_pan', str(0.0)+'\t;Ganho integral para controle da posicao no pan')
				self.__Config.set('Head', 'd_pan', str(0.0)+'\t;Ganho derivativo para controle da posicao no pan\n')
				self.__Config.set('Head', 'p_tilt', str(0.0)+'\t;Ganho proporcinal para controle da posicao no tilt')
				self.__Config.set('Head', 'i_tilt', str(0.0)+'\t;Ganho integral para controle da posicao no tilt')
				self.__Config.set('Head', 'd_tilt', str(0.0)+'\t;Ganho derivativo para controle da posicao no tilt\n;Ganho PID para a posicao\n')
				
				self.__Config.set('Head', 'min_vel', str(1)+'\t;Velocidade minima\n;Ganho P para a velocidade e velocidade minima')
			
				with open('../Data/config.ini', 'wb') as configfile:
					self.__Config.write(configfile)
			
				self.__Config.read('../Data/config.ini')

			else:
				self.__p_pan = self.__Config.getfloat('Head', 'p_pan')
				self.__i_pan = self.__Config.getfloat('Head', 'i_pan')
				self.__d_pan = self.__Config.getfloat('Head', 'i_pan')
				self.__p_tilt = self.__Config.getfloat('Head', 'p_tilt')
				self.__i_tilt = self.__Config.getfloat('Head', 'i_tilt')
				self.__d_tilt = float(self.__Config.get('Head', 'd_tilt').rpartition(';')[0])
			
				self.__min_speed = int(self.__Config.get('Head', 'min_vel').rpartition(';')[0])
				break

#----------------------------------------------------------------------------------------------------------------------------------

	def __find(self,status):
		self.__jump_find = 75
		self.__list_find = [[self.min_posPAN, self.max_posTILT],
												[self.max_posPAN, self.max_posTILT]]
		
		# Indo para bola
		if abs(self.servo.readWord(self.__SERVO_PAN, self.__PRESENT_POS)-self.servo.readWord(self.__SERVO_PAN, self.__GOAL_POS)) < 10:
			# Procura qual e o maior valor da distancia
			dis_pan =  abs(self.servo.readWord(self.__SERVO_PAN,  self.__PRESENT_POS) - self.__list_find[self.__pos_find%2][0])*1.0
			dis_tilt = abs(self.servo.readWord(self.__SERVO_TILT, self.__PRESENT_POS) - self.__list_find[self.__pos_find%2][1] + self.__jump_find*(self.__pos_find/2))*1.0
			
			if dis_pan > dis_tilt:
				max_dis = dis_pan
			else:
				max_dis = dis_tilt
			
#			print("dis_pan: " + str(dis_pan))
#			print("dis_tilt: " + str(dis_tilt))
#			raw_input("max_dis: " + str(max_dis))
			
#			print(99*(dis_pan/max_dis))
#			raw_input(99*(dis_tilt/max_dis))
			
			if self.__args.head == False or self.servo.readByte(self.__SERVO_PAN,self.__STATUS) == 1:
				self.servo.writeWord(self.__SERVO_PAN, self.__SPEED,
													1+int(99*(dis_pan/max_dis)))
				self.servo.writeWord(self.__SERVO_PAN,
													self.__GOAL_POS,
													self.__list_find[self.__pos_find%2][0])
			if self.__args.head == False or self.servo.readByte(self.__SERVO_TILT,self.__STATUS) == 1:
				self.servo.writeWord(self.__SERVO_TILT, self.__SPEED,
														1+int(99*(dis_tilt/max_dis)))
				self.servo.writeWord(self.__SERVO_TILT,
														self.__GOAL_POS,
														self.__list_find[self.__pos_find%2][1]+(self.__jump_find*(self.__pos_find/2)))
			self.__pos_find += 1
			if self.__list_find[self.__pos_find%2][1]-(self.__jump_find*(self.__pos_find/2)) <= self.min_posTILT:
				self.__pos_find = 0
		
		return [self.servo.readWord(self.__SERVO_PAN, self.__PRESENT_POS), self.servo.readWord(self.__SERVO_TILT, self.__PRESENT_POS)]


#----------------------------------------------------------------------------------------------------------------------------------

	def __segue(self,status):
		# Pan
#		# Posicao
		self.__pos_find = 0
		if self.__args.head == False or self.servo.readByte(self.__SERVO_PAN,self.__STATUS) == 1:
			self.servo.writeWord(self.__SERVO_PAN, self.__SPEED, self.__min_speed)
			self.servo.writeWord(self.__SERVO_PAN,
								self.__GOAL_POS,
								int(self.servo.readWord(self.__SERVO_PAN,self.__PRESENT_POS) + self.__ControllerPan.update(status[1])))
								

		# Tilt
		# Posicao
		if self.__args.head == False or self.servo.readByte(self.__SERVO_TILT,self.__STATUS) == 1:
			self.servo.writeWord(self.__SERVO_TILT, self.__SPEED, self.__min_speed)
			self.servo.writeWord(self.__SERVO_TILT,
							self.__GOAL_POS,
							int(self.servo.readWord(self.__SERVO_TILT,self.__PRESENT_POS) - self.__ControllerTilt.update(status[2])))
		
		bkb.write_int(Mem, 'VISION_TILT_DEG', abs(self.servo.readWord(self.__SERVO_TILT, self.__PRESENT_POS) - self.max_posTILT)*0.29)
		bkb.write_int(Mem, 'VISION_PAN_DEG', abs(self.servo.readWord(self.__SERVO_PAN , self.__PRESENT_POS) - self.cen_posPAN )*0.29)
		
#		bkb.write_int('VISION_MOTOR1_ANGLE', self.servo.readWord(self.__SERVO_TILT, self.__PRESENT_POS))
#		bkb.write_int('VISION_MOTOR2_ANGLE', self.servo.readWord(self.__SERVO_PAN, self.__PRESENT_POS))
		
		return [self.servo.readWord(self.__SERVO_PAN, self.__PRESENT_POS), self.servo.readWord(self.__SERVO_TILT, self.__PRESENT_POS)]

#----------------------------------------------------------------------------------------------------------------------------------

	def __setVarredura(self):
		# Crinado e setando
		cv2.namedWindow('Ajustar varredura - Head')
		cv2.createTrackbar('Val dir','Ajustar varredura - Head',0,1023,self.__nothing)
		cv2.createTrackbar('Val centro','Ajustar varredura - Head',0,1023,self.__nothing)
		cv2.createTrackbar('Val esq','Ajustar varredura - Head',0,1023,self.__nothing)
		
		cv2.createTrackbar('Val cima','Ajustar varredura - Head',0,1023,self.__nothing)
		cv2.createTrackbar('Val meio','Ajustar varredura - Head',0,1023,self.__nothing)
		cv2.createTrackbar('Val baixo','Ajustar varredura - Head',0,1023,self.__nothing)
		
		cv2.setTrackbarPos('Val dir','Ajustar varredura - Head', self.min_posPAN)
		cv2.setTrackbarPos('Val centro','Ajustar varredura - Head', self.cen_posPAN)
		cv2.setTrackbarPos('Val esq','Ajustar varredura - Head', self.max_posPAN)
		
		cv2.setTrackbarPos('Val cima','Ajustar varredura - Head', self.min_posTILT)
		cv2.setTrackbarPos('Val meio','Ajustar varredura - Head', self.cen_posTILT)
		cv2.setTrackbarPos('Val baixo','Ajustar varredura - Head', self.max_posTILT)
		
		self.servo.writeWord(self.__SERVO_PAN,self.__SPEED, 0)
		self.servo.writeWord(self.__SERVO_TILT,self.__SPEED, 0)
		
		cap = cv2.VideoCapture(0)
		while True:
			ret, frame = cap.read()
			if self.min_posPAN != cv2.getTrackbarPos('Val dir','Ajustar varredura - Head'):
				self.min_posPAN = cv2.getTrackbarPos('Val dir','Ajustar varredura - Head')
				self.servo.writeWord(self.__SERVO_TILT,self.__GOAL_POS, self.cen_posTILT)
				self.servo.writeWord(self.__SERVO_PAN,self.__VAL_MIN, self.min_posPAN)
				self.servo.writeWord(self.__SERVO_PAN,self.__GOAL_POS, self.min_posPAN)
			
			if self.cen_posPAN != cv2.getTrackbarPos('Val centro','Ajustar varredura - Head'):
				self.cen_posPAN = cv2.getTrackbarPos('Val centro','Ajustar varredura - Head')
				self.servo.writeWord(self.__SERVO_PAN,self.__GOAL_POS, self.cen_posPAN)
				self.servo.writeWord(self.__SERVO_TILT,self.__GOAL_POS, self.cen_posTILT)
			
			if self.max_posPAN != cv2.getTrackbarPos('Val esq','Ajustar varredura - Head'):
				self.max_posPAN = cv2.getTrackbarPos('Val esq','Ajustar varredura - Head')
				self.servo.writeWord(self.__SERVO_TILT,self.__GOAL_POS, self.cen_posTILT)
				self.servo.writeWord(self.__SERVO_PAN,self.__VAL_MAX, self.max_posPAN)
				self.servo.writeWord(self.__SERVO_PAN,self.__GOAL_POS, self.max_posPAN)
			
			if self.min_posTILT != cv2.getTrackbarPos('Val cima','Ajustar varredura - Head'):
				self.min_posTILT = cv2.getTrackbarPos('Val cima','Ajustar varredura - Head')
				self.servo.writeWord(self.__SERVO_PAN,self.__GOAL_POS, self.cen_posPAN)
				self.servo.writeWord(self.__SERVO_TILT,self.__VAL_MIN, self.min_posTILT)
				self.servo.writeWord(self.__SERVO_TILT,self.__GOAL_POS, self.min_posTILT)
			
			if self.cen_posTILT != cv2.getTrackbarPos('Val meio','Ajustar varredura - Head'):
				self.cen_posTILT = cv2.getTrackbarPos('Val meio','Ajustar varredura - Head')
				self.servo.writeWord(self.__SERVO_PAN,self.__GOAL_POS, self.cen_posPAN)
				self.servo.writeWord(self.__SERVO_TILT,self.__GOAL_POS, self.cen_posTILT)
			
			if self.max_posTILT != cv2.getTrackbarPos('Val baixo','Ajustar varredura - Head'):
				self.max_posTILT = cv2.getTrackbarPos('Val baixo','Ajustar varredura - Head')
				self.servo.writeWord(self.__SERVO_PAN,self.__GOAL_POS, self.cen_posPAN)
				self.servo.writeWord(self.__SERVO_TILT,self.__VAL_MAX, self.max_posTILT)
				self.servo.writeWord(self.__SERVO_TILT,self.__GOAL_POS, self.max_posTILT)
			
			cv2.imshow('Ajustar varredura - Head', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		cv2.destroyAllWindows()
		cap.release()

#----------------------------------------------------------------------------------------------------------------------------------

	def finalize(self):
		self.__Config.set('Offset', 'ID_19', str(self.cen_posTILT)+'\t;Offset Tilt')
		self.__Config.set('Offset', 'ID_20', str(self.cen_posPAN)+'\t;Offset Pan\n;Valores para o robo olhando para frente')
		
		self.__Config.set('Head', 'p_pan', str(self.__p_pan)+'\t;Ganho proporcinal para controle da posicao no pan')
		self.__Config.set('Head', 'i_pan', str(self.__i_pan)+'\t;Ganho integral para controle da posicao no pan')
		self.__Config.set('Head', 'd_pan', str(self.__d_pan)+'\t;Ganho derivativo para controle da posicao no pan\n')
		self.__Config.set('Head', 'p_tilt', str(self.__p_tilt)+'\t;Ganho proporcinal para controle da posicao no tilt')
		self.__Config.set('Head', 'i_tilt', str(self.__i_tilt)+'\t;Ganho integral para controle da posicao no tilt')
		self.__Config.set('Head', 'd_tilt', str(self.__d_tilt)+'\t;Ganho derivativo para controle da posicao no tilt\n;Ganho PID para a posicao\n')
		
		self.__Config.set('Head', 'min_vel', str(self.__min_speed)+'\t;Velocidade minima\n;Ganho P para a velocidade e velocidade minima')

#----------------------------------------------------------------------------------------------------------------------------------

	def __nothing(x):
		pass
