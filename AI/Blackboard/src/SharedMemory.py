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
        "IMU_GYRO_X": 0
        "IMU_GYRO_Y": 1
        "IMU_GYRO_Z": 2
        "IMU_ACCEL_X": 3
        "IMU_ACCEL_Y": 4
        "IMU_ACCEL_Z": 5
        "IMU_COMPASS_X": 6
        "IMU_COMPASS_Y": 7
        "IMU_COMPASS_Z": 8
        "IMU_EULER_X": 9
        "IMU_EULER_Y": 10
        "IMU_EULER_Z": 11
        "IMU_QUAT_X": 12
        "IMU_QUAT_Y": 13
        "IMU_QUAT_Z": 14
        "VISION_AREA_SEGMENT": 15
        "VISION_BALL_X": 16
        "VISION_BALL_Y": 17
        "VISION_BALL_TAG": 18
        "VISION_LAND_X": 19
        "VISION_LAND_Y": 20
        "VISION_LAND_TAG": 21
        "VISION_RB01_TAG": 22
        "VISION_RB01_X": 23
        "VISION_RB01_Y": 24
        "VISION_RB01_TIME": 25
        "VISION_RB02_TAG": 26
        "VISION_RB02_X": 27
        "VISION_RB02_Y": 28
        "VISION_RB02_TIME": 29
        "VISION_RB03_TAG": 30
        "VISION_RB03_X": 31
        "VISION_RB03_Y": 32
        "VISION_RB03_TIME": 33
        "VISION_RB04_TAG": 34
        "VISION_RB04_X": 35
        "VISION_RB04_Y": 36
        "VISION_RB04_TIME": 37
        "VISION_RB05_TAG": 38
        "VISION_RB05_X": 39
        "VISION_RB05_Y": 40
        "VISION_RB05_TIME": 41
        "VISION_RB06_TAG": 42
        "VISION_RB06_X": 43
        "VISION_RB06_Y": 44
        "VISION_RB06_TIME": 45
        "VISION_RB07_TAG": 46
        "VISION_RB07_X": 47
        "VISION_RB07_Y": 48
        "VISION_RB07_TIME": 49
        "VISION_RB08_TAG": 50
        "VISION_RB08_X": 51
        "VISION_RB08_Y": 52
        "VISION_RB08_TIME": 53
        "VISION_RB09_TAG": 54
        "VISION_RB09_X": 55
        "VISION_RB09_Y": 56
        "VISION_RB09_TIME": 57
        "VISION_RB10_TAG": 58
        "VISION_RB10_X": 59
        "VISION_RB10_Y": 60
        "VISION_RB10_TIME": 61
        "VISION_RB11_TAG": 62
        "VISION_RB11_X": 63
        "VISION_RB11_Y": 64
        "VISION_RB11_TIME": 65
        "VISION_RB12_TAG": 66
        "VISION_RB12_X": 67
        "VISION_RB12_Y": 68
        "VISION_RB12_TIME": 69
        "VISION_RB13_TAG": 70
        "VISION_RB13_X": 71
        "VISION_RB13_Y": 72
        "VISION_RB13_TIME": 73
        "VISION_RB14_TAG": 74
        "VISION_RB14_X": 75
        "VISION_RB14_Y": 76
        "VISION_RB14_TIME": 77
        "VISION_RB15_TAG": 78
        "VISION_RB15_X": 79
        "VISION_RB15_Y": 80
        "VISION_RB15_TIME": 81
        "VISION_RB16_TAG": 82
        "VISION_RB16_X": 83
        "VISION_RB16_Y": 84
        "VISION_RB16_TIME": 85
        "VISION_RB17_TAG": 86
        "VISION_RB17_X": 87
        "VISION_RB17_Y": 88
        "VISION_RB17_TIME": 89
        "VISION_RB18_TAG": 90
        "VISION_RB18_X": 91
        "VISION_RB18_Y": 92
        "VISION_RB18_TIME": 93
        "VISION_RB19_TAG": 94
        "VISION_RB19_X": 95
        "VISION_RB19_Y": 96
        "VISION_RB19_TIME": 97
        "VISION_RB20_TAG": 98
        "VISION_RB20_X": 99
        "VISION_RB20_Y": 100
        "VISION_RB20_TIME": 101
        "VISION_RB21_TAG": 102
        "VISION_RB21_X": 103
        "VISION_RB21_Y": 104
        "VISION_RB21_TIME": 105
        "VISION_RB22_TAG": 106
        "VISION_RB22_X": 107
        "VISION_RB22_Y": 108
        "VISION_RB22_TIME": 109
        "VISUAL_MEMORY_AL_01": 110
        "VISUAL_MEMORY_AL_02": 111
        "VISUAL_MEMORY_AL_03": 112
        "VISUAL_MEMORY_AL_04": 113
        "VISUAL_MEMORY_AL_05": 114
        "VISUAL_MEMORY_AL_06": 115
        "VISUAL_MEMORY_AL_07": 116
        "VISUAL_MEMORY_AL_08": 117
        "VISUAL_MEMORY_AL_09": 118
        "VISUAL_MEMORY_AL_10": 119
        "VISUAL_MEMORY_AL_11": 120
        "VISUAL_MEMORY_OP_01": 121
        "VISUAL_MEMORY_OP_02": 122
        "VISUAL_MEMORY_OP_03": 123
        "VISUAL_MEMORY_OP_04": 124
        "VISUAL_MEMORY_OP_05": 125
        "VISUAL_MEMORY_OP_06": 126
        "VISUAL_MEMORY_OP_07": 127
        "VISUAL_MEMORY_OP_08": 128
        "VISUAL_MEMORY_OP_09": 129
        "VISUAL_MEMORY_OP_10": 130
        "VISUAL_MEMORY_OP_11": 131
        "VISION_TILT_DEG": 132
        "VISION_PAN_DEG": 133
        "CBR_COORDINATOR": 134
        "CBR_RUN": 135
        "LOCALIZATION_BALL_X": 136
        "LOCALIZATION_BALL_Y": 137
        "LOCALIZATION_RBT01_X": 138
        "LOCALIZATION_RBT01_Y": 139
        "LOCALIZATION_RBT02_X": 140
        "LOCALIZATION_RBT02_Y": 141
        "LOCALIZATION_RBT03_X": 142
        "LOCALIZATION_RBT03_Y": 143
        "LOCALIZATION_RBT04_X": 144
        "LOCALIZATION_RBT04_Y": 145
        "LOCALIZATION_RBT05_X": 146
        "LOCALIZATION_RBT05_Y": 147
        "LOCALIZATION_RBT06_X": 148
        "LOCALIZATION_RBT06_Y": 149
        "LOCALIZATION_RBT07_X": 150
        "LOCALIZATION_RBT07_Y": 151
        "LOCALIZATION_RBT08_X": 152
        "LOCALIZATION_RBT08_Y": 153
        "LOCALIZATION_RBT09_X": 154
        "LOCALIZATION_RBT09_Y": 155
        "LOCALIZATION_RBT10_X": 156
        "LOCALIZATION_RBT10_Y": 157
        "LOCALIZATION_RBT11_X": 158
        "LOCALIZATION_RBT11_Y": 159
        "LOCALIZATION_OPP01_X": 160
        "LOCALIZATION_OPP01_Y": 161
        "LOCALIZATION_OPP02_X": 162
        "LOCALIZATION_OPP02_Y": 163
        "LOCALIZATION_OPP03_X": 164
        "LOCALIZATION_OPP03_Y": 165
        "LOCALIZATION_OPP04_X": 166
        "LOCALIZATION_OPP04_Y": 167
        "LOCALIZATION_OPP05_X": 168
        "LOCALIZATION_OPP05_Y": 169
        "LOCALIZATION_OPP06_X": 170
        "LOCALIZATION_OPP06_Y": 171
        "LOCALIZATION_OPP07_X": 172
        "LOCALIZATION_OPP07_Y": 173
        "LOCALIZATION_OPP08_X": 174
        "LOCALIZATION_OPP08_Y": 175
        "LOCALIZATION_OPP09_X": 176
        "LOCALIZATION_OPP09_Y": 177
        "LOCALIZATION_OPP10_X": 178
        "LOCALIZATION_OPP10_Y": 179
        "LOCALIZATION_OPP11_X": 180
        "LOCALIZATION_OPP11_Y": 181
        "DECISION_RBT01_DIST_BALL": 182
        "DECISION_RBT02_DIST_BALL": 183
        "DECISION_RBT03_DIST_BALL": 184
        "DECISION_RBT04_DIST_BALL": 185
        "VISION_FIRST_GOALPOST": 186
        "VISION_SECOND_GOALPOST": 187
        "VISION_THIRD_GOALPOST": 188
        "VISION_FOURTH_GOALPOST": 189
        "fVISION_FIELD": 190
    }
#------------------------------------------------------------------------------------------
