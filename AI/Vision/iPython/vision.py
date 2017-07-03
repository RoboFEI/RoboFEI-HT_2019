# coding: utf-8

# ---- List of execution parameters ----

import argparse

parser = argparse.ArgumentParser(description='Robot Vision', epilog= 'Responsável pela detecção dos objetos em campo / Responsible for detection of Field objects')
parser.add_argument('--visionball', '-vb', action="store_true", help = 'Calibra valor para a visão da bola')
parser.add_argument('--withoutservo', '-ws', action="store_true", help = 'Sem servos')
parser.add_argument('--head', '-he', action="store_true", help = 'Configurando parâmetros do controle da cabeça')

args = parser.parse_args()

# ---- Imports ----

# Libraries to be used
import sys
sys.path.append('./include')
sys.path.append('./src')

# The standard libraries used in the vision system

# Used class developed by RoboFEI-HT
from CameraCapture import * # Class responsible for performing the observation of domain
from MainFunctions import * # Declaration the main functions

# ---- Main Code ----

# Starting processes

killedProcess() # Recognize external kill

# Creating shared memory (blackboard)
bkb = SharedMemory()
mem = bkb.shd_constructor(0)

camera = CameraCapture(bkb, mem) # Object responsible for the camera

# Main loop

while True:
	try:
		frame = camera.currentObservation()
		sleep(2)
	except KeyboardInterrupt:
		os.system('clear') # Cleaning terminal
		print "Keyboard interrupt detected"
		break
	except VisionException as e:
		if e.numbererror == 3:
			break

# Finishing processes

camera.finalize()
cv2.destroyAllWindows()