#include <iostream>
#include "blackboard.h"
#include "minIni.h"

using namespace std;
#define INI_FILE_PATH "../../Control/Data/config.ini"

int main()
{
	minIni* ini;
	ini = new minIni((char *)INI_FILE_PATH);
	int *mem = using_shared_memory(ini->getd("Communication","no_player_robofei",-1024) * 100); 

	int x = read_int(mem, IMU_EULER_X);
	int y = read_int(mem, IMU_EULER_Y);
	int z = read_int(mem, IMU_EULER_Z);
	
	cout<<"Variacao em torno do eixo x: "<<x<<endl;
	cout<<"Variacao em torno do eixo y: "<<y<<endl;
	cout<<"Variaao em torno do eixo z: "<<z<<endl;

}

