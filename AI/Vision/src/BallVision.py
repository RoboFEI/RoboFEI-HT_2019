import numpy as np
import os
import cv2
import ctypes

try:
    from ConfigParser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0


class VisionBall (object):

	Config = None #Para ler o Config.ini
	__ball_cascade = None #Para o XML
	
	## Variaveis de Controle
	# Segmentacao do campo
	__h_low = None
	__h_high  = None
	__s_low = None
	__s_high = None
	__v_low = None
	__v_high = None
	
	__size_element_input = None
	__erosion_input = None
	__dilation_input = None
	__blur_input = None
	__cut_sensitivity_seg_input = None
	
	#Haar bola
	__minSize_HaarBall = None
	__maxSize_HaarBall = None
	__neighbours_HaarBall = None
	__scaleFactor_HaarBall = None
	__cut_sensitivity_haar_input = None
	
	__lower = None
	__upper = None
	__kernel = None
	
	__args = None # Argumentos de entrada
	
	#Contrele logica
	__contframelost = 1
	__framelostball = 10
	__inspos = None
	__status = np.array([0,-1,-1,-1])
	
	__media = 10

#----------------------------------------------------------------------------------------------------------------------------------
	def __init__(self,args):
		self.__ball_cascade=cv2.CascadeClassifier('../Data/Ball.xml')
		
		# Read config.ini
		self.Config = ConfigParser()
		self.__readConfig()
		self.__updateElement()
		
		self.__args=args
		
		# Calibrar
		if args.visionball == True:
			self.__calibrar()

#----------------------------------------------------------------------------------------------------------------------------------

	def __calibrar(self):
		passo = 0
		cap = cv2.VideoCapture(0) #Abrindo camera
		ret = cap.set(3,1280)
		ret = cap.set(4,720)
		
		while passo != 2:
			if passo == 0:
				cv2.namedWindow('Mascara - Bola')
				#cv2.namedWindow('Frame cortado  - Bola', cv2.WINDOW_AUTOSIZE)
				
				# create trackbars for color change
				cv2.createTrackbar('H_Low','Mascara - Bola',0,255,self.__nothing)
				cv2.createTrackbar('H_High','Mascara - Bola',0,255,self.__nothing)
				cv2.createTrackbar('S_Low','Mascara - Bola',0,255,self.__nothing)
				cv2.createTrackbar('S_High','Mascara - Bola',255,255,self.__nothing)
				cv2.createTrackbar('V_Low','Mascara - Bola',0,255,self.__nothing)
				cv2.createTrackbar('V_High',				'Mascara - Bola',	255,	255,	self.__nothing)
				cv2.createTrackbar('Size element', 'Mascara - Bola', 1, 25, self.__nothing)
				cv2.createTrackbar('Erosion','Mascara - Bola',1,25,self.__nothing)
				cv2.createTrackbar('Dilation','Mascara - Bola',1,25,self.__nothing)
				cv2.createTrackbar('Blur','Mascara - Bola',0,25,self.__nothing)
				cv2.createTrackbar('Cut sensitivity','Mascara - Bola',0,500,self.__nothing)
				
				#Setando valoeres iniciais
				cv2.setTrackbarPos('H_Low','Mascara - Bola', self.__h_low)
				cv2.setTrackbarPos('H_High','Mascara - Bola', self.__h_high)
				cv2.setTrackbarPos('S_Low','Mascara - Bola', self.__s_low)
				cv2.setTrackbarPos('S_High','Mascara - Bola', self.__s_high)
				cv2.setTrackbarPos('V_Low','Mascara - Bola', self.__v_low)
				cv2.setTrackbarPos('V_High','Mascara - Bola', self.__v_high)
				cv2.setTrackbarPos('Size element','Mascara - Bola', self.__size_element_input)
				cv2.setTrackbarPos('Erosion','Mascara - Bola', self.__erosion_input)
				cv2.setTrackbarPos('Dilation','Mascara - Bola', self.__dilation_input)
				cv2.setTrackbarPos('Blur','Mascara - Bola', self.__blur_input)
				cv2.setTrackbarPos('Cut sensitivity','Mascara - Bola', self.__cut_sensitivity_seg_input)
				
				os.system("v4l2-ctl -d /dev/video0 -c focus_auto=0 && v4l2-ctl -d /dev/video0 -c focus_absolute=0")
				while True:
					ret, frame = cap.read()
					
					self.__size_element_input = cv2.getTrackbarPos('Size element','Mascara - Bola')
					self.__erosion_input = cv2.getTrackbarPos('Erosion','Mascara - Bola')
					self.__dilation_input = cv2.getTrackbarPos('Dilation','Mascara - Bola')
					self.__blur_input = cv2.getTrackbarPos('Blur', 'Mascara - Bola')
					self.__h_high  = cv2.getTrackbarPos('H_High','Mascara - Bola')
					self.__h_low = cv2.getTrackbarPos('H_Low','Mascara - Bola')
					self.__s_high = cv2.getTrackbarPos('S_High','Mascara - Bola')
					self.__s_low = cv2.getTrackbarPos('S_Low','Mascara - Bola')
					self.__v_high = cv2.getTrackbarPos('V_High','Mascara - Bola')
					self.__v_low = cv2.getTrackbarPos('V_Low','Mascara - Bola')
					self.__cut_sensitivity_seg_input = cv2.getTrackbarPos('Cut sensitivity','Mascara - Bola')
					
					if self.__size_element_input ==0:
						self.__size_element_input = 1
						cv2.setTrackbarPos('Size element','Mascara - Bola', self.__size_element_input)
					
					if self.__blur_input % 2 == 1 :
						pass
					else:
						self.__blur_input = self.__blur_input + 1
						cv2.setTrackbarPos('Blur', 'Mascara - Bola', self.__blur_input)
					
					self.__updateElement()
					
					mask_verde = self.__applyMask(frame)
					cut = self.__cutFrame(mask_verde)
					
					frame_campo = frame[cut[2]:cut[3], cut[0]:cut[1]]
					
					mostra = cv2.bitwise_and(frame,frame,mask=mask_verde)
					mostra = cv2.resize(mostra, (0,0), fx=640.0/1920, fy=640.0/1920)
					
					cv2.imshow('Mascara - Video', mostra)
					
#					frame_campo = cv2.resize(frame_campo, (0,0), fx=640.0/1024, fy=640.0/1024)
					if np.all(cut != -1) == True:
						frame = cv2.resize(frame, (0,0), fx=640.0/1920, fy=640.0/1920)
						if frame_campo.shape[0] < 10 or frame_campo.shape[1] < 10:#This is for error control
							print "Calibration Error: Frame too small for Segmentation"
						else:
						        cv2.imshow('Frame cortado  - Bola', frame_campo)
					
					if cv2.waitKey(1) & 0xFF == ord('q'):
						break
				passo += 1
			
			elif passo == 1:
				cv2.destroyAllWindows()
				cv2.namedWindow('Calibrar Haar - Bola')
			
				# create trackbars for color change
				cv2.createTrackbar('Min size','Calibrar Haar - Bola',1,255,self.__nothing)
				cv2.createTrackbar('Max size','Calibrar Haar - Bola',1,10000,self.__nothing)
				cv2.createTrackbar('Neighbours','Calibrar Haar - Bola',1,255,self.__nothing)
				cv2.createTrackbar('Scalefactor','Calibrar Haar - Bola',1,255,self.__nothing)
				cv2.createTrackbar('Cut sensitivity','Calibrar Haar - Bola',1,255,self.__nothing)
			
				#Setando valoeres iniciais
				cv2.setTrackbarPos('Min size','Calibrar Haar - Bola', self.__minSize_HaarBall)
				cv2.setTrackbarPos('Max size','Calibrar Haar - Bola', self.__maxSize_HaarBall)
				cv2.setTrackbarPos('Neighbours','Calibrar Haar - Bola', self.__neighbours_HaarBall)
				cv2.setTrackbarPos('Scalefactor','Calibrar Haar - Bola', int((self.__scaleFactor_HaarBall-1)*100))
				cv2.setTrackbarPos('Cut sensitivity','Calibrar Haar - Bola', int(self.__cut_sensitivity_haar_input*100))
				
				os.system("v4l2-ctl -d /dev/video0 -c focus_auto=0 && v4l2-ctl -d /dev/video0 -c focus_absolute=0")
				pos = None
				while True:
					ret, frame = cap.read()
				
					self.__minSize_HaarBall = cv2.getTrackbarPos('Min size','Calibrar Haar - Bola')
					self.__maxSize_HaarBall = cv2.getTrackbarPos('Max size','Calibrar Haar - Bola')
					self.__neighbours_HaarBall = cv2.getTrackbarPos('Neighbours','Calibrar Haar - Bola')
					self.__scaleFactor_HaarBall = (cv2.getTrackbarPos('Scalefactor','Calibrar Haar - Bola')/100.0)+1
					self.__cut_sensitivity_haar_input = cv2.getTrackbarPos('Cut sensitivity','Calibrar Haar - Bola')/100.0
				
					if self.__scaleFactor_HaarBall ==1:
						self.__scaleFactor_HaarBall = 1.01
						cv2.setTrackbarPos('Scalefactor','Calibrar Haar - Bola', 1)
						
					if self.__cut_sensitivity_haar_input == 0:
						self.__cut_sensitivity_haar_input = 0.01
						cv2.setTrackbarPos('Cut sensitivity','Calibrar Haar - Bola', 1)
					
					if self.__neighbours_HaarBall % 2 == 0:
						self.__neighbours_HaarBall += 1
						cv2.setTrackbarPos('Neighbours','Calibrar Haar - Bola', self.__neighbours_HaarBall)
				
					self.__updateElement()
					
					if pos is None:
						balls = self.__haarBall(frame)
						if balls is not ():
							pos = [9999, 9999, -1, -1, 0]
							for (x,y,w,h) in balls:
								cv2.rectangle(	frame,
												(x,y),
												(x+w,y+h),
												(0,255,0),
												2)
								if pos[0] > x:
									pos[0] = x
								if pos[1] > y:
									pos[1] = y
								if pos[2] < x + w:
									pos[2] = x + w
								if pos[3] < y + h:
									pos[3] = y + h
							pos[4] = ((pos[3] - pos[1]) + (pos[2] - pos[0]))/2
					else:
						cut =  pos
						pos = None
						if cut[0] - cut[4]*self.__cut_sensitivity_haar_input < 0:
							cut[0] = cut[4]*self.__cut_sensitivity_haar_input
						if cut[1] - cut[4]*self.__cut_sensitivity_haar_input < 0:
							cut[1] = cut[4]*self.__cut_sensitivity_haar_input
						if cut[2] + cut[4]*self.__cut_sensitivity_haar_input > 2304:
							cut[2] = 2304 - cut[4]*self.__cut_sensitivity_haar_input
						if cut[3] + cut[4]*self.__cut_sensitivity_haar_input > 1296:
							cut[3] = 1296 - cut[4]*self.__cut_sensitivity_haar_input
						
						frame_cut = frame[cut[1] - cut[4]*self.__cut_sensitivity_haar_input:cut[3] + cut[4]*self.__cut_sensitivity_haar_input, cut[0] - cut[4]*self.__cut_sensitivity_haar_input:cut[2] + cut[4]*self.__cut_sensitivity_haar_input]
						cv2.rectangle(	frame,
												(int(cut[0] - cut[4]*self.__cut_sensitivity_haar_input), int(cut[1] - cut[4]*self.__cut_sensitivity_haar_input)),
												(int(cut[2] + cut[4]*self.__cut_sensitivity_haar_input), int(cut[3] + cut[4]*self.__cut_sensitivity_haar_input)),
												(255, 0, 0),
												2)
												
						try:
							if frame_cut.shape[0] < 10 or frame_cut.shape[1] < 10 :
								cv2.imshow('Corte - Bola', frame_cut)					
						except :
							print "Calibration Error: Frame too small to cut"
							pass
												
    					#cv2.imshow('Corte - Bola', frame_cut)
						
						balls = self.__haarBall(frame_cut)
						if balls is not ():
							pos = [9999, 9999, -1, -1, 0]
							for (x,y,w,h) in balls:
								cv2.rectangle(	frame,
												(x + int(cut[0] - cut[4]*self.__cut_sensitivity_haar_input), y + int(cut[1] - cut[4]*self.__cut_sensitivity_haar_input)),
												(x + int(cut[0] - cut[4]*self.__cut_sensitivity_haar_input) + w, y + int(cut[1] - cut[4]*self.__cut_sensitivity_haar_input) + h),
												(0, 255, 0),
												2)
								if pos[0] > x + cut[0] - cut[4]*self.__cut_sensitivity_haar_input:
									pos[0] = x + cut[0] - cut[4]*self.__cut_sensitivity_haar_input
								if pos[1] > y + cut[1] - cut[4]*self.__cut_sensitivity_haar_input:
									pos[1] = y + cut[1] - cut[4]*self.__cut_sensitivity_haar_input
								if pos[2] < x + w + cut[0] - cut[4]*self.__cut_sensitivity_haar_input:
									pos[2] = x + w + cut[0] - cut[4]*self.__cut_sensitivity_haar_input
								if pos[3] < y + h + cut[1] - cut[4]*self.__cut_sensitivity_haar_input:
									pos[3] = y + h + cut[1] - cut[4]*self.__cut_sensitivity_haar_input
							pos[4] = ((pos[3] - pos[1]) + (pos[2] - pos[0]))/2
						else:
							pos = None
					
					frame = cv2.resize(frame, (0,0), fx=640.0/1920, fy=640.0/1920)
					if frame.shape[0] < 10 or frame.shape[1] < 10:#This is for error control
						print "Calibration Error: Frame too small for Haar"
					else:
						cv2.imshow('Calibrar Haar - Bola', frame)
				
					if cv2.waitKey(1) & 0xFF == ord('q'):
						break
				passo += 1
			
		cv2.destroyAllWindows()
		cap.release()

#----------------------------------------------------------------------------------------------------------------------------------

	def __updateElement(self):
		#Elementos de deteccao
		self.__lower = np.array([self.__h_low,self.__s_low,self.__v_low])
		self.__upper = np.array([self.__h_high,self.__s_high,self.__v_high])
		
		self.__kernel = np.ones((self.__size_element_input,self.__size_element_input),np.uint8)

#----------------------------------------------------------------------------------------------------------------------------------

	def __readConfig(self):
		# Read file config.ini
		while True:
			if self.Config.read('../Data/config.ini') and 'Vision Ball' in self.Config.sections():
				print 'Leitura do config.ini, Vision Ball'
				self.__h_low = self.Config.getint('Vision Ball', 'h_low')
				self.__h_high  = self.Config.getint('Vision Ball', 'h_high')
				self.__s_low = self.Config.getint('Vision Ball', 'S_Low')
				self.__s_high = self.Config.getint('Vision Ball', 'S_High')
				self.__v_low = self.Config.getint('Vision Ball', 'V_Low')
				self.__v_high = int(self.Config.get('Vision Ball', 'V_High'))
			
				self.__size_element_input = self.Config.getint('Vision Ball','size_element')
				self.__erosion_input = self.Config.getint('Vision Ball','erosion_iterations')
				self.__dilation_input = self.Config.getint('Vision Ball', 'dilation_iterations')
				self.__blur_input = self.Config.getint('Vision Ball', 'Blur')
				self.__cut_sensitivity_seg_input = int(self.Config.get('Vision Ball', 'cut_sensitivity_seg'))

				self.__minSize_HaarBall = self.Config.getint('Vision Ball', 'minSize_HaarBall')
				self.__maxSize_HaarBall = self.Config.getint('Vision Ball', 'maxSize_HaarBall')
				self.__neighbours_HaarBall = self.Config.getint('Vision Ball', 'neighbours_HaarBall')
				self.__scaleFactor_HaarBall = self.Config.getfloat('Vision Ball', 'scaleFactor_HaarBall')
				self.__cut_sensitivity_haar_input = float(self.Config.get('Vision Ball', 'cut_sensitivity_HaarBall'))
				break

			else:
				print 'Falha na leitura do config.ini, crinando arquivo\nVision Ball inexistente, criando valores padrao'
				self.Config = ConfigParser()
				self.Config.write('../Data/config.ini')
		
				self.Config.add_section('Vision Ball')
				self.Config.set('Vision Ball', 'H_Low', str(0)+'\t\t\t;Valor minimo para o hue')
				self.Config.set('Vision Ball', 'H_High', str(255)+'\t;Valor maximo para o hue')
				self.Config.set('Vision Ball', 'S_Low', str(0)+'\t\t\t;Valor minimo para o saturation')
				self.Config.set('Vision Ball', 'S_High', str(255)+'\t;Valor maximo para o saturation')
				self.Config.set('Vision Ball', 'V_Low', str(0)+'\t\t\t;Valor minimo para o value')
				self.Config.set('Vision Ball', 'V_High', str(255)+'\t;Valor maximo para o value\n')
	
				self.Config.set('Vision Ball','size_element', str(2)+'\t\t\t\t;Tamanho do elemento')
				self.Config.set('Vision Ball','erosion_iterations', str(0)+'\t;Numero de vezes para erosao')
				self.Config.set('Vision Ball', 'dilation_iterations', str(0)+'\t;Numero de vezes para dilacao')
				self.Config.set('Vision Ball', 'Blur', str(0)+'\t\t\t\t\t\t\t\t;Raio das bordas')
				self.Config.set('Vision Ball', 'cut_sensitivity_seg', str(0)+'\t;Quao sensivel o corte do frame deve ser para segmentacao\n')
	
				self.Config.set('Vision Ball', 'minSize_HaarBall',str(50)+'\t\t\t\t\t;Minimo tamanho do quadro')
				self.Config.set('Vision Ball', 'maxSize_HaarBall',str(1000)+'\t\t\t\t;Maximo tamanho do quadro')
				self.Config.set('Vision Ball', 'neighbours_HaarBall', str(5)+'\t\t\t\t;Vizinhos proximos')
				self.Config.set('Vision Ball', 'scaleFactor_HaarBall', str(1.29)+'\t\t;Fator de escala')
				self.Config.set('Vision Ball', 'cut_sensitivity_HaarBall', str(1)+'\t;Quao sensivel o corte do frame deve ser para Haar\n')
			
				with open('../Data/config.ini', 'wb') as configfile:
					self.Config.write(configfile)
		
#----------------------------------------------------------------------------------------------------------------------------------

	def detect(self,frame,res):
		if self.__status[0] == 2 and self.__contframelost<=5:
			#print "Localizado bola" #Debug
			posx = (self.__inspos[len(self.__inspos)-1,0]+10)*(res[0]/20)
			posy = (self.__inspos[len(self.__inspos)-1,1]+10)*(res[1]/20)
			raio = (self.__inspos[len(self.__inspos)-1,2]*(res[1]/20))/2
			
			esquerda = int( posx - raio * (1 + self.__cut_sensitivity_haar_input + self.__contframelost * 0.5/self.__cut_sensitivity_haar_input ) )
			if esquerda < 0:
				esquerda = 0
			direita = int( posx + raio * (1 + self.__cut_sensitivity_haar_input + self.__contframelost * 0.5/self.__cut_sensitivity_haar_input ) ) + 5
			
			cima = int( posy - raio * (1 + self.__cut_sensitivity_haar_input + self.__contframelost * 0.5/self.__cut_sensitivity_haar_input ) )
			if cima < 0:
				cima = 0
			
			baixo = int( posy + raio * (1 + self.__cut_sensitivity_haar_input + self.__contframelost * 0.5/self.__cut_sensitivity_haar_input ) ) + 15
			
			cut = np.array([esquerda, direita, cima, baixo])
			
			# Aplicando haar
			if cut[1]-cut[0]>=self.__minSize_HaarBall and cut[3]-cut[2]>=self.__minSize_HaarBall:	# Valor aceitavel para o Haar, campo encontrado
				frame_campo = frame[cut[2]:cut[3], cut[0]:cut[1]]
				balls = self.__haarBall(frame_campo)
			
				if balls is not ():	# Bola encontrada
					self.__updateStatus(np.array([2,	# Bola encontrada
															(balls[0,0]+cut[0]+balls[0,2]/2)*(20.0/res[0])-10,	# Posicao relativa do centro em x
															(balls[0,1]+cut[2]+balls[0,3]/2)*(20.0/res[1])-10,	# Posicao relativa do centro em y
															(balls[0,2]+balls[0,3])/(0.1*res[1])]))	# Diametro da bola
					mask_verde = 0
				else:	# Bola nao encontrada
					mask_verde = self.__applyMask(frame)
					moment = self.__findMoment(mask_verde,res)
					self.__updateStatus(np.array([1,moment[0],moment[1],-1]))
					
			else:	# Campo nao encontrado
				mask_verde = 0
				frame_campo = 0
				self.__updateStatus(np.array([0,-1,-1,-1]))
			
		else:
			# Cria a mascara
			mask_verde = self.__applyMask(frame)
			
			# Pegando limites de corte
			cut = self.__cutFrame(mask_verde)
			
			# Aplicando haar
			if cut[1]-cut[0]>=self.__minSize_HaarBall and cut[3]-cut[2]>=self.__minSize_HaarBall and np.all(cut !=-1):	# Valor aceitavel para o Haar, campo encontrado
				frame_campo = frame[cut[2]:cut[3], cut[0]:cut[1]]
				balls = self.__haarBall(frame_campo)
			
				if balls is not ():	# Bola encontrada
					self.__updateStatus(np.array([2,	# Bola encontrada
															(balls[0,0]+cut[0]+balls[0,2]/2)*(20.0/res[0])-10,	# Posicao relativa do centro em x
															(balls[0,1]+cut[2]+balls[0,3]/2)*(20.0/res[1])-10,	# Posicao relativa do centro em y
															(balls[0,2]+balls[0,3])/(0.1*res[1])]))	# Diametro da bola
				else:	# Bola nao encontrada
					moment = self.__findMoment(mask_verde,res)
					self.__updateStatus(np.array([1,moment[0],moment[1],-1]))
					
			else:	# Campo nao encontrado
				frame_campo = 0
				balls = ()
				self.__updateStatus(np.array([0,-1,-1,-1]))

#---------------------------------------Para VB

		if self.__args.visionball == True or self.__args.head == True:
#			if frame_campo is not 0 and np.all(cut != -1) == True:
#				frame_campo = cv2.resize(frame_campo, (0,0), fx=640.0/res[0], fy=640.0/res[0]) 
#				cv2.imshow('Frame cortado  - Bola', frame_campo)
#			else:
#				cv2.destroyWindow('Frame cortado  - Bola')
			
			if mask_verde is not 0:
				mostra = cv2.bitwise_and(frame,frame,mask=mask_verde)
				mostra = cv2.resize(mostra, (0,0), fx=640.0/res[0], fy=640.0/res[0])
				cv2.imshow('Mascara - Bola', mostra)
#			else:
#				cv2.destroyWindow('Mascara - Bola')
			
			if self.__status[0] == 0:
				cv2.putText(frame,
										"Campo nao encontrado",
										(int(0.029*res[0]),int(0.0625*res[0])),
										cv2.FONT_HERSHEY_PLAIN,
										0.0031*res[0],
										(0,255,0),
										 thickness=int(0.0015*res[0]))
			elif self.__status[0] == 1:
				cv2.rectangle(frame,
											(cut[0],cut[2]),
											(cut[1],cut[3]),
											(255,255,0),
											2)
				cv2.putText(frame,
										"Bola nao encontrada",
										(int(0.029*res[0]),int(0.0625*res[0])),
										cv2.FONT_HERSHEY_PLAIN,
										0.0031*res[0],
										(0,255,0),
										thickness=int(0.0015*res[0]))
			elif self.__status[0] == 2:
				cv2.rectangle(frame,
											(cut[0],cut[2]),
											(cut[1],cut[3]),
											(255,255,0),
											2)
				if balls is not ():
					for (x,y,w,h) in balls:
						cv2.rectangle(frame,
													(x+cut[0],y+cut[2]),
													(x+cut[0]+w,y+cut[2]+h),
													(0,255,0),
													2)
			
			frame = cv2.resize(frame, (0,0), fx=640.0/res[0], fy=640.0/res[0])
			cv2.imshow('Video - Bola', frame)

#---------------------------------------Para VB

		return self.__status

#----------------------------------------------------------------------------------------------------------------------------------

	def __updateStatus(self, status):
		if status[0] == 0:
			if self.__contframelost <= self.__framelostball and self.__status[0] ==2:
				self.__status = np.array([2,0,0,self.__status[3]])
			else:
				self.__status = status
			self.__contframelost += 1
		
		elif status[0] == 1:
			if self.__contframelost <= self.__framelostball and self.__status[0] ==2:
				self.__status = np.array([2,0,0,self.__status[3]])
			else:
				self.__status = status
			self.__contframelost += 1
		
		elif status[0] == 2:
			if self.__contframelost != 0:
				self.__contframelost = 0
				self.__inspos = np.array([[status[1], status[2], status[3]]])
				median = np.array([status[1], status[2], status[3]])
				self.__status = np.array([2, median[0], median[1], median[2]])
			else:
				if len(self.__inspos) >= self.__media:
					self.__inspos = np.delete(self.__inspos, 0, 0)
				self.__inspos = np.concatenate((self.__inspos, np.array([[status[1], status[2], status[3]]])), axis=0)
				median = self.__inspos.sum(axis=0)/len(self.__inspos)
				self.__status = np.array([2, median[0], median[1], median[2]])

#----------------------------------------------------------------------------------------------------------------------------------

	def __findMoment(self,mask_verde,res):
		momento = cv2.moments(mask_verde)
		try:
			cx = float(momento['m10']/(momento['m00']*res[0]))
			cy = float(momento['m01']/(momento['m00']*res[1]))
			
			if cx <= 0.3333:
					cx = -1
			elif cx > 0.3333 and cx < 0.6667:
				cx = 0
			else:
				cx = 1
			
			if cy <= 0.3333:
				cy = -1
			elif cy > 0.3333 and cy < 0.6667:
				cy = 0
			else:
				cy = 1
			
			return np.array([cx,cy])
		except ZeroDivisionError:
			return np.array([0,0])

#----------------------------------------------------------------------------------------------------------------------------------

	def __haarBall(self,frame):
		try:
			balls = self.__ball_cascade.detectMultiScale(frame,
														minNeighbors=self.__neighbours_HaarBall,
														scaleFactor=self.__scaleFactor_HaarBall,
														minSize=(self.__minSize_HaarBall,self.__minSize_HaarBall),
														maxSize=(self.__maxSize_HaarBall,self.__maxSize_HaarBall))
		except cv2.error as e:
			balls = ()
			print 'Falha no Haar'
			
		return balls

#----------------------------------------------------------------------------------------------------------------------------------

	def __applyMask(self, frame):
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, self.__lower, self.__upper)
		
		## erosion
		mask = cv2.erode(mask,self.__kernel,iterations=self.__erosion_input)
		
		## dilation
		mask = cv2.dilate(mask,self.__kernel,iterations=self.__dilation_input)
		
		return cv2.medianBlur(mask,self.__blur_input)

#----------------------------------------------------------------------------------------------------------------------------------

	def __cutFrame(self, mask_verde):
		#cima
		cima = -1
		for i in range(0,len(mask_verde),5):
			if sum(mask_verde[i])>int(255*self.__cut_sensitivity_seg_input): #minimo pixels
				cima = i
				break
		
		#baixo
		baixo = -1
		for i in range(len(mask_verde)-1,-1,-5):
			if sum(mask_verde[i])>int(255*self.__cut_sensitivity_seg_input): #minimo pixels
				baixo = i
				break
		
		# Girando mascara
		mask_verde=mask_verde.transpose()
		
		#esp p/ dir
		esquerda = -1
		for i in range(0,len(mask_verde),5):
			if sum(mask_verde[i])>int(255*self.__cut_sensitivity_seg_input): #minimo 4 pixels
				esquerda = i
				break
		
		#dir p/ esp
		direita = -1
		for i in range(len(mask_verde)-1,0,-5):
			if sum(mask_verde[i])>int(255*self.__cut_sensitivity_seg_input): #minimo 4 pixels
				direita = i
				break
		
		return np.array([esquerda,direita,cima,baixo])

#----------------------------------------------------------------------------------------------------------------------------------

	def finalize(self):
		self.Config.set('Vision Ball', 'H_Low', str(self.__h_low)+'\t\t\t;Valor minimo para o hue')
		self.Config.set('Vision Ball', 'H_High', str(self.__h_high)+'\t;Valor maximo para o hue')
		self.Config.set('Vision Ball', 'S_Low', str(self.__s_low)+'\t\t\t;Valor minimo para o saturation')
		self.Config.set('Vision Ball', 'S_High', str(self.__s_high)+'\t;Valor maximo para o saturation')
		self.Config.set('Vision Ball', 'V_Low', str(self.__v_low)+'\t\t\t;Valor minimo para o value')
		self.Config.set('Vision Ball', 'V_High', str(self.__v_high)+'\t;Valor maximo para o value\n')

		self.Config.set('Vision Ball','size_element', str(self.__size_element_input)+'\t\t\t\t;Tamanho do elemento')
		self.Config.set('Vision Ball','erosion_iterations', str(self.__erosion_input)+'\t;Numero de vezes para erosao')
		self.Config.set('Vision Ball', 'dilation_iterations', str(self.__dilation_input)+'\t;Numero de vezes para dilacao')
		self.Config.set('Vision Ball', 'Blur', str(self.__blur_input)+'\t\t\t\t\t\t\t\t;Raio das bordas')
		self.Config.set('Vision Ball', 'cut_sensitivity_seg', str(self.__cut_sensitivity_seg_input)+'\t;Quao sensivel o corte do frame deve ser para segmentacao\n')

		self.Config.set('Vision Ball', 'minSize_HaarBall',str(self.__minSize_HaarBall)+'\t\t\t\t\t;Minimo tamanho do quadro')
		self.Config.set('Vision Ball', 'maxSize_HaarBall',str(self.__maxSize_HaarBall)+'\t\t\t\t;Maximo tamanho do quadro')
		self.Config.set('Vision Ball', 'neighbours_HaarBall', str(self.__neighbours_HaarBall)+'\t\t\t\t;Vizinhos proximos')
		self.Config.set('Vision Ball', 'scaleFactor_HaarBall', str(self.__scaleFactor_HaarBall)+'\t\t;Fator de escala')
		self.Config.set('Vision Ball', 'cut_sensitivity_HaarBall', str(self.__cut_sensitivity_haar_input)+'\t;Quao sensivel o corte do frame deve ser para Haar\n')

		with open('../Data/config.ini', 'wb') as configfile:
			self.Config.write(configfile)

#----------------------------------------------------------------------------------------------------------------------------------

	def __nothing(x,y):
		pass
