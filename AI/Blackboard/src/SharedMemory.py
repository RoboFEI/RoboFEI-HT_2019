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
            try:
                self.testlib = ctypes.CDLL('../build/lib/libblackboardpy.so') #chama a library que contem as funções em c++
            except OSError:
                self.testlib = ctypes.CDLL('../AI/build/lib/libblackboardpy.so') #chama a library que contem as funções em c++
        self.testlib.using_shared_memory.restype = ctypes.POINTER(ctypes.c_int)
        mem = self.testlib.using_shared_memory(KEY)         #using c++ function
        #print 'python', mem
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
    'PLANNING_COMMAND' : 0,
    'PLANNING_PARAMETER_VEL': 1,
    'PLANNING_PARAMETER_ANGLE': 2,
    'IMU_STATE' : 3,
    'IMU_RESET': 4,
    'CONTROL_ACTION': 13,
    'CONTROL_HEIGHT_A': 14,
    'CONTROL_HEIGHT_B': 15,
    'CONTROL_HEIGHT_C': 16,
    'DECISION_ACTION_A': 17,
    'DECISION_ACTION_B': 18,
    'DECISION_STATE': 19,
    'DECISION_POSITION_A': 20,
    'DECISION_POSITION_B': 21,
    'DECISION_POSITION_C': 22,
    'DECISION_BALL_POS': 23,
    'DECISION_OPP1_POS': 24,
    'DECISION_OPP2_POS': 25,
    'DECISION_OPP3_POS': 26,
    'COM_ACTION_ROBOT1': 27,
    'COM_ACTION_ROBOT2': 28,
    'COM_ACTION_ROBOT3': 29,
    'COM_STATE_ROBOT1': 30,
    'COM_STATE_ROBOT2': 31,
    'COM_STATE_ROBOT3': 32,
    'COM_POS_ROBOT1': 33,
    'COM_POS_ROBOT2': 34,
    'COM_POS_ROBOT3': 35,
    'COM_POS_BALL_ROBOT1': 36,
    'COM_POS_BALL_ROBOT2': 37,
    'COM_POS_BALL_ROBOT3': 38,
    'COM_POS_OPP_A_ROBOT1': 39,
    'COM_POS_OPP_A_ROBOT2': 40,
    'COM_POS_OPP_A_ROBOT3': 41,
    'COM_POS_OPP_A_ROBOT4': 42,
    'COM_POS_OPP_B_ROBOT1': 43,
    'COM_POS_OPP_B_ROBOT2': 44,
    'COM_POS_OPP_B_ROBOT3': 45,
    'COM_POS_OPP_B_ROBOT4': 46,
    'COM_POS_OPP_C_ROBOT1': 47,
    'COM_POS_OPP_C_ROBOT2': 48,
    'COM_POS_OPP_C_ROBOT3': 49,
    'COM_POS_OPP_C_ROBOT4': 50,
    'COM_REFEREE': 51,
    'LOCALIZATION_X': 52,
    'LOCALIZATION_Y': 53,
    'LOCALIZATION_THETA': 54,
    'VISION_LOST': 57,
    'DECISION_SEARCH_ON': 58,
    'DECISION_ACTION_VISION': 59,
    'VISION_MOTOR1_GOAL': 60,
    'VISION_MOTOR2_GOAL': 61,
    'VISION_SEARCH_GOAL': 62,
    'VISION_LOST_GOAL': 63,
    'VISION_STATE': 64,
    'ROBOT_NUMBER': 65,
    'VISION_pos_servo1': 66,
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
    'CONTROL_MOVING': 84,
    'ROBOT_VIEW_ROTATE': 100,
    'CONTROL_WORKING': 101,
    'VISION_WORKING': 102,
    'LOCALIZATION_WORKING': 103,
    'DECISION_WORKING': 104,
    'IMU_WORKING': 105,
    'VOLTAGE': 106,
    'DECISION_LOCALIZATION': 107,
    'iVISION_FIELD': 108,
    }

    variable_float = {
        "IMU_GYRO_X": 1,
        "IMU_GYRO_Y": 2,
        "IMU_GYRO_Z": 3,
        "IMU_ACCEL_X": 4,
        "IMU_ACCEL_Y": 5,
        "IMU_ACCEL_Z": 6,
        "IMU_COMPASS_X": 7,
        "IMU_COMPASS_Y": 8,
        "IMU_COMPASS_Z": 9,
        "IMU_EULER_X": 10,
        "IMU_EULER_Y": 11,
        "IMU_EULER_Z": 12,
        "IMU_QUAT_X": 13,
        "IMU_QUAT_Y": 14,
        "IMU_QUAT_Z": 15,
        "VISION_AREA_SEGMENT": 16,
        "VISION_BALL_X": 17,
        "VISION_BALL_Y": 18,
        "VISION_BALL_TAG": 19,
        "VISION_LAND_X": 20,
        "VISION_LAND_Y": 21,
        "VISION_LAND_TAG": 22,
        "VISION_RB01_TAG": 23,
        "VISION_RB01_X": 24,
        "VISION_RB01_Y": 25,
        "VISION_RB01_TIME": 26,
        "VISION_RB02_TAG": 27,
        "VISION_RB02_X": 28,
        "VISION_RB02_Y": 29,
        "VISION_RB02_TIME": 30,
        "VISION_RB03_TAG": 31,
        "VISION_RB03_X": 32,
        "VISION_RB03_Y": 33,
        "VISION_RB03_TIME": 34,
        "VISION_RB04_TAG": 35,
        "VISION_RB04_X": 36,
        "VISION_RB04_Y": 37,
        "VISION_RB04_TIME": 38,
        "VISION_RB05_TAG": 39,
        "VISION_RB05_X": 40,
        "VISION_RB05_Y": 41,
        "VISION_RB05_TIME": 42,
        "VISION_RB06_TAG": 43,
        "VISION_RB06_X": 44,
        "VISION_RB06_Y": 45,
        "VISION_RB06_TIME": 46,
        "VISION_RB07_TAG": 47,
        "VISION_RB07_X": 48,
        "VISION_RB07_Y": 49,
        "VISION_RB07_TIME": 50,
        "VISION_RB08_TAG": 51,
        "VISION_RB08_X": 52,
        "VISION_RB08_Y": 53,
        "VISION_RB08_TIME": 54,
        "VISION_RB09_TAG": 55,
        "VISION_RB09_X": 56,
        "VISION_RB09_Y": 57,
        "VISION_RB09_TIME": 58,
        "VISION_RB10_TAG": 59,
        "VISION_RB10_X": 60,
        "VISION_RB10_Y": 61,
        "VISION_RB10_TIME": 62,
        "VISION_RB11_TAG": 63,
        "VISION_RB11_X": 64,
        "VISION_RB11_Y": 65,
        "VISION_RB11_TIME": 66,
        "VISION_RB12_TAG": 67,
        "VISION_RB12_X": 68,
        "VISION_RB12_Y": 69,
        "VISION_RB12_TIME": 70,
        "VISION_RB13_TAG": 71,
        "VISION_RB13_X": 72,
        "VISION_RB13_Y": 73,
        "VISION_RB13_TIME": 74,
        "VISION_RB14_TAG": 75,
        "VISION_RB14_X": 76,
        "VISION_RB14_Y": 77,
        "VISION_RB14_TIME": 78,
        "VISION_RB15_TAG": 79,
        "VISION_RB15_X": 80,
        "VISION_RB15_Y": 81,
        "VISION_RB15_TIME": 82,
        "VISION_RB16_TAG": 83,
        "VISION_RB16_X": 84,
        "VISION_RB16_Y": 85,
        "VISION_RB16_TIME": 86,
        "VISION_RB17_TAG": 87,
        "VISION_RB17_X": 88,
        "VISION_RB17_Y": 89,
        "VISION_RB17_TIME": 90,
        "VISION_RB18_TAG": 91,
        "VISION_RB18_X": 92,
        "VISION_RB18_Y": 93,
        "VISION_RB18_TIME": 94,
        "VISION_RB19_TAG": 95,
        "VISION_RB19_X": 96,
        "VISION_RB19_Y": 97,
        "VISION_RB19_TIME": 98,
        "VISION_RB20_TAG": 99,
        "VISION_RB20_X": 100,
        "VISION_RB20_Y": 101,
        "VISION_RB20_TIME": 102,
        "VISION_RB21_TAG": 103,
        "VISION_RB21_X": 104,
        "VISION_RB21_Y": 105,
        "VISION_RB21_TIME": 106,
        "VISION_RB22_TAG": 107,
        "VISION_RB22_X": 108,
        "VISION_RB22_Y": 109,
        "VISION_RB22_TIME": 110,
        "VISUAL_MEMORY_AL_01": 111,
        "VISUAL_MEMORY_AL_02": 112,
        "VISUAL_MEMORY_AL_03": 113,
        "VISUAL_MEMORY_AL_04": 114,
        "VISUAL_MEMORY_AL_05": 115,
        "VISUAL_MEMORY_AL_06": 116,
        "VISUAL_MEMORY_AL_07": 117,
        "VISUAL_MEMORY_AL_08": 118,
        "VISUAL_MEMORY_AL_09": 119,
        "VISUAL_MEMORY_AL_10": 120,
        "VISUAL_MEMORY_AL_11": 121,
        "VISUAL_MEMORY_OP_01": 122,
        "VISUAL_MEMORY_OP_02": 123,
        "VISUAL_MEMORY_OP_03": 124,
        "VISUAL_MEMORY_OP_04": 125,
        "VISUAL_MEMORY_OP_05": 126,
        "VISUAL_MEMORY_OP_06": 127,
        "VISUAL_MEMORY_OP_07": 128,
        "VISUAL_MEMORY_OP_08": 129,
        "VISUAL_MEMORY_OP_09": 130,
        "VISUAL_MEMORY_OP_10": 131,
        "VISUAL_MEMORY_OP_11": 132,
        "VISION_TILT_DEG": 133,
        "VISION_PAN_DEG": 134,
        "CBR_COORDINATOR": 135,
        "CBR_RUN": 136,
        "LOCALIZATION_BALL_X": 137,
        "LOCALIZATION_BALL_Y": 138,
        "LOCALIZATION_RBT01_X": 139,
        "LOCALIZATION_RBT01_Y": 140,
        "LOCALIZATION_RBT02_X": 141,
        "LOCALIZATION_RBT02_Y": 142,
        "LOCALIZATION_RBT03_X": 143,
        "LOCALIZATION_RBT03_Y": 144,
        "LOCALIZATION_RBT04_X": 145,
        "LOCALIZATION_RBT04_Y": 146,
        "LOCALIZATION_RBT05_X": 147,
        "LOCALIZATION_RBT05_Y": 148,
        "LOCALIZATION_RBT06_X": 149,
        "LOCALIZATION_RBT06_Y": 150,
        "LOCALIZATION_RBT07_X": 151,
        "LOCALIZATION_RBT07_Y": 152,
        "LOCALIZATION_RBT08_X": 153,
        "LOCALIZATION_RBT08_Y": 154,
        "LOCALIZATION_RBT09_X": 155,
        "LOCALIZATION_RBT09_Y": 156,
        "LOCALIZATION_RBT10_X": 157,
        "LOCALIZATION_RBT10_Y": 158,
        "LOCALIZATION_RBT11_X": 159,
        "LOCALIZATION_RBT11_Y": 160,
        "LOCALIZATION_OPP01_X": 161,
        "LOCALIZATION_OPP01_Y": 162,
        "LOCALIZATION_OPP02_X": 163,
        "LOCALIZATION_OPP02_Y": 164,
        "LOCALIZATION_OPP03_X": 165,
        "LOCALIZATION_OPP03_Y": 166,
        "LOCALIZATION_OPP04_X": 167,
        "LOCALIZATION_OPP04_Y": 168,
        "LOCALIZATION_OPP05_X": 169,
        "LOCALIZATION_OPP05_Y": 170,
        "LOCALIZATION_OPP06_X": 171,
        "LOCALIZATION_OPP06_Y": 172,
        "LOCALIZATION_OPP07_X": 173,
        "LOCALIZATION_OPP07_Y": 174,
        "LOCALIZATION_OPP08_X": 175,
        "LOCALIZATION_OPP08_Y": 176,
        "LOCALIZATION_OPP09_X": 177,
        "LOCALIZATION_OPP09_Y": 178,
        "LOCALIZATION_OPP10_X": 179,
        "LOCALIZATION_OPP10_Y": 180,
        "LOCALIZATION_OPP11_X": 181,
        "LOCALIZATION_OPP11_Y": 182,
        "DECISION_RBT01_DIST_BALL": 183,
        "DECISION_RBT02_DIST_BALL": 184,
        "DECISION_RBT03_DIST_BALL": 185,
        "DECISION_RBT04_DIST_BALL": 186,
        "VISION_FIRST_GOALPOST": 187,
        "VISION_SECOND_GOALPOST": 188,
        "VISION_THIRD_GOALPOST": 189,
        "VISION_FOURTH_GOALPOST": 190,
        "fVISION_FIELD": 191
    }
#------------------------------------------------------------------------------------------
