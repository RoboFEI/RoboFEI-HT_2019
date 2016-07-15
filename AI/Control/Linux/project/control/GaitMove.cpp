/*--------------------------------------------------------------------

******************************************************************************
* @file GaitMove.cpp
* @author Isaac Jesus da Silva - ROBOFEI-HT - FEI 😛
* @version V1.1.0
* @created 15/07/2016
* @Modified 15/07/2016
* @e-mail isaac25silva@yahoo.com.br
* @revisor Isaac Jesus da Silva
* @e-mail isaac25silva@yahoo.com.br
* @brief gait 😛
****************************************************************************
**************************************************************************** 
Arquivo fonte contendo metodos de movimentos do gait
/--------------------------------------------------------------------------*/

#include <iostream>
#include <stdio.h>
#include <unistd.h>
#include "MotionManager.h"
#include "GaitMove.hpp"


//========================================================================
//Construtor--------------------------------------------------------------
GaitMove::GaitMove(int *mem_t, minIni* ini)
{
    //Copiando endereco da memoria compartilhada
    mem = mem_t;

    //Carregando valores do config.ini ---------------
    gait = new ReadConfig("Gait",ini);
    walkfoward = new ReadConfig("Walking Config",ini);
    turnRobot = new ReadConfig("Turn Robot",ini);
    walkslow = new ReadConfig("Walk Slow",ini);
    turnBallR = new ReadConfig("Turn Ball Right",ini);
    turnBallL = new ReadConfig("Turn Ball Left",ini);
    sidleR = new ReadConfig("Sidle Right",ini);
    sidleL = new ReadConfig("Sidle Left",ini);
    //**********************************************

    MotionManager::GetInstance()->LoadINISettings(ini);
    MotionManager::GetInstance()->AddModule((MotionModule*)Walking::GetInstance());
}

//========================================================================
//Execute the gait generation---------------------------------------------
void GaitMove::move_gait(float X_amplitude, float Y_amplitude, float A_amplitude, bool &stop_gait, ReadConfig* configGait, ReadConfig* configP)
{
    write_int(mem, CONTROL_MOVING, 1);
    if(Walking::GetInstance()->IsRunning()==0)
    {
        //Gait_in_place(stop_gait); // Need performes the Gait before performe others moviments
        if(stop_gait == 1)
        {
            while(Walking::GetInstance()->GetCurrentPhase()!=0 && Walking::GetInstance()->IsRunning()!=0)  usleep(8*1000);
            Walking::GetInstance()->Stop();
            Walking::GetInstance()->m_Joint.SetEnableBody(false);
            Action::GetInstance()->m_Joint.SetEnableBody(true);
            MotionManager::GetInstance()->SetEnable(true);
            Action::GetInstance()->Start(9); // Realiza a ação do numero contido no move_number
            while(Action::GetInstance()->IsRunning()) usleep(8*1000); // Aguarda finalizar a ação
            stop_gait = 0;
        }
        std::cout << "Stop com gait" << std::endl;
        configGait->changeParam(Walking::GetInstance()); //volta para os parametros padrao do gait
        Action::GetInstance()->Stop();
        Walking::GetInstance()->m_Joint.SetEnableBody(true);
        Action::GetInstance()->m_Joint.SetEnableBody(false);
        MotionStatus::m_CurrentJoints.SetEnableBodyWithoutHead(true);
        Walking::GetInstance()->X_MOVE_AMPLITUDE = configGait->walk_foward;
        Walking::GetInstance()->Y_MOVE_AMPLITUDE = configGait->sidle;
        Walking::GetInstance()->A_MOVE_AMPLITUDE = configGait->turn_angle;
        Walking::GetInstance()->Start();
        sleep(2);
    }
    configP->changeParam(Walking::GetInstance()); //change the parameters
    Action::GetInstance()->Stop();
    MotionManager::GetInstance()->SetEnable(true);
    Walking::GetInstance()->m_Joint.SetEnableBody(true);
    Action::GetInstance()->m_Joint.SetEnableBody(false);
    MotionStatus::m_CurrentJoints.SetEnableBodyWithoutHead(true);
    Walking::GetInstance()->X_MOVE_AMPLITUDE = X_amplitude;
    Walking::GetInstance()->Y_MOVE_AMPLITUDE = Y_amplitude;
    Walking::GetInstance()->A_MOVE_AMPLITUDE = A_amplitude;
    Walking::GetInstance()->Start();
}

//========================================================================
//Do the gait staing int the place----------------------------------------
void GaitMove::Gait_in_place(bool &stop_gait, bool same_moviment)
{
    if(same_moviment == false) //Imprime na tela se o movimento nao foi repetido
        std::cout<<" | Stop com gait"<<std::endl;
    move_gait(gait->walk_foward, gait->sidle, gait->turn_angle, stop_gait, gait, gait);
}

//========================================================================
//Execute the gait generation---------------------------------------------
void GaitMove::walk_foward_slow(bool &stop_gait, bool max_speed, bool same_moviment)
{
    if(same_moviment == false)
        std::cout<<" | Andar lento para frente"<<std::endl;
    if(float(read_int(mem, DECISION_ACTION_B))<walkslow->walk_foward && max_speed==false)
        move_gait(float(read_int(mem, DECISION_ACTION_B)), walkslow->sidle, walkslow->turn_angle, stop_gait, gait, walkslow);
    else
        move_gait(walkslow->walk_foward, walkslow->sidle, walkslow->turn_angle, stop_gait, gait, walkslow);
}


//========================================================================
//O Robo para de executar o gait--------------------------------------------
void GaitMove::robot_stop(bool &stop_gait)
{
    //write_int(mem, CONTROL_MOVING, 1);
    std::cout<<" | Nada a fazer"<<std::endl;
    if (Walking::GetInstance()->IsRunning()!=0)
    {
        move_gait(gait->walk_foward, gait->sidle, gait->turn_angle, stop_gait, gait, gait);
        usleep(500000);
    }
    while(Walking::GetInstance()->GetCurrentPhase()!=0 && Walking::GetInstance()->IsRunning()!=0)  usleep(8*1000);
    Walking::GetInstance()->Stop();
    Walking::GetInstance()->m_Joint.SetEnableBody(false);
    Action::GetInstance()->m_Joint.SetEnableBody(true);
    MotionManager::GetInstance()->SetEnable(true);
    usleep(500000); //Aguarda 0.5 segundos para estabilizar o robo
    Action::GetInstance()->Start(1); // Realiza a ação do numero contido no move_number
    while(Action::GetInstance()->IsRunning()) usleep(8*1000);
    stop_gait = 1;
    write_int(mem, CONTROL_MOVING, 0);
}

//========================================================================
//Andar rapido para frente------------------------------------------------
void GaitMove::walk_foward_fast(bool &stop_gait, bool same_moviment)
{
    if(same_moviment == false)
        std::cout<<" | Andar para frente"<<std::endl;
    move_gait(walkfoward->walk_foward, walkfoward->sidle, walkfoward->turn_angle, stop_gait, gait, walkfoward);
}


//========================================================================
//O robo vira para a direita----------------------------------------------
void GaitMove::turn_right(bool &stop_gait, bool max_angle, bool same_moviment)
{
    if(same_moviment == false)
        std::cout << " | Virar a direita" << std::endl;
    if(float(read_int(mem, DECISION_ACTION_B))<turnRobot->turn_angle && max_angle==false)
        move_gait(turnRobot->walk_foward, turnRobot->sidle, -float(read_int(mem, DECISION_ACTION_B)), stop_gait, gait, turnRobot);
    else
        move_gait(turnRobot->walk_foward, turnRobot->sidle, -turnRobot->turn_angle, stop_gait, gait, turnRobot);
}

//========================================================================
//O robo vira para a esquerda---------------------------------------------
void GaitMove::turn_left(bool &stop_gait, bool max_angle, bool same_moviment)
{
    if(same_moviment == false)
        std::cout<<" | Virar a esquerda"<<std::endl;
    if(float(read_int(mem, DECISION_ACTION_B))<turnRobot->turn_angle && max_angle==false)
        move_gait(turnRobot->walk_foward, turnRobot->sidle, -float(read_int(mem, DECISION_ACTION_B)), stop_gait, gait, turnRobot);
    else
        move_gait(turnRobot->walk_foward, turnRobot->sidle, turnRobot->turn_angle, stop_gait, gait, turnRobot);
}

//========================================================================
//The robot sidle to right------------------------------------------------
void GaitMove::sidle_right(bool &stop_gait, bool same_moviment)
{
    if(same_moviment == false)
        std::cout<<" | Andar de Lado direita"<<std::endl;
    move_gait(sidleR->walk_foward, -sidleR->sidle, sidleR->turn_angle, stop_gait, gait, sidleR);
}

//========================================================================
//The robot sidle to left-------------------------------------------------
void GaitMove::sidle_left(bool &stop_gait, bool same_moviment)
{
    if(same_moviment == false)
        std::cout<<" | Andar de Lado esquerda"<<std::endl;
    move_gait(sidleL->walk_foward, sidleL->sidle, sidleL->turn_angle, stop_gait, gait, sidleL);
}

//========================================================================
//The robot sidle to right-------------------------------------------------
void GaitMove::turn_around_ball_right(bool &stop_gait, bool same_moviment)
{
    if(same_moviment == false)
        std::cout<<" | Girar em torno da bola para direita"<<std::endl;
    move_gait(turnBallR->walk_foward, -turnBallR->sidle, -turnBallR->turn_angle, stop_gait, gait, turnBallR);
}

//========================================================================
//The robot sidle to left-------------------------------------------------
void GaitMove::turn_around_ball_left(bool &stop_gait, bool same_moviment)
{
    if(same_moviment == false)
        std::cout<<" | Girar em torno da bola para esquerda"<<std::endl;
    move_gait(turnBallL->walk_foward, turnBallL->sidle, turnBallL->turn_angle, stop_gait, gait, turnBallL);
}

//========================================================================
//gait backward fast--------------------------------------------------
void GaitMove::walk_backward_fast(bool &stop_gait, bool same_moviment)
{
    if(same_moviment == false)
        std::cout<<" | Andar rapido para traz"<<std::endl;
    move_gait(-walkfoward->walk_foward, walkfoward->sidle, walkfoward->turn_angle, stop_gait, gait, walkfoward);
}

//========================================================================
//gait backward slow------------------------------------------------------
void GaitMove::walk_backward_slow(bool &stop_gait, bool max_speed, bool same_moviment)
{
    if(same_moviment == false)
        std::cout<<" | Andar lento para traz"<<std::endl;
    if(float(read_int(mem, DECISION_ACTION_B))<walkslow->walk_foward && max_speed==false)
        move_gait(-float(read_int(mem, DECISION_ACTION_B)), walkslow->sidle, walkslow->turn_angle, stop_gait, gait, walkslow);
    else
        move_gait(-walkslow->walk_foward, walkslow->sidle, walkslow->turn_angle, stop_gait, gait, walkslow);
}




