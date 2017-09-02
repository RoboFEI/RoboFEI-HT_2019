# coding: utf-8

# Libraries to be used.
import signal # Class used for external interrupt detection.

# Used class developed by RoboFEI-HT
from VisionException import *  # Used to handle exceptions

def signal_term_handler(signal, frame):
	raise VisionException(3, '')

def killedProcess():
	signal.signal(signal.SIGTERM, signal_term_handler)