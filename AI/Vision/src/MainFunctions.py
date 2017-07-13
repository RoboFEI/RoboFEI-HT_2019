# coding: utf-8

import signal
from VisionException import *

def signal_term_handler(signal, frame):
	raise VisionException(3, '')

def killedProcess():
	signal.signal(signal.SIGTERM, signal_term_handler)