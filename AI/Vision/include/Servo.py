# coding: utf-8

import ctypes

## Describes Class Servo - Communicate, Write and read from Vision Servo-motors

class Servo(object):
	
	## visionlib
	# .
	__visionlib = None
	
	## Constructor Class
	# Initializes the communication with the servos.
	def __init__(self,posTILT,posPAN):
		print "Start the Class Servo"
		
		# Using shared memory from C++ functions
		# Loads Vision library in the path /build/lib/libvision.so (Needs compilation and build)
		ctypes.cdll.LoadLibrary("../../build/lib/libvision.so")
		
		# Calls lybrary that contains C++ functions
		self.__visionlib = ctypes.CDLL('../../build/lib/libvision.so') 
		
		# Defines return type (boolean)
		self.__visionlib.initServo.restype = ctypes.c_bool 
		
		# Conects to Pan and tilt servos
		if self.__visionlib.initServo(ctypes.c_int(posTILT), ctypes.c_int(posPAN)):
			# Error treatament, if not connected to servos exit(0)
			raise VisionException(3, '')
		
		# Define return type of the method dxlReadByte (int)
		self.__visionlib.dxlReadByte.restype = ctypes.c_int 
		
		# Define return type of the method dxlReadWord (int)
		self.__visionlib.dxlReadWord.restype = ctypes.c_int 
		
		# Define initial torque with 50% to servo ID=20, parameter 34 seted with 512
		self.__visionlib.dxlWriteWord(ctypes.c_int(20), ctypes.c_int(34), ctypes.c_int(512)); 
		
		# Define initial torque with 50% to servo ID=19, parameter 34 seted with 512
		self.__visionlib.dxlWriteWord(ctypes.c_int(19), ctypes.c_int(34), ctypes.c_int(512)); 
		
	## readByte
	# Reads a byte from servo defined by ID.
	def readByte(self, ID, Pos):
		# Returns a byte from servo defined by ID in pos position
		return self.__visionlib.dxlReadByte( ctypes.c_int(ID), ctypes.c_int(Pos))
	
	## readWord
	# Reads a word from servo defined by ID.
	def readWord(self, ID, Pos):
		# Returns a word from servo defined by ID in pos position
		return self.__visionlib.dxlReadWord( ctypes.c_int(ID), ctypes.c_int(Pos))
	
	## writeByte
	# Writes a byte from servo defined by ID.
	def writeByte(self, ID, Pos, value):
		# Writes a byte in servo ID, Position Pos, and the value to be written
		self.__visionlib.dxlWriteByte( ctypes.c_int(ID), ctypes.c_int(Pos), ctypes.c_int(value))
	
	## writeWord
	# Writes a word from servo defined by ID.
	def writeWord(self, ID, Pos, value):
		# Writes a word in servo ID, Position Pos, and the value to be written
		self.__visionlib.dxlWriteWord( ctypes.c_int(ID), ctypes.c_int(Pos), ctypes.c_int(value))