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
#define PLANNING_COMMAND *(mem)
#define PLANNING_PARAMETER_VEL *(mem+1)
#define PLANNING_PARAMETER_ANGLE *(mem+2)
#define IMU_STATE *(mem+3)


#define CONTROL_ACTION *(mem+13)
#define CONTROL_HEIGHT_A *(mem+14)
#define CONTROL_HEIGHT_B *(mem+15)
#define CONTROL_HEIGHT_C *(mem+16)
#define DECISION_ACTION_A *(mem+17)
#define DECISION_ACTION_B *(mem+18)
#define DECISION_STATE *(mem+19)
#define DECISION_POSITION_A *(mem+20)
#define DECISION_POSITION_B *(mem+21)
#define DECISION_POSITION_C *(mem+22)
#define DECISION_BALL_POS *(mem+23)
#define DECISION_OPP1_POS *(mem+24)
#define DECISION_OPP2_POS *(mem+25)
#define DECISION_OPP3_POS *(mem+26)
#define COM_ACTION_ROBOT1 *(mem+27)
#define COM_ACTION_ROBOT2 *(mem+28)
#define COM_ACTION_ROBOT3 *(mem+29)
#define COM_STATE_ROBOT1 *(mem+30)
#define COM_STATE_ROBOT2 *(mem+31)
#define COM_STATE_ROBOT3 *(mem+32)
#define COM_POS_ROBOT1 *(mem+33)
#define COM_POS_ROBOT2 *(mem+34)
#define COM_POS_ROBOT3 *(mem+35)
#define COM_POS_BALL_ROBOT1 *(mem+36)
#define COM_POS_BALL_ROBOT2 *(mem+37)
#define COM_POS_BALL_ROBOT3 *(mem+38)
#define COM_POS_OPP_A_ROBOT1 *(mem+39)
#define COM_POS_OPP_A_ROBOT2 *(mem+40)
#define COM_POS_OPP_A_ROBOT3 *(mem+41)
#define COM_POS_OPP_A_ROBOT4 *(mem+42)
#define COM_POS_OPP_B_ROBOT1 *(mem+43)
#define COM_POS_OPP_B_ROBOT2 *(mem+44)
#define COM_POS_OPP_B_ROBOT3 *(mem+45)
#define COM_POS_OPP_B_ROBOT4 *(mem+46)
#define COM_POS_OPP_C_ROBOT1 *(mem+47)
#define COM_POS_OPP_C_ROBOT2 *(mem+48)
#define COM_POS_OPP_C_ROBOT3 *(mem+49)
#define COM_POS_OPP_C_ROBOT4 *(mem+50)
#define COM_REFEREE *(mem+51)
#define LOCALIZATION_X *(mem+52)
#define LOCALIZATION_Y *(mem+53)
#define LOCALIZATION_THETA *(mem+54)
#define VISION_MOTOR1_ANGLE *(mem+55)
#define VISION_MOTOR2_ANGLE *(mem+56)
#define VISION_LOST_BALL *(mem+57)
#define VISION_SEARCH_BALL *(mem+58)
#define DECISION_ACTION_VISION *(mem+59)
#define VISION_MOTOR1_GOAL *(mem+60)
#define VISION_MOTOR2_GOAL *(mem+61)
#define VISION_SEARCH_GOAL *(mem+62)
#define VISION_LOST_GOAL *(mem+63)
#define VISION_STATE *(mem+64)
#define ROBOT_NUMBER *(mem+65)
#define VISION_pos_servo1 *(mem+66)
#define VISION_pos_servo2 *(mem+67)
#define COM_POS_ORIENT_QUALIT_ROBOT_A *(mem+68)
#define COM_POS_DIST_QUALIT_ROBOT_A *(mem+69)
#define COM_POS_ORIENT_QUALIT_ROBOT_B *(mem+70)
#define COM_POS_DIST_QUALIT_ROBOT_B *(mem+71)
#define COM_POS_ORIENT_QUALIT_ROBOT_C *(mem+72)
#define COM_POS_DIST_QUALIT_ROBOT_C *(mem+73)
#define VISION_DELTA_ORIENT *(mem+74)
#define LOCALIZATION_FIND_ROBOT *(mem+75)
#define RECEIVED_ROBOT_SENDING *(mem+76)
#define RECEIVED_QUAL_ORIENT *(mem+77)
#define RECEIVED_QUAL_DIST *(mem+78)
#define RECEIVED_ROBOT_SEEN *(mem+79)
#define CONTROL_MESSAGES *(mem+80)
#define ASKED_QUALIT_DIRECT *(mem+81)
#define ASKED_QUALIT_DISTANCE *(mem+82)
#define ASKED_RELATED_ROBOT *(mem+83)
#define ROBOT_VIEW_ROTATE *(mem+100)

#define VISION_DIST_BALL *(memf+1)
#define VISION_DIST_GOAL *(memf+2)
#define VISION_DIST_OPP1 *(memf+3)
#define VISION_DIST_OPP2 *(memf+4)
#define VISION_DIST_OPP3 *(memf+5)
#define IMU_GYRO_X *(memf+6)
#define IMU_GYRO_Y *(memf+7)
#define IMU_GYRO_Z *(memf+8)
#define IMU_ACCEL_X *(memf+9)
#define IMU_ACCEL_Y *(memf+10)
#define IMU_ACCEL_Z *(memf+11)
#define IMU_COMPASS_X *(memf+12)
#define IMU_COMPASS_Y *(memf+13)
#define IMU_COMPASS_Z *(memf+14)
#define IMU_EULER_X *(memf+15)
#define IMU_EULER_Y *(memf+16)
#define IMU_EULER_Z *(memf+17)
#define IMU_QUAT_X *(memf+18)
#define IMU_QUAT_Y *(memf+19)
#define IMU_QUAT_Z *(memf+20)
#define VISION_AREA_SEGMENT *(memf+21)
#define VISION_ANGLE_BALL *(memf+22)
#define VISION_ANGLE_GOAL *(memf+23)
#define VISION_ANGLE_OPP1 *(memf+24)
#define VISION_ANGLE_OPP2 *(memf+25)
#define VISION_ANGLE_OPP3 *(memf+26)


//----global variables------------------------------------------------
extern int *mem ; //Variável que manipula memória compartilhada
extern float *memf ; //Variável que manipula memória compartilhada

//----Functions prototype---------------------------------------------
int* using_shared_memory(int); //Função que cria e acopla a memória compartilhada


