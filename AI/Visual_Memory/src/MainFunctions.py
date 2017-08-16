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
def readDataLandmarks( ):
	return None