# coding: utf-8

# ****************************************************************************
# * @file: DNN.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class DNN
# ****************************************************************************

# ---- Imports ----

# The standard libraries used in the vision system.
import tarfile # Used for manipulating tar files.
import pandas as pd # Utilizado para manipular dados e tabelas
import os # Biblioteca utilizada para interação com o sistema
import shutil # Biblioteca utilizada para apagar diretorios com arquivos
import time # Libraries used for time management.

# The standard libraries used in the visual memory system.
import cv2 # OpenCV library used for image processing.
import numpy as np # Library used for operations with matrix and array.

# Libraries to supporting the network execution using Tensorflow.
import tensorflow as tf
from utils import label_map_util
from utils import visualization_utils as vis_util

# Used class developed by RoboFEI-HT.
from BasicProcesses import * # Standard and abstract class.

## Class DNN
# Class that implements object detection using a deep neural network (DNN).
class DNN(BasicProcesses):
    
    # ---- Variables ----
    
    ## EXTRACTION_DIRECTORY
    # Diretorio aonde será extraida a rede.
    __EXTRACTION_DIRECTORY = './Data/Rede'
    
    ## PATH_TO_CKPT
    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    __PATH_TO_CKPT = 'frozen_inference_graph.pb'
    
    ## PATH_TO_LABELS
    # List of the strings that is used to add correct label for each box.
    __PATH_TO_LABELS = 'object-detection.pbtxt'
    
    ## DIRECTORY_TRAINING_IMAGES
    # Directory where the training imagens will be saved.
    __DIRECTORY_TRAINING_IMAGES = './Train'
    
    ## numclasses
    # The Number of classes that are detected by the network.
    __numclasses = None
    
    ## detection_graph
    # Variavel de configuração do TensorFlow.
    __detection_graph = None
    
    ## sess
    # Variavel de execução do TensorFlow.
    __sess = None
    
    ## __label
    # Dicionario com as strings das classes que seram detectadas pela rede.
    __label = None
    
    ## __parameters
    # Parametros de configuração para a execução da DNN.
    __parameters = None
    
    # Variaveis de apoio do TensorFlow
    
    __imagetensor = __detectionboxes = __detectionscores = __detectionclasses = __numdetections = __category_index = None
    
    ## __unzipNetwork
    # .
    def __unzipNetwork(self, name):
        tar = tarfile.open('./Data/'+name+'.tar.gz')
        tar.extractall(path=self.__EXTRACTION_DIRECTORY)
        tar.close()
    
    ## instantiatingDNNVariables
    # Used to create/instantiate the variables that will be used by DNN in detecting objects.
    def __instantiatingDNNVariables(self):
        # Reading network file.
        self.__detection_graph = tf.Graph()
        with self.__detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.__EXTRACTION_DIRECTORY+ '/' +self.__PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
    
        label_map = label_map_util.load_labelmap(self.__EXTRACTION_DIRECTORY+ '/' +self.__PATH_TO_LABELS)
        
        filelabel = str(label_map).replace('\n', '').replace(' ', '').replace('{', '').replace('}', '').replace('\"', '\'')
        self.__label = {}
        for text in filelabel.split('item')[1:]:
            key = float(text.split(':')[-1])
            name = text.split('\'')[1]
            self.__label[key] = name
        
        if self._args.dnn == True:
            self.__numclasses = str(label_map).count('id')
            categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.__numclasses, use_display_name=True)
            self.__category_index = label_map_util.create_category_index(categories)
    
        # Creating a section to run the detection.
        with self.__detection_graph.as_default():
            self.__sess = tf.Session(
                graph=self.__detection_graph,
                config=tf.ConfigProto(
                    intra_op_parallelism_threads=1,
                    inter_op_parallelism_threads=1
                )
            )
            
            self.__imagetensor = self.__detection_graph.get_tensor_by_name('image_tensor:0')
            self.__detectionboxes = self.__detection_graph.get_tensor_by_name('detection_boxes:0')
            self.__detectionscores = self.__detection_graph.get_tensor_by_name('detection_scores:0')
            self.__detectionclasses = self.__detection_graph.get_tensor_by_name('detection_classes:0')
            self.__numdetections = self.__detection_graph.get_tensor_by_name('num_detections:0')
    
    ## trackbarThresholdMin
    # .
    def __trackbarThresholdMin(self, value):
        self.__parameters['threshold_to_train_min'] = min(value/100.0, self.__parameters['threshold_to_train_max']-0.01)
        cv2.setTrackbarPos('threshold_min', 'DNN - Parameters', int(self.__parameters['threshold_to_train_min']*100))
    
    ## trackbarThresholdMax
    # .
    def __trackbarThresholdMax(self, value):
        self.__parameters['threshold_to_train_max'] = max(value/100.0, self.__parameters['threshold_to_train_min']+0.01)
        cv2.setTrackbarPos('threshold_max', 'DNN - Parameters', int(self.__parameters['threshold_to_train_max']*100))
    
    ## Constructor Class
    def __init__(self, a):
        super(DNN, self).__init__(a, 'DNN', 'Parameters')
        
        # Creating and updating default parameter values.
        self.__parameters = {
            'network_name': 'rede',
            'threshold_to_train_min': 0.2,
            'threshold_to_train_max': 0.5,
        }
        self.__parameters = self._conf.readVariables(self.__parameters)
        
        # Creating neural network.
        self.__unzipNetwork(self.__parameters['network_name'])
        self.__instantiatingDNNVariables()
        
        if self._args.dnn == True:
            cv2.namedWindow('DNN - Parameters')
            cv2.createTrackbar(
                'threshold_min',
                'DNN - Parameters',
                int(self.__parameters['threshold_to_train_min']*100),
                100,
                self.__trackbarThresholdMin
            )
            cv2.createTrackbar(
                'threshold_max',
                'DNN - Parameters',
                int(self.__parameters['threshold_to_train_max']*100),
                100,
                self.__trackbarThresholdMax
            )
        
        if self._args.train == True:
            try:
                os.makedirs(self.__DIRECTORY_TRAINING_IMAGES+'/imagens to classify')
            except OSError:
                pass
            try:
                os.makedirs(self.__DIRECTORY_TRAINING_IMAGES+'/annotations DNN')
            except OSError:
                pass
        
    ## detectDNN
    # .
    def __detectDNN(self, img):
        # Actual detection.
        image_np_expanded = np.expand_dims(img, axis=0)
        (boxes, scores, classes, num) = self.__sess.run(
            [self.__detectionboxes, self.__detectionscores, self.__detectionclasses, self.__numdetections],
            feed_dict={self.__imagetensor: image_np_expanded}
        )
        
        if self._args.dnn == True:
            # Visualization of the results of a detection.
            img = cv2.resize(
                img,
                None,
                fx=380.0/img.shape[0],
                fy=380.0/img.shape[0]
            )
            vis_util.visualize_boxes_and_labels_on_image_array(
                img,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                self.__category_index,
                use_normalized_coordinates=True,
                line_thickness=2,
                min_score_thresh=self.__parameters['threshold_to_train_min'],
            )
        
        # Creating DataFrame detection.
        classes = classes.tolist()
        for i in xrange(len(classes[0])):
            classes[0][i] = self.__label[classes[0][i]]
        
        df = pd.DataFrame()
        df['classes'] = classes[0]
        df['scores'] = scores[0]
        df['boxes'] = boxes[0].tolist()
        
        return df, img
    
    ## detect
    # .
    def detect(self, observation):
        if self._args.train == True:
            image = observation['frame'].copy()
        
        objects, observation['frame'] = self.__detectDNN(observation['frame'])
        
        if self._args.dnn == True:
            cv2.imshow('DNN - Parameters', observation['frame'])
            if cv2.waitKey(1) == ord('q'):
                raise VisionException(5, 'DNN')
                
        if self._args.train == True:
            cv2.imwrite(self.__DIRECTORY_TRAINING_IMAGES+'/imagens to classify/'+'Robot-'+ time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(int(observation['time']))) + str(round(observation['time'] - int(observation['time']), 2))[1:] +'.jpg', image)
    
            if len(objects.scores) != 0:        
                text = '<annotation>\n\t<folder>imagens to classify</folder>\n\t<filename>Robot-'+ time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(int(observation['time']))) + str(round(observation['time'] - int(observation['time']), 2))[1:] +'.jpg</filename>\n\t<path>'+ os.getcwd() +'/'+ self.__DIRECTORY_TRAINING_IMAGES.split('/')[-1] +'/imagens to check/Robot-'+ time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(int(observation['time']))) + str(round(observation['time'] - int(observation['time']), 2))[1:] +'.jpg</path>\n\t<source>\n\t\t<database>Unknown</database>\n\t</source>\n\t<size>\n\t\t<width>'+ str(image.shape[1]) +'</width>\n\t\t<height>'+ str(image.shape[0]) +'</height>\n\t\t<depth>'+ str(image.shape[2]) +'</depth>\n\t</size>\n\t<segmented>0</segmented>'
    
                for classes, __, box in objects[(objects.scores > self.__parameters['threshold_to_train_min'])].values:
                    text += '\n\t<object>\n\t\t<name>'+ classes+ '</name>\n\t\t<pose>Unspecified</pose>\n\t\t<truncated>0</truncated>\n\t\t<difficult>0</difficult>\n\t\t<bndbox>\n\t\t\t<xmin>'+ str(int(box[1]*image.shape[1])) +'</xmin>\n\t\t\t<ymin>'+ str(int(box[0]*image.shape[0])) +'</ymin>\n\t\t\t<xmax>'+ str(int(box[3]*image.shape[1])) +'</xmax>\n\t\t\t<ymax>'+ str(int(box[2]*image.shape[0])) +'</ymax>\n\t\t</bndbox>\n\t</object>'
    
                text += '\n</annotation>'
    
                f = open(self.__DIRECTORY_TRAINING_IMAGES + '/annotations DNN/' + 'Robot-'+ time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(int(observation['time']))) + str(round(observation['time'] - int(observation['time']), 2))[1:] +'.xml', 'w')
                f.write(text)
                f.close()
        
        return objects[objects.scores > self.__parameters['threshold_to_train_max']]
    
    ## finalize
    # .
    def finalize(self):
        # Deleting extracted network
        try:
            shutil.rmtree('./Data/Rede')
        except OSError:
            pass
        
        if self._args.dnn == True:
            cv2.destroyAllWindows()
        
        # Saving parameter values
        self._end()