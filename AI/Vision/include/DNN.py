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
import pandas as pd # 

# The standard libraries used in the visual memory system.
import cv2 # OpenCV library used for image processing.
import numpy as np # Library used for operations with matrix and array.

# Libraries to supporting the network execution using Tensorflow.
import tensorflow as tf
from utils import label_map_util
from utils import visualization_utils as vis_util

# Used class developed by RoboFEI-HT.
from BasicThread import * # Base class with primary functions

## Class DNN
# .
class DNN(BasicThread):
    
    # ---- Variables ----
    
    ## __PATH_TO_CKPT
    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    __PATH_TO_CKPT = "frozen_inference_graph.pb"
    
    ## __PATH_TO_LABELS
    # List of the strings that is used to add correct label for each box.
    __PATH_TO_LABELS = "object-detection.pbtxt"
    
    ## __numclasses
    # The Number of classes that are detected by the network.
    __numclasses = None
    
    ## __detection_graph
    # .
    __detection_graph = None
    
    ## __sess
    # .
    __sess = None
    
    ## __label
    # .
    __label = None
    
    ## __parameters
    # .
    __parameters = None
    
    imagetensor = detectionboxes = detectionscores = detectionclasses = numdetections = category_index = None
    
    ## __unzipNetwork
    # .
    def __unzipNetwork(self, name):
        tar = tarfile.open("./Data/"+name+".tar.gz")
        tar.extractall(path=self.__EXTRACTION_DIRECTORY)
        tar.close()
    
    ## instantiatingDNNVariables
    # Used to create/instantiate the variables that will be used by DNN in detecting objects.
    def __instantiatingDNNVariables(self):
        # Reading network file.
        self.__detection_graph = tf.Graph()
        with self.__detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.__EXTRACTION_DIRECTORY+ "/" +self.__PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
    
        label_map = label_map_util.load_labelmap(self.__EXTRACTION_DIRECTORY+ "/" +self.__PATH_TO_LABELS)
        
        filelabel = str(label_map).replace("\n", "").replace(" ", "").replace("{", "").replace("}", "")
        self.__label = {}
        for text in filelabel.split("item")[1:]:
            key = float(text[-1])
            name = text.split("\"")[1]
            self.__label[key] = name
        
        if self._args.dnn == True:
            self.__numclasses = str(label_map).count("id")
            categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.__numclasses, use_display_name=True)
            self.category_index = label_map_util.create_category_index(categories)
    
        # Creating a section to run the detection.
        with self.__detection_graph.as_default():
            self.__sess = tf.Session(
                graph=self.__detection_graph,
                config=tf.ConfigProto(
                    intra_op_parallelism_threads=1,
                    inter_op_parallelism_threads=1
                )
            )
            
            self.imagetensor = self.__detection_graph.get_tensor_by_name('image_tensor:0')
            self.detectionboxes = self.__detection_graph.get_tensor_by_name('detection_boxes:0')
            self.detectionscores = self.__detection_graph.get_tensor_by_name('detection_scores:0')
            self.detectionclasses = self.__detection_graph.get_tensor_by_name('detection_classes:0')
            self.numdetections = self.__detection_graph.get_tensor_by_name('num_detections:0')
    
    ## Constructor Class
    def __init__(self, a):
        super(DNN, self).__init__(a, "DNN", "Parameters")
        
        # Creating and updating default parameter values.
        self.__parameters = {
            "network_name": "rede",
            "threshold_to_train": 0.2,
        }
        self.__parameters = self._conf.readVariables(self.__parameters)
        
        # Creating neural network.
        self.__unzipNetwork(self.__parameters["network_name"])
        self.__instantiatingDNNVariables()
        
    ## detectDNN
    # .
    def __detectDNN(self, img):
        # Actual detection.
        image_np_expanded = np.expand_dims(img, axis=0)
        (boxes, scores, classes, num) = self.__sess.run(
            [self.detectionboxes, self.detectionscores, self.detectionclasses, self.numdetections],
            feed_dict={self.imagetensor: image_np_expanded}
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
                self.category_index,
                use_normalized_coordinates=True,
                line_thickness=2,
                min_score_thresh=self.__parameters["threshold_to_train"],
            )
        
        # Creating DataFrame detection.
        classes = classes.tolist()
        for i in xrange(len(classes[0])):
            classes[0][i] = self.__label[classes[0][i]]
        
        df = pd.DataFrame()
        df["classes"] = classes[0]
        df["scores"] = scores[0]
        df["boxes"] = boxes[0].tolist()
        
        return df, img
    
    ## detect
    # .
    def detect(self, observation):
        objects, observation['frame'] = self.__detectDNN(observation['frame'])
    
    observation = {}
    
    observation['frame'] = cv2.imread("/home/vinicius/objectDetect_clear/Train/imagenstreino/frames0_040.jpg")
    
    detect(observation)
    
    #self-iPython detec