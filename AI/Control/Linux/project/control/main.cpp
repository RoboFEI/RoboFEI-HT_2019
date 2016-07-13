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
#include <unistd.h>
#include <iostream>
#include <stdio.h>
#include <termios.h>
#include <fcntl.h>
#include <stdlib.h>
#include <cstdlib>

#include <stdio.h>
#include <errno.h>
#include <sys/ipc.h>
#include <sys/shm.h>


#include "minIni.h"
#include <string>

#include "Action.h"
#include "Walking.h"
#include "MX28.h"
#include "MotionManager.h"
#include "LinuxMotionTimer.h"
#include "LinuxCM730.h"
#include "LinuxActionScript.h"
#include <blackboard.h>
#include <boost/program_options.hpp> //tratamento de argumentos linha de comando
#include "ReadConfig.hpp"

#ifdef MX28_1024
#define MOTION_FILE_PATH    "../../Control/Data/motion_1024.bin"
#else
#define MOTION_FILE_PATH    "../../Control/Data/motion_4096.bin"
#endif

#define INI_FILE_PATH       "../../Control/Data/config.ini"

#define DEBUG_PRINT true

#define LIMITE_TEMP 80	// Define a temperatura maxima dos motores

using namespace Robot;
using namespace std;

int kbhit(); //Function kbhit.cpp

int check_servo(CM730 *cm730, int idServo, bool &stop_gait);

int Initialize_servo();

void Gait_in_place(bool &stop_gait);

void move_action(int move_number, bool interrupt, bool &stop_gait); // Robot perform action move

void move_gait(float X_amplitude, float Y_amplitude, float A_amplitude, bool &stop_gait, ReadConfig* configGait, ReadConfig* configP); // Robot perform gait

void kick_right_strong(CM730 *cm730, bool &stop_gait);

void kick_left_strong(CM730 *cm730, bool &stop_gait);

void robot_stop(ReadConfig *gait , bool &stop_gait);

void pass_left(CM730 *cm730,bool &stop_gait);

void pass_right(CM730 *cm730,bool &stop_gait);

void goalkeeper(bool &stop_gait);

void change_current_dir()
{
    char exepath[1024] = {0};
    if(readlink("/proc/self/exe", exepath, sizeof(exepath)) != -1)
        chdir(dirname(exepath));
}

char string1[50]; //String

int main(int argc, char **argv)
{

    unsigned int tensaomedia = 0;

    change_current_dir();

    minIni* ini;
    ini = new minIni((char *)INI_FILE_PATH);

  	//Acopla ou cria a memoria compartilhada
    int *mem = using_shared_memory(ini->getd("Communication","no_player_robofei",-1024) * 100); //0 for real robot

    bool stop_gait = 1;
	char *Servoport;
    sprintf(string1,"echo fei 123456| sudo -S renice -20 -p %d", getpid()); // prioridade maxima do codigo
    system(string1);//prioridade
    float turn_angle = 20;
    float walk_foward= 15;
    int value;
	int erro;
	int idServo;

    printf( "\n===== ROBOFEI-HT Control Process =====\n\n");

    Action::GetInstance()->LoadFile((char *)MOTION_FILE_PATH);



    //Carregando valores do config.ini -----------------------------------------
    ReadConfig gait("Gait",ini);
    ReadConfig walkfoward("Walking Config",ini);
    ReadConfig turnRobot("Turn Robot",ini);
    ReadConfig walkslow("Walk Slow",ini);
    ReadConfig turnBallR("Turn Ball Right",ini);
    ReadConfig turnBallL("Turn Ball Left",ini);
    ReadConfig sidleR("Sidle Right",ini);
    ReadConfig sidleL("Sidle Left",ini);

	//**************************************************************************
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


	MotionManager::GetInstance()->LoadINISettings(ini);

    Walking::GetInstance()->LoadINISettings(ini); 
    MotionManager::GetInstance()->AddModule((MotionModule*)Action::GetInstance());
    MotionManager::GetInstance()->AddModule((MotionModule*)Walking::GetInstance());
    LinuxMotionTimer linuxMotionTimer;
	linuxMotionTimer.Initialize(MotionManager::GetInstance());
	linuxMotionTimer.Start();
    /////////////////////////////////////////////////////////////////////

//	printf("Pronto 3\n");
//    getchar();

	Action::GetInstance()->Initialize();
    Walking::GetInstance()->m_Joint.SetEnableBody(false);
    Action::GetInstance()->m_Joint.SetEnableBody(true);
    MotionManager::GetInstance()->SetEnable(true);

	std::cout<<"Start Action 1"<<std::endl;
    Action::GetInstance()->Start(1);    /* Init(stand up) pose */
    while(Action::GetInstance()->IsRunning()) usleep(8*1000); 
	Action* a=Action::GetInstance();

//	getchar();	

//	std::cout<<"Start Action 9"<<std::endl;
//    Action::GetInstance()->Start(9);   // Posicionando para andar
//    while(Action::GetInstance()->IsRunning()) usleep(8*1000); 

	Action::GetInstance()->Stop();

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
				    cout << "Levantar quando as costas está para cima" << endl;
					move_action(11, 0, stop_gait);
		        break;

		        case 98: //b
				    cout << "Levantar quando o peito está para cima" << endl;
					move_action(10, 0, stop_gait);
		        break;
		        
		        case 112: //p
				    kick_right_strong(&cm730, stop_gait);
		        break;

		        case 108: //l
				    kick_left_strong(&cm730, stop_gait);
		        break;

		        case 99: //c
				    cout << "Chutar direito bola laranja" << endl;
					move_action(12, 0, stop_gait);
		        break;

		        case 103: //g
				    cout << "Chutar esquerdo bola laranja" << endl;
					move_action(61, 0, stop_gait);
		        break;

		        case 102: //f
				    cout << "Andar para frente" << endl;
					move_gait(walkfoward.walk_foward, walkfoward.sidle, walkfoward.turn_angle, stop_gait, &gait, &walkfoward);
		        break;

		        case 100: //d
				    cout << "Vira para direita" << endl;
					move_gait(turnRobot.walk_foward, turnRobot.sidle, -turnRobot.turn_angle, stop_gait, &gait, &turnRobot);
		        break;

		        case 105: //i
				    pass_left(&cm730, stop_gait);
		        break;

		        case 101: //e
				    cout << "Vira para esquerda" << endl;
					move_gait(turnRobot.walk_foward, turnRobot.sidle, turnRobot.turn_angle, stop_gait, &gait, &turnRobot);
		        break;

		        case 106: //j
				    pass_right(&cm730, stop_gait);
		        break;

		        case 109: //m
				    cout << "Andar de lado esquerda" << endl;
					move_gait(sidleL.walk_foward, sidleL.sidle, sidleL.turn_angle, stop_gait, &gait, &sidleL);
		        break;

		        case 110: //n
				    cout << "Andar de lado direita" << endl;
					move_gait(sidleR.walk_foward, -sidleR.sidle, sidleR.turn_angle, stop_gait, &gait, &sidleR);
		        break;

		        case 111: //o
				    cout << "Rotacionar a esquerda em volta da bola" << endl;
					move_gait(turnBallL.walk_foward, turnBallL.sidle, turnBallL.turn_angle, stop_gait, &gait, &turnBallL);
		        break;

		        case 113: //q
				    cout << "Rotacionar a direita em volta da bola" << endl;
					move_gait(turnBallR.walk_foward, -turnBallR.sidle, -turnBallR.turn_angle, stop_gait, &gait, &turnBallR);
		        break;

		        case 107: //k
				    cout << "Andar curto para frente" << endl;
					move_gait(walkslow.walk_foward, walkslow.sidle, walkslow.turn_angle, stop_gait, &gait, &walkslow);
		        break;

		        case 114: //r
				    cout << "Andar curto para traz" << endl;
					move_gait(-walkslow.walk_foward, walkslow.sidle, walkslow.turn_angle, stop_gait, &gait, &walkslow);
		        break;

		        case 118: //v
				    cout << "Andar rapido para traz" << endl;
					move_gait(-walkfoward.walk_foward, walkfoward.sidle, walkfoward.turn_angle, stop_gait, &gait, &walkfoward);
		        break;

		        case 115: //s
					cout << "Stop com gait" << endl;
					move_gait(gait.walk_foward, gait.sidle, gait.turn_angle, stop_gait, &gait, &gait);
		        break;

		        case 116: //t
		            robot_stop(&gait , stop_gait);
		        break;
		        
		        case 117: //u
		            goalkeeper(stop_gait);
		        break;

		        case 104: //h
				    cout << "Greetings" << endl;
					move_action(24, 0, stop_gait);
		        break;

                case 122: //z
                    cout<<" | GoodBye"<<endl;
			        move_action(8, 0, stop_gait);
			     break;

		        case 27: //ESC (stop)
				    cout << "Stop and shutdown code" << endl;
					return 0;
		        break;

				default:
					if(key!=0)
						cout<< "Tecla incorreta - verifique quais teclas controlam o robo"<<endl;
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

			std::cout<< "Action " << read_int(mem, DECISION_ACTION_A); // Mostra o valor da ação

			if (read_int(mem, IMU_STATE) && !variables.count("g")){ // Ve se esta caido
				if(read_float(mem, IMU_ACCEL_X) > 0){  //Levanta se caido de frente
					std::cout<<" | Levantar de frente";
					move_action(10, 0, stop_gait);
				}
				else{  //Levanta se caido de costa
					std::cout<<" | Levantar de costa";
					move_action(11, 0, stop_gait);
				}
				stop_gait = 1;
				sleep(1);
			}


			if(read_int(mem, DECISION_ACTION_A) == 0)
			{
		        robot_stop(&gait , stop_gait);
			}

			if(read_int(mem, DECISION_ACTION_A) == 1)
			{
				std::cout<<" | Andar para frente"<<std::endl;
				move_gait(walkfoward.walk_foward, walkfoward.sidle, walkfoward.turn_angle, stop_gait, &gait, &walkfoward);
			}
			if(read_int(mem, DECISION_ACTION_A) == 2)
			{
				std::cout<<" | Virar a esquerda"<<std::endl;
				move_gait(turnRobot.walk_foward, turnRobot.sidle, turnRobot.turn_angle, stop_gait, &gait, &turnRobot);
			}
			if(read_int(mem, DECISION_ACTION_A) == 3)
			{
				std::cout<<" | Virar a direita"<<std::endl;
				move_gait(turnRobot.walk_foward, turnRobot.sidle, -turnRobot.turn_angle, stop_gait, &gait, &turnRobot);
			}
			if(read_int(mem, DECISION_ACTION_A) == 4)
			{
                kick_right_strong(&cm730, stop_gait);
			}
			if(read_int(mem, DECISION_ACTION_A) == 5)
			{
			    kick_left_strong(&cm730, stop_gait);
			}
			if(read_int(mem, DECISION_ACTION_A) == 6)
			{
				std::cout<<" | Andar de Lado esquerda"<<std::endl;
				move_gait(sidleL.walk_foward, sidleL.sidle, sidleL.turn_angle, stop_gait, &gait, &sidleL);
			}
			if(read_int(mem, DECISION_ACTION_A) == 7)
			{
				std::cout<<" | Andar de Lado direita"<<std::endl;
				move_gait(sidleR.walk_foward, -sidleR.sidle, sidleR.turn_angle, stop_gait, &gait, &sidleR);
			}
			if(read_int(mem, DECISION_ACTION_A) == 8)
			{
				std::cout<<" | Andar lento para frente"<<std::endl;
				if(float(read_int(mem, DECISION_ACTION_B))<walkslow.walk_foward)
				    move_gait(float(read_int(mem, DECISION_ACTION_B)), walkslow.sidle, walkslow.turn_angle, stop_gait, &gait, &walkslow);
				else
    				move_gait(walkslow.walk_foward, walkslow.sidle, walkslow.turn_angle, stop_gait, &gait, &walkslow);
			}
			if(read_int(mem, DECISION_ACTION_A) == 9)
			{
				std::cout<<" | Girar em torno da bola para esquerda"<<std::endl;
				move_gait(turnBallL.walk_foward, turnBallL.sidle, turnBallL.turn_angle, stop_gait, &gait, &turnBallL);
			}

			if(read_int(mem, DECISION_ACTION_A) == 10)
			{
				goalkeeper(stop_gait);  // colocar o action-script para cair e defender!!!
			}
			if(read_int(mem, DECISION_ACTION_A) == 11)
			{
				std::cout<<" | Stop com gait"<<std::endl;
			    move_gait(gait.walk_foward, gait.sidle, gait.turn_angle, stop_gait, &gait, &gait);
			}
			if(read_int(mem, DECISION_ACTION_A) == 12)
			{			
				pass_left(&cm730, stop_gait);
            }
            if(read_int(mem, DECISION_ACTION_A) == 13)
			{			
				pass_right(&cm730, stop_gait);
            }

			if(read_int(mem, DECISION_ACTION_A) == 14)
			{
				std::cout<<" | Girar em torno da bola para direita"<<std::endl;
				move_gait(turnBallR.walk_foward, -turnBallR.sidle, -turnBallR.turn_angle, stop_gait, &gait, &turnBallR);
			}
			if(read_int(mem, DECISION_ACTION_A) == 15)
			{
				if (read_int(mem, IMU_STATE)){ // check if robot is fall
					std::cout<<" | Levantar de frente"<<std::endl;
					move_action(10, 0, stop_gait);
				}
				else
					std::cout<<" | \e[1;31mRobô não está caido ou IMU está desligada\e[0m"<<std::endl;
			}
			if(read_int(mem, DECISION_ACTION_A) == 16)
			{
				if (read_int(mem, IMU_STATE)){ // check if robot is fall
					std::cout<<" | Levantar de costa"<<std::endl;
					move_action(11, 0, stop_gait);
				}
				else
					std::cout<<" | \e[1;31mRobô não está caido ou IMU está desligada\e[0m"<<std::endl;
			}
			if(read_int(mem, DECISION_ACTION_A) == 17)
			{
				cout<<" | Andar rapido para traz"<<endl;
				move_gait(-walkfoward.walk_foward, walkfoward.sidle, walkfoward.turn_angle, stop_gait, &gait, &walkfoward);
			}
			if(read_int(mem, DECISION_ACTION_A) == 18)
			{
				cout<<" | Andar lento para traz"<<endl;
				move_gait(-walkslow.walk_foward, walkslow.sidle, walkslow.turn_angle, stop_gait, &gait, &walkslow);
			}
			if(read_int(mem, DECISION_ACTION_A) == 19)
			{
				cout<<" | Greetings"<<endl;
			    move_action(24, 0, stop_gait);
			}
			if(read_int(mem, DECISION_ACTION_A) == 20)
			{
				cout<<" | GoodBye"<<endl;
			    move_action(8, 0, stop_gait);
			}
			usleep(50000);
			
	}
	//--------------------------------------------------------------------------------------------------
	//==================================================================


    std::cout<<"Press some key to end!\n"<<std::endl;
    getchar();

//    LinuxActionScript::ScriptStart("script.asc");
//    while(LinuxActionScript::m_is_running == 1) sleep(10);

    return 0;
}

//========================================================================
//Execute the move action-------------------------------------------------
void move_action(int move_number, bool interrupt, bool &stop_gait )
{
    write_int(mem, CONTROL_MOVING, 1);
	while(Walking::GetInstance()->GetCurrentPhase()!=0 && Walking::GetInstance()->IsRunning()!=0)  usleep(8*1000);
	Walking::GetInstance()->Stop();
	Walking::GetInstance()->m_Joint.SetEnableBody(false);
	Action::GetInstance()->m_Joint.SetEnableBody(true);
	MotionManager::GetInstance()->SetEnable(true);
	Action::GetInstance()->Start(move_number); // Realiza a ação do numero contido no move_number
	while(Action::GetInstance()->IsRunning() && ~interrupt) usleep(8*1000); // Aguarda finalizar a ação ou para por interrupção
	stop_gait = 1;
	write_int(mem, CONTROL_MOVING, 0);
}

//========================================================================
//Execute the gait generation---------------------------------------------
void move_gait(float X_amplitude, float Y_amplitude, float A_amplitude, bool &stop_gait, ReadConfig* configGait, ReadConfig* configP)
{
    write_int(mem, CONTROL_MOVING, 1);
	if(Walking::GetInstance()->IsRunning()==0)
	{
		//Gait_in_place(stop_gait); // Need performes the Gait before performe others moviments
		if(stop_gait == 1)
		{
			move_action(9, 0, stop_gait);
			stop_gait = 0;
		}
                write_int(mem, CONTROL_MOVING, 1);
		cout << "Stop com gait" << endl;
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
void Gait_in_place(bool &stop_gait)
{
//    CONTROL_MOVING = 1;
//	if(stop_gait == 1)
//	{
//		cout << "Action 9" << endl;
//		move_action(9, 0, stop_gait);
//		stop_gait = 0;
//	}
//	move_gait(0.0, 0.0, 0.0, stop_gait);
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
	*deviceIndex = 0; 		//endereça o Servo
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

//==============================================================================
void robot_stop(ReadConfig *gait , bool &stop_gait)
{
    //write_int(mem, CONTROL_MOVING, 1);
    if (Walking::GetInstance()->IsRunning()!=0)
    {
		move_gait(gait->walk_foward, gait->sidle, gait->turn_angle, stop_gait, gait, gait);
		sleep(1);
	}
	std::cout<<" | Nada a fazer"<<std::endl;
	while(Walking::GetInstance()->GetCurrentPhase()!=0 && Walking::GetInstance()->IsRunning()!=0)  usleep(8*1000);
	Walking::GetInstance()->Stop();
	Walking::GetInstance()->m_Joint.SetEnableBody(false);
	Action::GetInstance()->m_Joint.SetEnableBody(true);
	MotionManager::GetInstance()->SetEnable(true);
	usleep(500000); //Aguarda 0.5 segundos
	Action::GetInstance()->Start(1); // Realiza a ação do numero contido no move_number
	while(Action::GetInstance()->IsRunning()) usleep(8*1000);
	stop_gait = 1;
	write_int(mem, CONTROL_MOVING, 0);
}

//==============================================================================
void kick_left_strong(CM730 *cm730, bool &stop_gait)
{
    write_int(mem, CONTROL_MOVING, 1);
    int erro;
    int value;
    cout << "Chute esquerdo bola branca" << endl;
	move_action(1, 0, stop_gait);
	Action::GetInstance()->Start(62);
    while(Action::GetInstance()->IsRunning()) usleep(8*1000);
	Action::GetInstance()->Stop();
	Action::GetInstance()->m_Joint.SetEnableBody(false);
    MotionManager::GetInstance()->SetEnable(false);

	//getchar();

	// Velocidades
	cm730->WriteWord(12, 32, 985, &erro);
	cm730->WriteWord(14, 32, 812, &erro);
	cm730->WriteWord(16, 32, 1023, &erro);
    cm730->WriteWord(18, 32, 150, &erro);

	cm730->WriteWord(12, 30, MotionManager::GetInstance()->m_Offset[12]+741, &erro);
	cm730->WriteWord(14, 30, MotionManager::GetInstance()->m_Offset[14]+327, &erro);
	cm730->WriteWord(16, 30, MotionManager::GetInstance()->m_Offset[16]+501, &erro);
	cm730->WriteWord(18, 30, MotionManager::GetInstance()->m_Offset[18]+478, &erro);

	//Esperando movimento
	cm730->ReadWord(16, 36, &value, 0);
	while(abs(value-(MotionManager::GetInstance()->m_Offset[16]+501))>10)
	{
	    cm730->ReadWord(16, 36, &value, 0);
	    //cout<<"position: "<<MotionManager::GetInstance()->m_Offset[14]+409<<" value: "<<value<<" dif: "<<abs(value-(MotionManager::GetInstance()->m_Offset[14]+409))<<endl;
		usleep(8*1000);
	}

	Action::GetInstance()->m_Joint.SetEnableBody(true);
	MotionManager::GetInstance()->SetEnable(true);
	Action::GetInstance()->Start(63);
	while(Action::GetInstance()->IsRunning()) usleep(8*1000);
	stop_gait = 1;
	write_int(mem, CONTROL_MOVING, 0);
}

//==============================================================================
void kick_right_strong(CM730 *cm730, bool &stop_gait)
{
    write_int(mem, CONTROL_MOVING, 1);
    int erro;
    int value;
	cout << "Chute direito bola branca" << endl;
	move_action(1, 0, stop_gait);
	while(Action::GetInstance()->IsRunning()) usleep(8*1000);
	Action::GetInstance()->Start(60);
	while(Action::GetInstance()->IsRunning()) usleep(8*1000);
	Action::GetInstance()->Stop();
	Action::GetInstance()->m_Joint.SetEnableBody(false);
	MotionManager::GetInstance()->SetEnable(false);

	//getchar();

	// Velocidades
	cm730->WriteWord(11, 32, 399, &erro);
	cm730->WriteWord(13, 32, 926, &erro);
	cm730->WriteWord(15, 32, 1023, &erro);
	cm730->WriteWord(17, 32, 97, &erro);

	cm730->WriteWord(11, 30, MotionManager::GetInstance()->m_Offset[11]+294, &erro);
	cm730->WriteWord(13, 30, MotionManager::GetInstance()->m_Offset[13]+614, &erro);
	cm730->WriteWord(15, 30, MotionManager::GetInstance()->m_Offset[15]+448, &erro);
	cm730->WriteWord(17, 30, MotionManager::GetInstance()->m_Offset[17]+545, &erro);
					
	//Esperando movimento
	cm730->ReadWord(15, 36, &value, 0);
	while(abs(value-(MotionManager::GetInstance()->m_Offset[15]+448))>10)
	{
	    cm730->ReadWord(15, 36, &value, 0);
		//cout<<"position: "<<MotionManager::GetInstance()->m_Offset[15]+448<<" value: "<<value<<" dif: "<<abs(value-(MotionManager::GetInstance()->m_Offset[15]+448))<<endl;
		usleep(8*1000);
	}

	Action::GetInstance()->m_Joint.SetEnableBody(true);
	MotionManager::GetInstance()->SetEnable(true);
	Action::GetInstance()->Start(61);
	while(Action::GetInstance()->IsRunning()) usleep(8*1000);
	stop_gait = 1;
	write_int(mem, CONTROL_MOVING, 0);

}

//==============================================================================
void pass_left(CM730 *cm730, bool &stop_gait)
{
    write_int(mem, CONTROL_MOVING, 1);
    int erro;
    int value;
    cout << "Passe Esquerda" << endl;
	move_action(1, 0, stop_gait);
	Action::GetInstance()->Start(70);
	while(Action::GetInstance()->IsRunning()) usleep(8*1000);
	Action::GetInstance()->Stop();
	Action::GetInstance()->m_Joint.SetEnableBody(false);
	MotionManager::GetInstance()->SetEnable(false);
					
	//getchar();
					
	// Velocidades
	cm730->WriteWord(7, 32, 255, &erro);
	cm730->WriteWord(9, 32, 1023, &erro);
					
	cm730->WriteWord(7, 30, MotionManager::GetInstance()->m_Offset[7]+603, &erro);
	cm730->WriteWord(9, 30, MotionManager::GetInstance()->m_Offset[9]+385, &erro);
					
	//Esperando  completar o movimento
	unsigned int count_s = 0;
	cm730->ReadWord(9, 46, &value, 0);
	while(value!=0)
	{
	    count_s++;
		cm730->ReadWord(9, 46, &value, 0);
		usleep(8*1000);
		if(count_s>100)
		    break; //Evita de ficar parado neste laco
	}
	//std::cout<<count_s<<std::endl;

	Action::GetInstance()->m_Joint.SetEnableBody(true);
	MotionManager::GetInstance()->SetEnable(true);
	Action::GetInstance()->Start(72);
	while(Action::GetInstance()->IsRunning()) usleep(8*1000);
	stop_gait = 1;
	write_int(mem, CONTROL_MOVING, 0);
	
}

//==============================================================================
void pass_right(CM730 *cm730, bool &stop_gait)
{
    write_int(mem, CONTROL_MOVING, 1);
    cout << "Passe Direita" << endl;
    int erro;
    int value;
	move_action(1, 0, stop_gait);
    Action::GetInstance()->Start(71);
	while(Action::GetInstance()->IsRunning()) usleep(8*1000);
	Action::GetInstance()->Stop();
	Action::GetInstance()->m_Joint.SetEnableBody(false);
    MotionManager::GetInstance()->SetEnable(false);
					
	//getchar();
					
	// Velocidades
	cm730->WriteWord(8, 32, 255, &erro);
	cm730->WriteWord(10, 32, 1023, &erro);
					
    cm730->WriteWord(8, 30, MotionManager::GetInstance()->m_Offset[8]+420, &erro);
	cm730->WriteWord(10, 30, MotionManager::GetInstance()->m_Offset[10]+638, &erro);
					
	//Esperando  completar o movimento
	unsigned int count_s = 0;
	cm730->ReadWord(10, 46, &value, 0);
	while(value!=0)
	{
	    count_s++;
		cm730->ReadWord(10, 46, &value, 0);
		usleep(8*1000);
		if(count_s>100)
		    break; //Evita de ficar parado neste laco
	}
	//std::cout<<count_s<<std::endl;
					
	Action::GetInstance()->m_Joint.SetEnableBody(true);
	MotionManager::GetInstance()->SetEnable(true);
	Action::GetInstance()->Start(73);
    while(Action::GetInstance()->IsRunning()) usleep(8*1000);
    stop_gait = 1;
    write_int(mem, CONTROL_MOVING, 0);
    
}

void goalkeeper(bool &stop_gait)
{
    std::cout<<" | Defender a bola"<<std::endl;  //------------------------------TODO
    move_action(1, 0, stop_gait);    /* Init(stand up) pose */
    move_action(20, 0, stop_gait);    // colocar o action-script para cair e defender!!!
}



