import sys
sys.path.append("./src")
import numpy as np
import os
import cv2
import ctypes
import argparse
import time
from math import log,exp,tan,radians

import tarfile
import tempfile
import zipfile

from defs import *

from scipy.stats import mode
from servo import Servo

from BallVision import *
from PanTilt import *

import sys

""" Initiate the path to blackboard (Shared Memory)"""
sys.path.append('../../Blackboard/src/')
"""Import the library Shared memory """
from SharedMemory import SharedMemory 
""" Treatment exception: Try to import configparser from python. Write and Read from config.ini file"""
try:
    """There are differences in versions of the config parser
    For versions > 3.0 """
    from ConfigParser import ConfigParser
except ImportError:
    """For versions < 3.0 """
    from ConfigParser import ConfigParser 

""" Instantiate bkb as a shared memory """
bkb = SharedMemory()
""" Config is a new configparser """
config = ConfigParser()
""" Path for the file config.ini:"""
config.read('../../Control/Data/config.ini')
""" Mem_key is for all processes to know where the blackboard is. It is robot number times 100"""
mem_key = int(config.get('Communication', 'no_player_robofei'))*100 
"""Memory constructor in mem_key"""
Mem = bkb.shd_constructor(mem_key)




#----------------------------------------------------------------------------------------------------------------------------------

def statusBall(positionballframe):
	global lista
	if positionballframe[0] == 0:
		lista = []
		print "Campo nao encontrado"
		
	if positionballframe[0] == 1:
		lista = []
		mens = "Bola nao encontrada, campo "
		
		if positionballframe[1] == -1:
			mens += "a esquerda"
		elif positionballframe[1] == 1:
			mens += "a direita"
		else:
			mens += "esta no meio"
		
		if positionballframe[2] == -1:
			mens += " cima"
		elif positionballframe[2] == 1:
			mens += " baixo"
		else:
			mens += " centro"
		print mens
	if positionballframe[0] == 2:
		if bkb.read_float(Mem, 'VISION_TILT_DEG') < 50:
			lista.append(21.62629757*exp(0.042451235*bkb.read_float(Mem, 'VISION_TILT_DEG')))#8.48048735
			##bkb.write_float(Mem, 'VISION_BALL_DIST', 430*tan(radians(bkb.read_float(Mem, 'VISION_TILT_DEG'))))
			print 'Dist using tilt angle: ', bkb.read_float(Mem, 'VISION_BALL_DIST')
			#0.0848048735*exp(0.042451235*bkb.read_int('VISION_TILT_DEG')
			#print "Distancia da Bola func 1 em metros: " + str(0.0848048735*exp(0.042451235*bkb.read_int('VISION_MOTOR1_ANGLE')))
			#print "Bola encontrada na posicao x: " + str(round(positionballframe[1],2)) + " y: " + str(round(positionballframe[2],2)) + " e diametro de: " + str(round(positionballframe[3],2))
		else:
			#print "Bola encontrada na posicao x: " + str(round(positionballframe[1],2)) + " y: " + str(round(positionballframe[2],2)) + " e diametro de: " + str(round(positionballframe[3],2))
			#print "Distancia da Bola func 2 em metros: " + str(4.1813911146*pow(positionballframe[3],-1.0724682465))
			lista.append(418.13911146*pow(positionballframe[3],-1.0724682465))
			print 'Dist using pixel size: ', bkb.read_float(Mem, 'VISION_BALL_DIST')
		if len(lista) == 1:
			dist_media = lista[0]
		else:
			if len(lista) >= 1:
				lista.pop(0)
			dist_media = float(sum(lista)/len(lista))
		bkb.write_float(Mem, 'VISION_BALL_DIST', dist_media)
		bkb.write_int(Mem,'VISION_LOST', 0)
		
		
#		print "Bola encontrada = " + str(bkb.read_int('VISION_LOST_BALL'))
#		print "Posicao servo 1 tilt = " + str(bkb.read_int('VISION_MOTOR1_ANGLE'))
	else:
	    bkb.write_int(Mem,'VISION_LOST', 1)
#	    print "Bola Perdida = " + str(bkb.read_int('VISION_LOST_BALL'))

	    
#----------------------------------------------------------------------------------------------------------------------------------

def readResolutions(Config):
	if 'Resolutions' not in Config.sections():
		print "Resolutions inexistente, criando valores padrao"
		Config.add_section('Resolutions')
	if len(Config.options('Resolutions')) == 0:
		Config.set('Resolutions','1','320x180')
		Config.set('Resolutions','2','640x480\n\t;Resolucoes nao pode ter valores iguais')
		with open('../Data/config.ini', 'wb') as configfile:
			Config.write(configfile)
		
	a = 0
	Resolutions = np.chararray((len(Config.options('Resolutions')), 2), itemsize=11)
	Resolutions[:]='0'
	for i in Config.options('Resolutions'):
			if '\n' in Config.get('Resolutions',i).rpartition('\n'):
				Resolutions[a,0] = Config.get('Resolutions',i).rpartition('\n')[0]
			else:
				Resolutions[a,0] = Config.get('Resolutions',i).rpartition('\n')[2]
			a += 1


	for a in range(0, len(Config.options('Resolutions'))):
			Resolutions[a,1] = Resolutions[a,0].rpartition('x')[2]
			Resolutions[a,0] = Resolutions[a,0].rpartition('x')[0]

	value = np.array( np.zeros( ( len( Config.options('Resolutions') ), 2 ), dtype=np.int ) )

	for i in range(0, len( Config.options('Resolutions') )):
			for j in range(0, 2):
				value[i,j] = int(Resolutions[i,j])
			
	return np.sort(value, axis=0)

#----------------------------------------------------------------------------------------------------------------------------------

def setResolution(status):
	global resolutions
	global atualres
	global dis
	global maxRadio
	
	if status[0] == 2:
#		print "Max: " + str(		maxRadio*pow(razao,atualres)		)
#		print "Min: " + str(		maxRadio*pow(razao,atualres+1)-2		)
		if status[3]>maxRadio*pow(razao,atualres):
			atualres -=1
			ret = cap.set(3,resolutions[atualres,0])
			ret = cap.set(4,resolutions[atualres,1])
		elif status[3]<maxRadio*pow(razao,atualres+1)-2:
			atualres +=1
			ret = cap.set(3,resolutions[atualres,0])
			ret = cap.set(4,resolutions[atualres,1])
	
	elif atualres != len(resolutions)/2 - 1:
		atualres = len(resolutions)/2 - 1
		ret = cap.set(3,resolutions[atualres,0])
		ret = cap.set(4,resolutions[atualres,1])

#----------------------------------------------------------------------------------------------------------------------------------

def classify(image_files, net, transformer,
             mean_file=None, labels=None, batch_size=None):
    """
    Classify some images against a Caffe model and print the results

    Arguments:
    caffemodel -- path to a .caffemodel
    deploy_file -- path to a .prototxt
    image_files -- list of paths to images

    Keyword arguments:
    mean_file -- path to a .binaryproto
    labels_file path to a .txt file
    use_gpu -- if True, run inference on the GPU
    """
#    if channels == 3:
#        mode = 'RGB'
#    elif channels == 1:
#        mode = 'L'
#    else:
#        raise ValueError('Invalid number for channels: %s' % channels)
    images = [image_files]

    # Classify the image
    scores = forward_pass(images, net, transformer, batch_size=batch_size)

    #
    # Process the results
    #
    results = {}

    indices = (-scores).argsort()[:, :7]  # take top 9 results
    classifications = []
    for image_index, index_list in enumerate(indices):
        result = []
        for i in index_list:
            # 'i' is a category in labels and also an index into scores
            if labels is None:
                label = 'Class #%s' % i
            else:
                label = labels[i]
            result.append((label, round(100.0 * scores[image_index, i], 4)))
        classifications.append(result)

    for index, classification in enumerate(classifications):
        print '{:-^80}'.format(' Prediction for image ')
        for label, confidence in classification:
            print '{:9.4%} - "{}"'.format(confidence / 100.0, label)
            results[label] = confidence / 100.0
        print
    return classification[0][0], results

#----------------------------------------------------------------------------------------------------------------------------------

def unzip_archive(archive):
    """
    Unzips an archive into a temporary directory
    Returns a link to that directory

    Arguments:
    archive -- the path to an archive file
    """
    assert os.path.exists(archive), 'File not found - %s' % archive

    tmpdir = os.path.join(tempfile.gettempdir(), os.path.basename(archive))
    assert tmpdir != archive  # That wouldn't work out

    if os.path.exists(tmpdir):
        # files are already extracted
        pass
    else:
        if tarfile.is_tarfile(archive):
            print 'Extracting tarfile ...'
            with tarfile.open(archive) as tf:
                tf.extractall(path=tmpdir)
        elif zipfile.is_zipfile(archive):
            print 'Extracting zipfile ...'
            with zipfile.ZipFile(archive) as zf:
                zf.extractall(path=tmpdir)
        else:
            raise ValueError('Unknown file type for %s' % os.path.basename(archive))
    return tmpdir

#----------------------------------------------------------------------------------------------------------------------------------

def soma_prob(mem_p, gamma = 0.9):
    #gamma  o valor de desconto
    memory_temp_size = len(mem_p.values())

    soma = {}
    for key, value in mem_p.iteritems():
        somador = 0
        for mem_index in range(memory_temp_size):
            somador = (gamma**(memory_temp_size-mem_index-1))*value[mem_index] + somador
#             print mem_p[index][mem_index],
#         print somador
        soma[key] = somador
#     print soma
    return soma














if __name__ == '__main__':


    """ Instantiate bkb as a shared memory """
#    bkb = SharedMemory()


    parser = argparse.ArgumentParser(description='Robot Vision', epilog= 'Responsavel pela deteccao dos objetos em campo / Responsible for detection of Field objects')
    parser.add_argument('--visionball', '--vb', action="store_true", help = 'Calibra valor para a visao da bola')
    parser.add_argument('--withoutservo', '--ws', action="store_true", help = 'Servos desligado')
    parser.add_argument('--head', '--he', action="store_true", help = 'Configurando parametros do controle da cabeca')
    # Positional arguments
    parser.add_argument('archive', help='Path to a DIGITS model archive')
    # Optional arguments
    parser.add_argument('--batch-size', type=int)
    parser.add_argument('--nogpu', action='store_true', help="Don't use the GPU")



#----------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------
#Inicio programa


    args = vars(parser.parse_args())
    args2 = parser.parse_args()

    ball = VisionBall(args2)

    tmpdir = unzip_archive(args['archive'])
    caffemodel = None
    deploy_file = None
    mean_file = None
    labels_file = None
    for filename in os.listdir(tmpdir):
        full_path = os.path.join(tmpdir, filename)
        if filename.endswith('.caffemodel'):
            caffemodel = full_path
        elif filename == 'deploy.prototxt':
            deploy_file = full_path
        elif filename.endswith('.binaryproto'):
            mean_file = full_path
        elif filename == 'labels.txt':
            labels_file = full_path
        else:
            print 'Unknown file:', filename

    assert caffemodel is not None, 'Caffe model file not found'
    assert deploy_file is not None, 'Deploy file not found'

    # Load the model and images
    net = get_net(caffemodel, deploy_file, use_gpu=False)
    transformer = get_transformer(deploy_file, mean_file)
    _, channels, height, width = transformer.inputs['data']
    labels = read_labels(labels_file)

    #create index from label to use in decicion action
    number_label =  dict(zip(labels, range(len(labels))))
    print number_label

    #buffer_t = np.zeros((10) , dtype=np.int)
    memory_temp_size = 10
    num_itens = len(labels)
    bucket = [0 for i in range(memory_temp_size)]
    mem_p = {}
    for i in labels:
        mem_p[i] = bucket



    if args2.withoutservo == False:
    	head = Pantilt(args2, ball.Config)

    lista = []
    minRadio = 0.8
    maxRadio = 20.0

    resolutions = readResolutions(ball.Config)
    atualres = len(resolutions)/2 -1
    razao = pow(minRadio/maxRadio, 1.0/len(resolutions))
    
    cap = cv2.VideoCapture(0) #Abrindo camera

    ret = cap.set(3,resolutions[atualres,0])
    ret = cap.set(4,resolutions[atualres,1])

    if args2.withoutservo == False:
    	posheadball = np.array([head.cen_posTILT,head.cen_posPAN]) #Iniciando valores iniciais da posicao da bola
    os.system("v4l2-ctl -d /dev/video0 -c focus_auto=0 && v4l2-ctl -d /dev/video0 -c focus_absolute=0")

    while True:

    	bkb.write_int(Mem,'VISION_WORKING', 1) # Variavel da telemetria
	
    	#Salva o frame
	
###    	for i in xrange(0,3):
        ret, frame = cap.read()
	
    	positionballframe = ball.detect(frame,np.array([resolutions[atualres,0],resolutions[atualres,1]]))
	
	#status
    	statusBall(positionballframe)
	
    	if args2.withoutservo == False:
    		posheadball = head.mov(positionballframe,posheadball,Mem, bkb)
#		if head.checkComm() == False:
#			print "Out of communication with servos!"
#			break
	
    	setResolution(positionballframe)
	
#	if args2.visionball == True or args2.head == True:
#		print "Resolucao: " + str(resolutions[atualres,0]) + "x" + str(resolutions[atualres,1])
	
    	if cv2.waitKey(1) & 0xFF == ord('q'):
    		break
#	raw_input("Pressione enter pra continuar")

    if args2.withoutservo == False:
    	head.finalize()
    ball.finalize()
    cv2.destroyAllWindows()
    cap.release()
