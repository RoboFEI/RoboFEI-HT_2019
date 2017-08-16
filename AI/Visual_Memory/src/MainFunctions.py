# coding: utf-8

# Libraries to be used.
import signal # Class used for external interrupt detection.

# Used class developed by RoboFEI-HT
from VisualMemoryException import *  # Used to handle exceptions

## signal_term_handler
def signal_term_handler(signal, frame):
	raise VisionException(3, '')

## killedProcess
def killedProcess( ):
	signal.signal(signal.SIGTERM, signal_term_handler)

## readDataLandmarks
def readDataLandmarks(taglandmark, mem):
	x = mem.read_float('VISION_LAND_X')
	y = mem.read_float('VISION_LAND_Y')
	time = mem.read_float('VISION_LAND_TIME')
	mem.write_float('VISION_LAND_TAG', 0)
	return [taglandmark, x, y, time ]