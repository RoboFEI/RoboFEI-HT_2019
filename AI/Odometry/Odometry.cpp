#include <iostream>
#include <unistd.h>
#include "blackboard.h"
#include "minIni.h"

using namespace std;
#define INI_FILE_PATH "../../Control/Data/config.ini"

int main()
{
	unsigned int microseconds;

	int M[12], Motor, i=0, k, id;
	float x, y, z;

	minIni* ini;
	ini = new minIni((char *)INI_FILE_PATH);
	int *mem = using_shared_memory(ini->getd("Communication","no_player_robofei",-1024) * 100); 

	while(1)
	{
		x = read_float(mem, IMU_EULER_X);
		y = read_float(mem, IMU_EULER_Y);
		z = read_float(mem, IMU_EULER_Z);

		for(id=7; id<19; id++) 
    		{
			Motor = id+101; //soma 101 para que os valores de id sejam equivalentes aos indices de variáveis da blackboard
			M[id-7] = read_int(mem, Motor); //Read the servo position on the blackboard
    		}
	
		cout<<"x: "<<x<<endl;
		cout<<"y: "<<y<<endl;
		cout<<"z: "<<z<<endl;

		for(i=0; i<12; i++) 
    		{
			k = i+7; //Incrementa o indice do respectivo motor
			cout << "Motor"<<k<<": "<<M[i]<<endl; //Apresenta valores dos motores
    		}
	
		cout <<"\033[2J\033[1;1H"; //Clean the terminal screen
		
		usleep(100000);
	}
}

