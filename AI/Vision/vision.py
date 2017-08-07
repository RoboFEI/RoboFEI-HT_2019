# coding: utf-8

# ---- List of execution parameters ----

import argparse

parser = argparse.ArgumentParser(description='Robot Vision', epilog= 'Responsável pela detecção dos objetos em campo./Responsible for detection of field objects.')

parser.add_argument('--camera', # Full name
				 '--ca', # Abbreviation for the name
				 action = "store_true", # Type variable
				 help = 'Calibra valor para a câmera.\\' \
						'Calibrates value for the camera.' # Description of the variable
				)

parser.add_argument('--visionball', # Full name
				 '--vb', # Abbreviation for the name
				 action = "store_true", # Type variable
				 help = 'Calibra valor para a visão da bola.\\' \
						'Calibrates value for ball view.' # Description of the variable
				)

parser.add_argument('--whiteball', # Full name
				 '--wb', # Abbreviation for the name
				 action = "store_true", # Type variable
				 help = 'Calibra valor o branco da bola.\\' \
						'Calibrate morphology used on the ball.' # Description of the variable
				)

parser.add_argument('--morphologyball', # Full name
				 '--mb', # Abbreviation for the name
				 action = "store_true", # Type variable
				 help = 'Calibra morfologia usadas na bola.\\' \
						'Calibrate morphology used on the ball.' # Description of the variable
				)

parser.add_argument('--withoutservo', # Full name
				 '--ws', # Abbreviation for the name
				 action = "store_true", # Type variable
				 help = 'Sem servos.\\' \
						'Without servomotors.' # Description of the variable
				)

parser.add_argument('--head', # Full name
				 '--he', # Abbreviation for the name
				 action = "store_true", # Type variable
				 help = 'Configurando parâmetros do controle da cabeça.\\' \
						'Configuring head control parameters.' # Description of the variable
				)

parser.add_argument('--localization', # Full name
				 '--lo', # Abbreviation for the name
				 action = "store_true", # Type variable
				 help = 'Configurando parâmetros da localização.\\' \
						'Configuring location parameters.' # Description of the variable
				)

parser.add_argument('--camerageometric', # Full name
				 '--cg', # Abbreviation for the name
				 action = "store_true", # Type variable
				 help = 'Inicia o treinamento da modelagem geometrica de câmera.\\' \
						'Begins geometric camera modeling training.' # Description of the variable
				)

args = parser.parse_args()

# ---- Imports ----

# Libraries to be used
import sys
sys.path.append('./include')
sys.path.append('./src')

# The standard libraries used in the vision system

# Used class developed by RoboFEI-HT
from CameraCapture import * # Class responsible for performing the observation of domain
from LocalizationVision import * # Class responsible for performing the observation of domain
from MainFunctions import * # Declaration the main functions
from HeadControl import * # 

# ---- Main Code ----

# Starting processes

args.withoutservo = False
if args.camerageometric == True and args.withoutservo == True:
	raise VisionException(6, 'It is not possible to do training without a servo, to remove the withoutservo function')

killedProcess() # Recognize external kill

try:
	camera = CameraCapture(args) # Object responsible for the camera
except VisionException as e:
	exit()

if args.withoutservo == False:
	try:
		head = HeadControl(args)
	except VisionException as e:
		camera.finalize()
		exit()

# Main loop

while True:
	try:
		observation = camera.currentObservation()
		if 'frame' not in observation.keys():
			time.sleep(0.1)
			continue
	except KeyboardInterrupt:
		os.system('clear') # Cleaning terminal
		print "Keyboard interrupt detected"
		break
	except VisionException as e:
		break

# Finishing processes

if args.withoutservo == False:
	head.finalize()
camera.finalize()