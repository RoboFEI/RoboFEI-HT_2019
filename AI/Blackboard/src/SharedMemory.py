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
    'IMU_GYRO_X': 1,
    'IMU_GYRO_Y': 2,
    'IMU_GYRO_Z': 3,
    'IMU_ACCEL_X': 4,
    'IMU_ACCEL_Y': 5,
    'IMU_ACCEL_Z': 6,
    'IMU_COMPASS_X': 7,
    'IMU_COMPASS_Y': 8,
    'IMU_COMPASS_Z': 9,
    'IMU_EULER_X': 10,
    'IMU_EULER_Y': 11,
    'IMU_EULER_Z': 12,
    'IMU_QUAT_X': 13,
    'IMU_QUAT_Y': 14,
    'IMU_QUAT_Z': 15,
    'VISION_AREA_SEGMENT': 16,
    'VISION_BALL_X': 17,
    'VISION_BALL_Y': 18,
    'VISION_BALL_TAG': 19,
    'VISION_BALL_TIME': 20,
    'VISION_LAND_X': 21,
    'VISION_LAND_Y': 22,
    'VISION_LAND_TAG': 23,
    'VISION_LAND_TIME': 24,
    'VISION_RB01_TAG': 25,
    'VISION_RB01_X': 26,
    'VISION_RB01_Y': 27,
    'VISION_RB01_TIME': 28,
    'VISION_RB02_TAG': 29,
    'VISION_RB02_X': 30,
    'VISION_RB02_Y': 31,
    'VISION_RB02_TIME': 32,
    'VISION_RB03_TAG': 33,
    'VISION_RB03_X': 34,
    'VISION_RB03_Y': 35,
    'VISION_RB03_TIME': 36,
    'VISION_RB04_TAG': 37,
    'VISION_RB04_X': 38,
    'VISION_RB04_Y': 39,
    'VISION_RB04_TIME': 40,
    'VISION_RB05_TAG': 41,
    'VISION_RB05_X': 42,
    'VISION_RB05_Y': 43,
    'VISION_RB05_TIME': 44,
    'VISION_RB06_TAG': 45,
    'VISION_RB06_X': 46,
    'VISION_RB06_Y': 47,
    'VISION_RB06_TIME': 48,
    'VISION_RB07_TAG': 49,
    'VISION_RB07_X': 50,
    'VISION_RB07_Y': 51,
    'VISION_RB07_TIME': 52,
    'VISION_RB08_TAG': 53,
    'VISION_RB08_X': 54,
    'VISION_RB08_Y': 55,
    'VISION_RB08_TIME': 56,
    'VISION_RB09_TAG': 57,
    'VISION_RB09_X': 58,
    'VISION_RB09_Y': 59,
    'VISION_RB09_TIME': 60,
    'VISION_RB10_TAG': 61,
    'VISION_RB10_X': 62,
    'VISION_RB10_Y': 63,
    'VISION_RB10_TIME': 64,
    'VISION_RB11_TAG': 65,
    'VISION_RB11_X': 66,
    'VISION_RB11_Y': 67,
    'VISION_RB11_TIME': 68,
    'VISION_RB12_TAG': 69,
    'VISION_RB12_X': 70,
    'VISION_RB12_Y': 71,
    'VISION_RB12_TIME': 72,
    'VISION_RB13_TAG': 73,
    'VISION_RB13_X': 74,
    'VISION_RB13_Y': 75,
    'VISION_RB13_TIME': 76,
    'VISION_RB14_TAG': 77,
    'VISION_RB14_X': 78,
    'VISION_RB14_Y': 79,
    'VISION_RB14_TIME': 80,
    'VISION_RB15_TAG': 81,
    'VISION_RB15_X': 82,
    'VISION_RB15_Y': 83,
    'VISION_RB15_TIME': 84,
    'VISION_RB16_TAG': 85,
    'VISION_RB16_X': 86,
    'VISION_RB16_Y': 87,
    'VISION_RB16_TIME': 88,
    'VISION_RB17_TAG': 89,
    'VISION_RB17_X': 90,
    'VISION_RB17_Y': 91,
    'VISION_RB17_TIME': 92,
    'VISION_RB18_TAG': 93,
    'VISION_RB18_X': 94,
    'VISION_RB18_Y': 95,
    'VISION_RB18_TIME': 96,
    'VISION_RB19_TAG': 97,
    'VISION_RB19_X': 98,
    'VISION_RB19_Y': 99,
    'VISION_RB19_TIME': 100,
    'VISION_RB20_TAG': 101,
    'VISION_RB20_X': 102,
    'VISION_RB20_Y': 103,
    'VISION_RB20_TIME': 104,
    'VISION_RB21_TAG': 105,
    'VISION_RB21_X': 106,
    'VISION_RB21_Y': 107,
    'VISION_RB21_TIME': 108,
    'VISION_RB22_TAG': 109,
    'VISION_RB22_X': 110,
    'VISION_RB22_Y': 111,
    'VISION_RB22_TIME': 112,
    'VISION_TILT_DEG': 113,
    'VISION_PAN_DEG': 114,
    'CBR_COORDINATOR': 115,
    'CBR_RUN': 116,
    'LOCALIZATION_BALL_X': 117,
    'LOCALIZATION_BALL_Y': 118,
    'LOCALIZATION_RBT01_X': 119,
    'LOCALIZATION_RBT01_Y': 120,
    'LOCALIZATION_RBT02_X': 121,
    'LOCALIZATION_RBT02_Y': 122,
    'LOCALIZATION_RBT03_X': 123,
    'LOCALIZATION_RBT03_Y': 124,
    'LOCALIZATION_RBT04_X': 125,
    'LOCALIZATION_RBT04_Y': 126,
    'LOCALIZATION_RBT05_X': 127,
    'LOCALIZATION_RBT05_Y': 128,
    'LOCALIZATION_RBT06_X': 129,
    'LOCALIZATION_RBT06_Y': 130,
    'LOCALIZATION_RBT07_X': 131,
    'LOCALIZATION_RBT07_Y': 132,
    'LOCALIZATION_RBT08_X': 133,
    'LOCALIZATION_RBT08_Y': 134,
    'LOCALIZATION_RBT09_X': 135,
    'LOCALIZATION_RBT09_Y': 136,
    'LOCALIZATION_RBT10_X': 137,
    'LOCALIZATION_RBT10_Y': 138,
    'LOCALIZATION_RBT11_X': 139,
    'LOCALIZATION_RBT11_Y': 140,
    'LOCALIZATION_OPP01_X': 141,
    'LOCALIZATION_OPP01_Y': 142,
    'LOCALIZATION_OPP02_X': 143,
    'LOCALIZATION_OPP02_Y': 144,
    'LOCALIZATION_OPP03_X': 145,
    'LOCALIZATION_OPP03_Y': 146,
    'LOCALIZATION_OPP04_X': 147,
    'LOCALIZATION_OPP04_Y': 148,
    'LOCALIZATION_OPP05_X': 149,
    'LOCALIZATION_OPP05_Y': 150,
    'LOCALIZATION_OPP06_X': 151,
    'LOCALIZATION_OPP06_Y': 152,
    'LOCALIZATION_OPP07_X': 153,
    'LOCALIZATION_OPP07_Y': 154,
    'LOCALIZATION_OPP08_X': 155,
    'LOCALIZATION_OPP08_Y': 156,
    'LOCALIZATION_OPP09_X': 157,
    'LOCALIZATION_OPP09_Y': 158,
    'LOCALIZATION_OPP10_X': 159,
    'LOCALIZATION_OPP10_Y': 160,
    'LOCALIZATION_OPP11_X': 161,
    'LOCALIZATION_OPP11_Y': 162,
    'DECISION_RBT01_DIST_BALL': 163,
    'DECISION_RBT02_DIST_BALL': 164,
    'DECISION_RBT03_DIST_BALL': 165,
    'DECISION_RBT04_DIST_BALL': 166,
    'VISION_FIRST_GOALPOST': 167,
    'VISION_SECOND_GOALPOST': 168,
    'VISION_THIRD_GOALPOST': 169,
    'VISION_FOURTH_GOALPOST': 170,
    'fVISION_FIELD': 171,
    }
#------------------------------------------------------------------------------------------
