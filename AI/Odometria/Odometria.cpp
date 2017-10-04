#include <iostream>
#include <unistd.h>
#include "blackboard.h"
#include "minIni.h"

using namespace std;
#define INI_FILE_PATH "../../Control/Data/config.ini"

int main()
{
	unsigned int microseconds;

	float x, y, z;

	minIni* ini;
	ini = new minIni((char *)INI_FILE_PATH);
	int *mem = using_shared_memory(ini->getd("Communication","no_player_robofei",-1024) * 100); 

	while(1)
	{
		x = read_float(mem, IMU_EULER_X);
		y = read_float(mem, IMU_EULER_Y);
		z = read_float(mem, IMU_EULER_Z);
	
		cout<<"x: "<<x<<endl;
		cout<<"y: "<<y<<endl;
		cout<<"z: "<<z<<endl;
		
		cout <<"\033[2J\033[1;1H";
		
		usleep(100000);
	}
}

