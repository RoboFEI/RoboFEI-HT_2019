/*--------------------------------------------------------------------

******************************************************************************
* @file control.cpp
* @author Isaac Jesus da Silva - ROBOFEI-HT - FEI 😛
* @version V2.1.0
* @created 20/01/2015
* @Modified 01/05/2016
* @e-mail isaac25silva@yahoo.com.br
* @brief control 😛
****************************************************************************
**************************************************************************** 
Arquivo fonte contendo o programa que controla os servos do corpo do robô
---------------------------------------------------------------------------*/

#include <unistd.h>
#include <string.h>
#include <libgen.h>
#include <iostream>
#include <stdio.h>
#include <termios.h>
#include <fcntl.h>
#include <stdlib.h>
#include <cstdlib>

//#include <stdio.h>
//#include <errno.h>
//#include <sys/ipc.h>
//#include <sys/shm.h>
#include <signal.h>

#include "minIni.h"
#include <string>

//#include "Action.h"
//#include "Walking.h"
#include "MX28.h"
#include "MotionManager.h"
#include "LinuxMotionTimer.h"
#include "LinuxCM730.h"
//#include "LinuxActionScript.h"
#include <blackboard.h>
#include <boost/program_options.hpp> //tratamento de argumentos linha de comando
#include "ActionMove.hpp"
#include "GaitMove.hpp"

#ifdef MX28_1024
#define MOTION_FILE_PATH    "../../Control/Data/motion_1024.bin"
#else
#define MOTION_FILE_PATH    "../../Control/Data/motion_4096.bin"
#endif

#define INI_FILE_PATH       "../../Control/Data/config.ini"

#define DEBUG_PRINT true

#define LIMITE_TEMP 80    // Define a temperatura maxima dos motores

using namespace Robot;
using namespace std;

int kbhit(); //Function kbhit.cpp

int check_servo(CM730 *cm730, int idServo, bool &stop_gait);

int Initialize_servo();

void change_current_dir()
{
    char exepath[1024] = {0};
    if(readlink("/proc/self/exe", exepath, sizeof(exepath)) != -1)
        chdir(dirname(exepath));
}

void sighandler(int sig)
{
    cout<< "\nProgram being closed!" << endl;
    exit(1); 
}

char string1[50]; //String

int main(int argc, char **argv)
{

    change_current_dir();

    minIni* ini;
    ini = new minIni((char *)INI_FILE_PATH);

    //Detecta o Ctrl+C-----------
    signal(SIGABRT, &sighandler);
    signal(SIGTERM, &sighandler);
    signal(SIGINT, &sighandler);
    //---------------------------

      //Acopla ou cria a memoria compartilhada
    int *mem = using_shared_memory(ini->getd("Communication","no_player_robofei",-1024) * 100); //0 for real robot

    bool stop_gait = true;
    char *Servoport;
    sprintf(string1,"echo fei 123456| sudo -S renice -20 -p %d", getpid()); // prioridade maxima do codigo
    system(string1);//prioridade
    int value;
    int idServo;
    bool flag_stop = 0;
    bool same_moviment = false;
    unsigned int buffer = 10000;
    unsigned int count_read=0;
    unsigned int step_time=20; // Determina a frequencia de leitura do blackboard

    printf( "\n===== ROBOFEI-HT Control Process =====\n\n");

    //-------------para entrada de argumentos-----------------------------------
    namespace po=boost::program_options;

    po::options_description desc("options");
    desc.add_options()
    ("help", "produce help message")
    ("k", "Inicia com o controle do robô pelo teclado")
    ("v", "Verifica a tensao nos servos do corpo")
    ("g", "Inicia o controle para usar com a interface grafica")
    ;
  
    po::variables_map variables;
    po::store(po::parse_command_line(argc, argv, desc), variables);
    po::notify(variables); 
    //--------------------------------------------------------------------------

    //////////////////// Framework Initialize ////////////////////////////
    // ---- Open USBDynamixel -----------------------------------------------{
    if(Initialize_servo()==1) // chama a função que encontra o endereço de comunicação com o servo
        return 0;
    LinuxCM730 linux_cm730(string1);
    CM730 cm730(&linux_cm730);
    if(MotionManager::GetInstance()->Initialize(&cm730) == false)
    {
        printf("Fail to initialize Motion Manager!\n");
        return 0;
    }
    //================================================================================== 

    //======================== check temperature =======================================     
    if (variables.count("v")) //verifica se foi chamado o argumento de controle pelo teclado
    {
        if(cm730.ReadByte(12, 42, &value, 0) != CM730::SUCCESS)
            std::cout<<"Erro na leitura da tensao"<<std::endl;
        std::cout<<"Tensao = "<<float(value)/10<<"V"<<std::endl;
        return 0;
    }
    //================================================================================== 

//    MotionManager::GetInstance()->LoadINISettings(ini);

    //Criando objeto da classe dos movimento de acoes----------------------------
    ActionMove actionMove(mem, (char *)MOTION_FILE_PATH);
    //**************************************************************************

    //Criando objeto da classe dos movimentos de caminhada----------------------
    GaitMove gaitMove(mem, ini);
    //**************************************************************************

//    MotionManager::GetInstance()->LoadINISettings(ini);
//    Walking::GetInstance()->LoadINISettings(ini); 
//    MotionManager::GetInstance()->AddModule((MotionModule*)Action::GetInstance());
//    MotionManager::GetInstance()->AddModule((MotionModule*)Walking::GetInstance());
    LinuxMotionTimer linuxMotionTimer;
    linuxMotionTimer.Initialize(MotionManager::GetInstance());
    linuxMotionTimer.Start();
    /////////////////////////////////////////////////////////////////////

    actionMove.poseStandup(stop_gait); /* Init(stand up) pose */

    //====== Reset the IMU ==========
    sleep(2);
    write_int(mem, IMU_RESET, 1);
    sleep(1);
    int k=0;

    if (!variables.count("k")) //verifica se foi chamado o argumento de controle pelo teclado
    {
        //====== Reset the IMU ==========
        while(read_float(mem, IMU_EULER_Z) > 0.0005 || read_float(mem, IMU_EULER_Z) < -0.0005)
        {
            sleep(2);
            write_int(mem, IMU_RESET, 1);
            cout<<"Reseting IMU"<<endl;
            sleep(1);
            if (k>4)
            {
                cout<<"Error: reset IMU failed"<<endl;
                break;
            }
            k++;
        }
    }
    //===============================

    //***********************************************************************************************
    if (variables.count("k")) //verifica se foi chamado o argumento de controle pelo teclado
    {
    //-------------iniciando o modulo de andar pelo teclado------------------------------------------

        while(1)
        {
            int key = kbhit();
            usleep(4*1000);

            switch(key)
            {
                case 97: //a
                    actionMove.standupFront(stop_gait);
                break;

                case 98: //b
                    actionMove.standupBack(stop_gait);
                break;
                
                case 112: //p
                    actionMove.kick_right_strong(&cm730, stop_gait);
                break;

                case 108: //l
                    actionMove.kick_left_strong(&cm730, stop_gait);
                break;

                case 99: //c
                    actionMove.kick_right_weak(stop_gait);
                break;

                case 103: //g
                    actionMove.kick_left_weak(stop_gait);
                break;

                case 102: //f
                    gaitMove.walk_foward_fast(stop_gait, same_moviment);
                break;

                case 100: //d
                    gaitMove.turn_right(stop_gait, true, same_moviment);
                break;

                case 105: //i
                    actionMove.pass_left(&cm730, stop_gait);
                break;

                case 101: //e
                    gaitMove.turn_left(stop_gait, true, same_moviment);
                break;

                case 106: //j
                    actionMove.pass_right(&cm730, stop_gait);
                break;

                case 109: //m
                    gaitMove.sidle_left(stop_gait, same_moviment);
                break;

                case 110: //n
                    gaitMove.sidle_right(stop_gait, same_moviment);
                break;

                case 111: //o
                    gaitMove.turn_around_ball_left(stop_gait, same_moviment);
                break;

                case 113: //q
                    gaitMove.turn_around_ball_right(stop_gait, same_moviment);
                break;

                case 107: //k
                    gaitMove.walk_foward_slow(stop_gait, true, same_moviment);
                break;

                case 114: //r
                    gaitMove.walk_backward_slow(stop_gait, true, same_moviment);
                break;

                case 118: //v
                    gaitMove.walk_backward_fast(stop_gait, same_moviment);
                break;

                case 115: //s
                    gaitMove.Gait_in_place(stop_gait, same_moviment);
                break;

                case 116: //t
                    gaitMove.robot_stop(stop_gait);
                break;
                
                case 117: //u
                    actionMove.goalkeeper(stop_gait);
                break;

                case 104: //h
                    actionMove.greetings(stop_gait);
                break;

                case 122: //z
                    actionMove.goodBye(stop_gait);
                 break;

                case 27: //ESC (stop)
                    cout << " | Exit process" << endl;
                    return 0;
                break;

                default:
                    if(key!=0)
                        cout<< " | \e[1;31mTecla incorreta - verifique quais teclas controlam o robo\e[0m"<<endl;
                break;

            }

            if (Action::GetInstance()->IsRunning()==0 && Walking::GetInstance()->IsRunning()==0 && check_servo(&cm730, idServo, stop_gait)!=0)
                return 0;

        }
    }
    //==========================================================================================


    //***************************************************************************************
    //-------------------------Controle pela decisão-----------------------------------------
    while(1)
    {

            //Confere se o movimento atual e o mesmo do anterior----------
            if(buffer==read_int(mem, DECISION_ACTION_A))
                same_moviment = true;
            else
            {
                same_moviment = false;
                std::cout<< "\nAction " << read_int(mem, DECISION_ACTION_A); // Mostra o valor da ação
                count_read=0;
            }
            buffer = read_int(mem, DECISION_ACTION_A);
            //------------------------------------------------------------

            if (read_int(mem, IMU_STATE) && !variables.count("g")){ // Ve se esta caido
                if(read_float(mem, IMU_ACCEL_X) > 0){  //Levanta se caido de frente
                    actionMove.standupFront(stop_gait);
                }
                else{  //Levanta se caido de costa
                    actionMove.standupBack(stop_gait);
                }
                stop_gait = 1;
                sleep(1);
                flag_stop = false;
            }


            if(read_int(mem, DECISION_ACTION_A) == 0)
            {
                if(flag_stop==false)
                    gaitMove.robot_stop(stop_gait);
                flag_stop = true; //variavel que indica que o robo ja estava parado, isso evita de repetir o movimento
            }
            else
                flag_stop = false;

            if(read_int(mem, DECISION_ACTION_A) == 1)
                gaitMove.walk_foward_fast(stop_gait, same_moviment);

            if(read_int(mem, DECISION_ACTION_A) == 2)
                gaitMove.turn_left(stop_gait, true, same_moviment);

            if(read_int(mem, DECISION_ACTION_A) == 3)
                gaitMove.turn_right(stop_gait, true, same_moviment);

            if(read_int(mem, DECISION_ACTION_A) == 4)
                actionMove.kick_right_strong(&cm730, stop_gait);

            if(read_int(mem, DECISION_ACTION_A) == 5)
                actionMove.kick_left_strong(&cm730, stop_gait);

            if(read_int(mem, DECISION_ACTION_A) == 6)
                gaitMove.sidle_left(stop_gait, same_moviment);

            if(read_int(mem, DECISION_ACTION_A) == 7)
                gaitMove.sidle_right(stop_gait, same_moviment);

            if(read_int(mem, DECISION_ACTION_A) == 8)
                gaitMove.walk_foward_slow(stop_gait, false, same_moviment);

            if(read_int(mem, DECISION_ACTION_A) == 9)
                gaitMove.turn_around_ball_left(stop_gait, same_moviment);

            if(read_int(mem, DECISION_ACTION_A) == 10)
                actionMove.goalkeeper(stop_gait);

            if(read_int(mem, DECISION_ACTION_A) == 11)
                gaitMove.Gait_in_place(stop_gait, same_moviment);

            if(read_int(mem, DECISION_ACTION_A) == 12)
                actionMove.pass_left(&cm730, stop_gait);

            if(read_int(mem, DECISION_ACTION_A) == 13)
                actionMove.pass_right(&cm730, stop_gait);

            if(read_int(mem, DECISION_ACTION_A) == 14)
                gaitMove.turn_around_ball_right(stop_gait, same_moviment);

            if(read_int(mem, DECISION_ACTION_A) == 15)
            {
                if (read_int(mem, IMU_STATE))// check if robot is fall
                    actionMove.standupFront(stop_gait);
                else
                    std::cout<<" | \e[1;31mRobô não está caido ou IMU está desligada\e[0m"<<std::endl;
            }
            if(read_int(mem, DECISION_ACTION_A) == 16)
            {
                if (read_int(mem, IMU_STATE))// check if robot is fall
                    actionMove.standupBack(stop_gait);
                else
                    std::cout<<" | \e[1;31mRobô não está caido ou IMU está desligada\e[0m"<<std::endl;
            }
            if(read_int(mem, DECISION_ACTION_A) == 17)
            {
                gaitMove.walk_backward_fast(stop_gait, same_moviment);
            }
            if(read_int(mem, DECISION_ACTION_A) == 18)
            {
                gaitMove.walk_backward_slow(stop_gait, true, same_moviment);
            }

            if(read_int(mem, DECISION_ACTION_A) == 19)
                actionMove.greetings(stop_gait);

            if(read_int(mem, DECISION_ACTION_A) == 20)
                actionMove.goodBye(stop_gait);

            if(read_int(mem, DECISION_ACTION_A) == 21)
                actionMove.kick_right_weak(stop_gait); //Chute fraco com pe direito

            if(read_int(mem, DECISION_ACTION_A) == 22)
                actionMove.kick_left_weak(stop_gait); //Chute fraco com pe esquerdo

            //Imprime na tela o tempo que esta ocioso por nao receber uma nova instrucao da decisao-------
            count_read++;
            std::cout << "\rReading BlackBoard" <<"[\e[38;5;82m"<< count_read<<"\e[0m] | Tempo ocioso"<<"[\e[38;5;82m"<< count_read*step_time/1000<<"s\e[0m]";
            fflush (stdout);
            usleep(step_time*1000); //Operando na frequencia de 1/step_time Hertz
            //--------------------------------------------------------------------------------------------
    }
    //--------------------------------------------------------------------------------------------------
    //==================================================================

    std::cout<<"Press some key to end!\n"<<std::endl;
    getchar();

//    LinuxActionScript::ScriptStart("script.asc");
//    while(LinuxActionScript::m_is_running == 1) sleep(10);

    return 0;
}


//////////////////// Framework Initialize ////////////////////////////
// ---- Open USBDynamixel -----------------------------------------------{
int Initialize_servo()
{
    bool servoComunica = false;
    bool servoConectado = false;
    bool connectedRS = false;
    int * deviceIndex = new int;
    int idServo;
    char string_buffer[100]="";
    *deviceIndex = 0;         //endereça o Servo
    while(*deviceIndex<3)// laço que percorre o servo 0, 1 e 2.
    {
        sprintf(string1,"/dev/robot/servo%d", *deviceIndex);
        LinuxCM730* linux_cm730;
        linux_cm730 = new LinuxCM730(string1);
        CM730* cm730;
        cm730 = new CM730(linux_cm730);

        if( MotionManager::GetInstance()->Initialize(cm730) == 0)
        { // not connect with board rs485
            
        }
        else
        {
            cm730->ReadByte(1, 3, &idServo, 0); // Read the servo id of servo 1
            servoConectado = idServo == 1;
            usleep(1000);
            cm730->ReadByte(1, 3, &idServo, 0);//Try again because of fail
            servoConectado = idServo == 1;
            if(servoConectado)
            {
                   cout<<"Connected and communicating with the body of the robot!\n";
                 return 0;
            }
            else
            {// connected with board rs485 but it's not communicating
                sprintf(string_buffer,"%s/dev/robot/servo%d\n", string_buffer, *deviceIndex);
                connectedRS = true;
            }            
        }
        *deviceIndex = *deviceIndex + 1;
        delete cm730;
        delete linux_cm730;
    }
    delete deviceIndex; //desalocando da memória
    
    if(connectedRS == true)
    {
        printf("\e[0;31mConectou-se a placa USB/RS-485 mas não conseguiu se comunicar com o servo.\e[0m\n");
        cout<<"Endereços encontrado:"<<endl;
        cout<<string_buffer<<endl;
        cout<<"\e[0;36mVerifique se a chave que liga os servos motores está na posição ligada.\n\n\e[0m"<<endl;
    }
    else
    {
        cout<<"\e[1;31mNão há nenhuma placa USB/RS-485 conectada no computador.\n\n\e[0m"<<endl;
    }
    return 1;

}

int check_servo(CM730 *cm730, int idServo, bool &stop_gait)
{
    static int i=0;
    int save=-1;
    for(int erro,j=1 ; i==0 && j<=18; j++)
    {
        cm730->WriteByte(j, 11, LIMITE_TEMP, &erro);
    }

    i++;
    if (i==19) //Ultimo motor: 18
        i=1;

    if (i<=6){ // Membro superiores ate 6
        if(cm730->ReadWord(i, 34, &save, 0)!=0)
        {
            cout<<"Perda na comunicação com o motor "<<i<<" - Membro superior"<<endl;
            usleep(500000);
            return 0;
        }
        if (save<=0)// Testa o torque
        {
            if(cm730->ReadWord(i, 43, &save, 0)!=0)
            {
                cout<<"Perda na comunicação com o motor "<<i<<" - Membro superior"<<endl;
                usleep(500000);
                return 0;
            }
            
            if(save>=LIMITE_TEMP)
            {
                cout<<"Motor "<<i<<" aqueceu a " << save << ", motor desligado - Membro superior"<<endl;
                usleep(500000);
                return 0;
            }
            else
            {
                cout<<"Motor "<<i<<" excedeu torque, motor desligado - Membro superior"<<endl;
                usleep(500000);
                return 0;
            }
        }
    }

    else{ // Membro inferiores, do 7 em diante
        if(cm730->ReadWord(i, 34, &save, 0)!=0)
        {
            cout<<"Perda na comunicação com o motor "<<i<<" - Membro inferior"<<endl;
            usleep(500000);
            return 0;
        }
        if (save<=0)// Testa o torque
        {
            if(cm730->ReadWord(i, 43, &save, 0)!=0)
            {
                cout<<"Perda na comunicação com o motor "<<i<<" - Membro inferior"<<endl;
                usleep(500000);
                return 0;
            }
            
            if(save>=LIMITE_TEMP)
            {
                cout<<"Motor "<<i<<" aqueceu a " << save << ", motor desligado - Membro inferior"<<endl;
                usleep(500000);
                return 0;
            }
            else
            {
                cout<<"Motor "<<i<<" excedeu torque, motor desligado - Membro inferior"<<endl;
                usleep(500000);
                return 0;
            }
        }
    }

    return 0;
}








