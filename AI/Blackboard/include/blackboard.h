/*--------------------------------------------------------------------

******************************************************************************
* @file blackboard.h
* @author Isaac Jesus da Silva - ROBOFEI-HT - FEI
* @version V0.0.0
* @created 07/04/2014
* @Modified 15/05/2014
* @e-mail isaac25silva@yahoo.com.br
* @brief Main header black board
****************************************************************************

Arquivo de cabeçalho contendo as funções e definições do black board

/--------------------------------------------------------------------*/

//---- Definições da memória compartilhada------------------------------
#define PLANNING_COMMAND 0
#define PLANNING_PARAMETER_VEL 1
#define PLANNING_PARAMETER_ANGLE 2
#define IMU_STATE 3


#define CONTROL_ACTION 13
#define CONTROL_HEIGHT_A 14
#define CONTROL_HEIGHT_B 15
#define CONTROL_HEIGHT_C 16
#define DECISION_ACTION_A 17
#define DECISION_ACTION_B 18
#define DECISION_STATE 19
#define DECISION_POSITION_A 20
#define DECISION_POSITION_B 21
#define DECISION_POSITION_C 22
#define DECISION_BALL_POS 23
#define DECISION_OPP1_POS 24
#define DECISION_OPP2_POS 25
#define DECISION_OPP3_POS 26
#define COM_ACTION_ROBOT1 27
#define COM_ACTION_ROBOT2 28
#define COM_ACTION_ROBOT3 29
#define COM_STATE_ROBOT1 30
#define COM_STATE_ROBOT2 31
#define COM_STATE_ROBOT3 32
#define COM_POS_ROBOT1 33
#define COM_POS_ROBOT2 34
#define COM_POS_ROBOT3 35
#define COM_POS_BALL_ROBOT1 36
#define COM_POS_BALL_ROBOT2 37
#define COM_POS_BALL_ROBOT3 38
#define COM_POS_OPP_A_ROBOT1 39
#define COM_POS_OPP_A_ROBOT2 40
#define COM_POS_OPP_A_ROBOT3 41
#define COM_POS_OPP_A_ROBOT4 42
#define COM_POS_OPP_B_ROBOT1 43
#define COM_POS_OPP_B_ROBOT2 44
#define COM_POS_OPP_B_ROBOT3 45
#define COM_POS_OPP_B_ROBOT4 46
#define COM_POS_OPP_C_ROBOT1 47
#define COM_POS_OPP_C_ROBOT2 48
#define COM_POS_OPP_C_ROBOT3 49
#define COM_POS_OPP_C_ROBOT4 50
#define COM_REFEREE 51
#define LOCALIZATION_X 52
#define LOCALIZATION_Y 53
#define LOCALIZATION_THETA 54
#define VISION_MOTOR1_ANGLE 55
#define VISION_MOTOR2_ANGLE 56
#define VISION_LOST_BALL 57
#define VISION_SEARCH_BALL 58
#define DECISION_ACTION_VISION 59
#define VISION_MOTOR1_GOAL 60
#define VISION_MOTOR2_GOAL 61
#define VISION_SEARCH_GOAL 62
#define VISION_LOST_GOAL 63
#define VISION_STATE 64
#define ROBOT_NUMBER 65
#define VISION_pos_servo1 66
#define VISION_pos_servo2 67
#define COM_POS_ORIENT_QUALIT_ROBOT_A 68
#define COM_POS_DIST_QUALIT_ROBOT_A 69
#define COM_POS_ORIENT_QUALIT_ROBOT_B 70
#define COM_POS_DIST_QUALIT_ROBOT_B 71
#define COM_POS_ORIENT_QUALIT_ROBOT_C 72
#define COM_POS_DIST_QUALIT_ROBOT_C 73
#define VISION_DELTA_ORIENT 74
#define LOCALIZATION_FIND_ROBOT 75
#define RECEIVED_ROBOT_SENDING 76
#define RECEIVED_QUAL_ORIENT 77
#define RECEIVED_QUAL_DIST 78
#define RECEIVED_ROBOT_SEEN 79
#define CONTROL_MESSAGES 80
#define ASKED_QUALIT_DIRECT 81
#define ASKED_QUALIT_DISTANCE 82
#define ASKED_RELATED_ROBOT 83
#define ROBOT_VIEW_ROTATE 100

#define VISION_DIST_BALL 1
#define VISION_DIST_GOAL 2
#define VISION_DIST_OPP1 3
#define VISION_DIST_OPP2 4
#define VISION_DIST_OPP3 5
#define IMU_GYRO_X 6
#define IMU_GYRO_Y 7
#define IMU_GYRO_Z 8
#define IMU_ACCEL_X 9
#define IMU_ACCEL_Y 10
#define IMU_ACCEL_Z 11
#define IMU_COMPASS_X 12
#define IMU_COMPASS_Y 13
#define IMU_COMPASS_Z 14
#define IMU_EULER_X 15
#define IMU_EULER_Y 16
#define IMU_EULER_Z 17
#define IMU_QUAT_X 18
#define IMU_QUAT_Y 19
#define IMU_QUAT_Z 20
#define VISION_AREA_SEGMENT 21
#define VISION_ANGLE_BALL 22
#define VISION_ANGLE_GOAL 23
#define VISION_ANGLE_OPP1 24
#define VISION_ANGLE_OPP2 25
#define VISION_ANGLE_OPP3 26


//----global variables------------------------------------------------
extern int *mem ; //Variável que manipula memória compartilhada
extern float *memf ; //Variável que manipula memória compartilhada

//----Functions prototype---------------------------------------------
int* using_shared_memory(int); //Função que cria e acopla a memória compartilhada

void write_int(int* , int, int);

void write_float(int*, int, float);

int read_int(int*, int);

float read_float(int*, int);

