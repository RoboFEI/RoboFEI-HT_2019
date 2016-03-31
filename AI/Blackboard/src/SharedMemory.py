#coding: utf-8
 # ----------------------------------------------------------------------------
 # ****************************************************************************
 # * @file SharedMemory.py
 # * @author Isaac Jesus da Silva - ROBOFEI-HT - FEI 😛
 # * @version V0.0.2
 # * @created 08/09/2015
 # * @Modified 16/09/2015
 # * @e-mail isaac25silva@yahoo.com.br
 # * @brief Shared Memory
 # ****************************************************************************
 # ****************************************************************************
import ctypes
import time
import os


# Classe do BlackBoard--------------------------------------------------------------------
class SharedMemory(object):
# Classe que lê e escreve na memória compartilhada do sistema '''

    def shd_constructor(self,KEY):
        #print "Start the Class Blackboard"
        # Usando memoria compartilhada a partir das funções do c++-------------------------------------------------------
        try:
            self.testlib = ctypes.CDLL('../../build/lib/libblackboardpy.so') #chama a library que contem as funções em c++
        except OSError:
            self.testlib = ctypes.CDLL('../AI/build/lib/libblackboardpy.so') #chama a library que contem as funções em c++
        self.testlib.using_shared_memory.restype = ctypes.POINTER(ctypes.c_int)
        mem = self.testlib.using_shared_memory(KEY)         #using c++ function
        print 'python', mem
        self.testlib.read_float.restype = ctypes.c_float #defining the return type, that case defining float
        self.testlib.read_int.restype = ctypes.c_int #defining the return type, that case defining int
        return mem
        #--------------------------------------------------------------------------------------------------------------------

    # Criando função que escreve float--------------------------------------------------------
    def write_float(self, mem, variable, value):
        self.testlib.write_float(mem, ctypes.c_int(self.variable_float[variable]), ctypes.c_float(value))
    #-----------------------------------------------------------------------------------------


    # Criando função que escreve float--------------------------------------------------------
    def write_floatDynamic(self, mem, variable,index, value):
        self.testlib.write_float(mem, ctypes.c_int(self.variable_float[variable]+index), ctypes.c_float(value))
    #-----------------------------------------------------------------------------------------

    # Criando função que escreve float--------------------------------------------------------
    def write_int(self, mem, variable, value):
        self.testlib.write_int(mem, ctypes.c_int(self.variable_int[variable]), ctypes.c_int(int(value)))
    #-----------------------------------------------------------------------------------------

    # Criando função que lê float--------------------------------------------------------
    def read_float(self, mem, variable):
        return self.testlib.read_float(mem, ctypes.c_int(self.variable_float[variable]))
    #-----------------------------------------------------------------------------------------

    # Criando função que lê float--------------------------------------------------------
    def read_int(self, mem, variable):
        return self.testlib.read_int(mem, ctypes.c_int(self.variable_int[variable]))
    #-----------------------------------------------------------------------------------------

    variable_int = {
    "PLANNING_COMMAND" : 0,
    "PLANNING_PARAMETER_VEL": 1,
    "PLANNING_PARAMETER_ANGLE": 2,
    "IMU_STATE" : 3,
    "CONTROL_MOVING": 84,
    "CONTROL_ACTION": 13,
    "CONTROL_HEIGHT_A": 14,
    "CONTROL_HEIGHT_B": 15,
    "CONTROL_HEIGHT_C": 16,
    "DECISION_ACTION_A": 17,
    "DECISION_ACTION_B": 18,
    "DECISION_STATE": 19,
    "DECISION_POSITION_A": 20,
    "DECISION_POSITION_B": 21,
    "DECISION_POSITION_C": 22,
    "DECISION_BALL_POS": 23,
    "DECISION_OPP1_POS": 24,
    "DECISION_OPP2_POS": 25,
    "DECISION_OPP3_POS": 26,
    "COM_ACTION_ROBOT1": 27,
    "COM_ACTION_ROBOT2": 28,
    "COM_ACTION_ROBOT3": 29,
    "COM_STATE_ROBOT1": 30,
    "COM_STATE_ROBOT2": 31,
    "COM_STATE_ROBOT3": 32,
    "COM_POS_ROBOT1": 33,
    "COM_POS_ROBOT2": 34,
    "COM_POS_ROBOT3": 35,
    "COM_POS_BALL_ROBOT1": 36,
    "COM_POS_BALL_ROBOT2": 37,
    "COM_POS_BALL_ROBOT3": 38,
    "COM_POS_OPP_A_ROBOT1": 39,
    "COM_POS_OPP_A_ROBOT2": 40,
    "COM_POS_OPP_A_ROBOT3": 41,
    "COM_POS_OPP_A_ROBOT4": 42,
    "COM_POS_OPP_B_ROBOT1": 43,
    "COM_POS_OPP_B_ROBOT2": 44,
    "COM_POS_OPP_B_ROBOT3": 45,
    "COM_POS_OPP_B_ROBOT4": 46,
    "COM_POS_OPP_C_ROBOT1": 47,
    "COM_POS_OPP_C_ROBOT2": 48,
    "COM_POS_OPP_C_ROBOT3": 49,
    "COM_POS_OPP_C_ROBOT4": 50,
    "COM_REFEREE": 51,
    "LOCALIZATION_X": 52,
    "LOCALIZATION_Y": 53,
    "LOCALIZATION_THETA": 54,
    "VISION_BALL_LOST": 57,
    "VISION_BALL_PAN_ON": 58,
    "DECISION_ACTION_VISION": 59,
    "VISION_MOTOR1_GOAL": 60,
    "VISION_MOTOR2_GOAL": 61,
    "VISION_SEARCH_GOAL": 62,
    "VISION_LOST_GOAL": 63,
    "VISION_STATE": 64,
    "ROBOT_NUMBER": 65,
    "VISION_pos_servo1": 66,
    'VISION_pos_servo2': 67,
    'COM_POS_ORIENT_QUALIT_ROBOT_A': 68,
    'COM_POS_DIST_QUALIT_ROBOT_A': 69,
    'COM_POS_ORIENT_QUALIT_ROBOT_B': 70,
    'COM_POS_DIST_QUALIT_ROBOT_B': 71,
    'COM_POS_ORIENT_QUALIT_ROBOT_C': 72,
    'COM_POS_DIST_QUALIT_ROBOT_C': 73,
    'VISION_DELTA_ORIENT': 74,
    'LOCALIZATION_FIND_ROBOT': 75,
    'RECEIVED_ROBOT_SENDING': 76,
    'RECEIVED_QUAL_ORIENT': 77,
    'RECEIVED_QUAL_DIST': 78,
    'RECEIVED_ROBOT_SEEN': 79,
    'CONTROL_MESSAGES': 80,
    'ASKED_QUALIT_DIRECT': 81,
    'ASKED_QUALIT_DISTANCE': 82,
    'ASKED_RELATED_ROBOT': 83,
    'ROBOT_VIEW_ROTATE': 100,
    'CONTROL_MOVING': 84,
    }

    variable_float = {
    "VISION_BALL_DIST": 1,
    "VISION_DIST_GOAL": 2,
    "VISION_DIST_OPP1": 3,
    "VISION_DIST_OPP2": 4,
    "VISION_DIST_OPP3": 5,
    "IMU_GYRO_X": 6,
    "IMU_GYRO_Y": 7,
    "IMU_GYRO_Z": 8,
    "IMU_ACCEL_X": 9,
    "IMU_ACCEL_Y": 10,
    "IMU_ACCEL_Z": 11,
    "IMU_COMPASS_X": 12,
    "IMU_COMPASS_Y": 13,
    "IMU_COMPASS_Z": 14,
    "IMU_EULER_X": 15,
    "IMU_EULER_Y": 16,
    "IMU_EULER_Z": 17,
    "IMU_QUAT_X": 18,
    "IMU_QUAT_Y": 19,
    "IMU_QUAT_Z": 20,
    'VISION_AREA_SEGMENT': 21,
    'VISION_ANGLE_BALL':22,
    'VISION_ANGLE_GOAL':23,
    'VISION_ANGLE_OPP1':24,
    'VISION_ANGLE_OPP2':25,
    'VISION_ANGLE_OPP3':26,
    'VISION_DIST_RBT01':30,
    'VISION_DIST_RBT02':31,
    'VISION_DIST_RBT03':32,
    'VISION_DIST_RBT04':33,
    'VISION_DIST_RBT05':34,
    'VISION_DIST_RBT06':35,
    'VISION_DIST_RBT07':36,
    'VISION_DIST_RBT08':37,
    'VISION_DIST_RBT09':38,
    'VISION_DIST_RBT10':39,
    'VISION_DIST_RBT11':40,
    'VISION_ANGLE_RBT01':41,
    'VISION_ANGLE_RBT02':42,
    'VISION_ANGLE_RBT03':43,
    'VISION_ANGLE_RBT04':44,
    'VISION_ANGLE_RBT05':45,
    'VISION_ANGLE_RBT06':46,
    'VISION_ANGLE_RBT07':47,
    'VISION_ANGLE_RBT08':48,
    'VISION_ANGLE_RBT09':49,
    'VISION_ANGLE_RBT10':50,
    'VISION_ANGLE_RBT11':51,
    "VISION_TILT_DEG": 52,
    "VISION_PAN_DEG": 53,
    }
#------------------------------------------------------------------------------------------
