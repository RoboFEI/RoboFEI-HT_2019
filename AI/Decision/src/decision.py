#! /usr/bin/env python
#coding: utf-8
#  ----------------------------------------------------------------------------
#  ****************************************************************************
#  * @file decision.py
#   *@project: ROBOFEI-HT - FEI 😛
#  * @author Isaac Jesus da Silva
#  * @version V0.0.1
#  * @created 06/10/2015
#  * @e-mail isaac25silva@yahoo.com.br
#  * @brief Decision
#   *@modified by: Danilo H. Perico
#   *@modified: 14 Oct 2015
#  ****************************************************************************
#  Program to execute the Decision process
#  ****************************************************************************

#import parser for arguments    
import argparse

from behavior import *

print
print '################### Decision #########################'
print 

#create arguments for each behavior
parser = argparse.ArgumentParser(description='Robot behavior', epilog= 'Se nenhuma ação for selecionada um comportamento comum será adotado! / If there is not a selected argument an ordinary behavior will be adopted!')
parser.add_argument('--golie', '-g', action="store_true", help = 'Seleciona comportamento de goleiro / selects golie behavior')
parser.add_argument('--quarterback', '-q', action="store_true", help = 'Seleciona comportamento de zagueiro / selects quarterback behavior')
parser.add_argument('--attacker', '-a', action="store_true", help = 'Seleciona comportamento de atacante / selects attacker behavior')

args = parser.parse_args()

#Golie decision:
if args.golie == True:
    robot = Golie()
    
#Quarterback decicion:    
elif args.quarterback == True:
    robot = Quarterback()
    
#Attacker decision:    
elif args.attacker == True:
    robot = Attacker()
    
#Ordinary decision:
else:
    robot = Ordinary()


#loop
while True:
    
    if robot.get_referee_usage() == 'yes':
        robot.decision(robot.get_referee()) #will read the referee 
    else:
        robot.decision(2) #always on play 
   
    time.sleep(0.2) 
    
    
    
