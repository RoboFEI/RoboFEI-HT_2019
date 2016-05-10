import ctypes

class Servo(object):

	def __init__(self,posTILT,posPAN):
		print "Start the Class Servo"
		# Usando memoria compartilhada a partir das funcoes do c++-------------------------------------------------------
		ctypes.cdll.LoadLibrary("../../build/lib/libvision.so")
		self.visionlib = ctypes.CDLL('../../build/lib/libvision.so') #chama a lybrary que contem as funcoes em c++
		self.visionlib.initServo.restype = ctypes.c_bool #defining the return type, that case defining bool
		if self.visionlib.initServo(ctypes.c_int(posTILT), ctypes.c_int(posPAN)):  #Conecta no servo do Pan Tilt
			exit (0)

		self.visionlib.dxlReadByte.restype = ctypes.c_int #defining the return type, that case defining int
		self.visionlib.dxlReadWord.restype = ctypes.c_int #defining the return type, that case defining int

		self.visionlib.dxlWriteWord(ctypes.c_int(20), ctypes.c_int(34), ctypes.c_int(512)); # Usando apenas 50% do torque
		self.visionlib.dxlWriteWord(ctypes.c_int(19), ctypes.c_int(34), ctypes.c_int(512)); # Usando apenas 50% do torque
		#--------------------------------------------------------------------------------------------------------------------
		
	def readByte(self, ID, Pos):
		return self.visionlib.dxlReadByte( ctypes.c_int(ID), ctypes.c_int(Pos))
	
	def readWord(self, ID, Pos):
		return self.visionlib.dxlReadWord( ctypes.c_int(ID), ctypes.c_int(Pos))
	
	def writeByte(self, ID, Pos, value):
		self.visionlib.dxlWriteByte( ctypes.c_int(ID), ctypes.c_int(Pos), ctypes.c_int(value))
	
	def writeWord(self, ID, Pos, value):
		self.visionlib.dxlWriteWord( ctypes.c_int(ID), ctypes.c_int(Pos), ctypes.c_int(value))
