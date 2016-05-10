/*--------------------------------------------------------------------
******************************************************************************
  * @file         vision.c
  * @author       Claudio Vilao - ROBOFEI-HT - FEI
  * @version      V0.0.1
  * @created      24/04/2014
  * @Modified by  Isaac Jesus da Silva - ROBOFEI-HT - FEI
  * @Modified     25/11/2015
  * @e-mail
  * @brief        Vision
  ****************************************************************************
/--------------------------------------------------------------------*/

#include"vision.h"

//using namespace std;

extern "C" bool initServo(int pos1, int pos2)
{
	int pos_servo1 = pos1;
	int pos_servo2 = pos2;
	//int index = 0;
    int deviceIndex = 0; //endereça a USB
    int baudnum = DEFAULT_BAUDNUM; //velocidade de transmissao
	// ---- Open USBDynamixel -----------------------------------------------{
		bool servoComunica = false;

		while(deviceIndex<3)// laço que percorre o servo 0, 1 e 2.
		{
			if( dxl_initialize(deviceIndex, baudnum) == 0 )
			{
				printf( "Failed to open servo%d!\n", deviceIndex );
				if(deviceIndex==2)  // Não encontrou nenhum
				{
					if(servoComunica)
						printf("Conectou-se a uma placa mas não conseguiu se comunicar com o servo\n");
					else
						printf("Não encontrou nenhuma placa do servo conectada a porta USB\n");
					return true;
				}
				deviceIndex++;      // Não conecta na placa do servo e tenta a proxima porta.
			}
			else
			{
				servoComunica = true;
				printf( "Succeed to open Servo%d!\n", deviceIndex );
					if(dxl_read_byte( HEAD_TILT, 3 ) == HEAD_TILT)
				{
		   			 	printf("Servo%d okay - Connected and communicated!\n", deviceIndex);
				 	dxl_write_word(19, 30, pos1);
				 	dxl_write_word(20, 30, pos2);
				 	return false;
				}
					else
					{
					printf("Servo wrong or not communicated!\n");
					if(deviceIndex==2)
					{
						printf("Conectou-se a uma placa mas não conseguiu se comunicar com o servo\n");
						return true;
					}
					deviceIndex++;
				}
			}
		}
	//-----------------------------------------------------------------------------}
}

extern "C" int dxlReadByte(int ID, int Pos)
{
	return dxl_read_byte(ID, Pos);
}

extern "C" int dxlReadWord(int ID, int Pos)
{
	return dxl_read_word(ID, Pos);
}

extern "C" void dxlWriteByte(int ID, int Pos, int value)
{
	dxl_write_byte(ID, Pos, value);
}

extern "C" void dxlWriteWord(int ID, int Pos, int value)
{
	dxl_write_word(ID, Pos, value);
}




