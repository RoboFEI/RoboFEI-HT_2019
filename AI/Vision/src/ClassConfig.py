from ConfigParser import ConfigParser

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
		
		self.max_count_lost_frame = None
		self.max_count_lost_frame_far_ball = None
		self.head_up = None
		self.cut_edge_image = None

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
		self.when_ball_up = None
		self.when_ball_down = None
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
				self.max_count_lost_frame_far_ball =   self.Config.getint('Basic Settings', 'max_count_lost_frame_far_ball')
				self.head_up = self.Config.getint('Basic Settings', 'head_up')
				self.cut_edge_image = self.Config.getint('Basic Settings', 'cut_edge_image')

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
				self.when_ball_up = self.Config.getint('Distance Limits (Pixels)', 'when_ball_up')
				self.when_ball_down = self.Config.getint('Distance Limits (Pixels)', 'when_ball_down')			
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
				self.Config.set('Basic Settings', 'max_count_lost_frame_far_ball'        , str(30)+'\t;Quanto que o robo espera apos achar a bola de longe')
				self.Config.set('Basic Settings', 'head_up'        , str(70)+'\t;Quanto que a cabeca sobe quando bola esta acima')
				self.Config.set('Basic Settings', 'cut_edge_image'        , str(150)+'\t;Corta as bordas pretas da imagem')

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
				self.Config.set('Distance Limits (Pixels)', 'when_ball_up', str(222) + '\t\t\t;Y screen for ball on up screen')
				self.Config.set('Distance Limits (Pixels)', 'when_ball_dpwn', str(333) + '\t\t\t;Y screen for ball on down screen')	

				with open('../Data/config.ini', 'wb') as configfile:
					self.Config.write(configfile)

