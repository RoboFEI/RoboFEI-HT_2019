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
parser = argparse.ArgumentParser(description='Robot behavior', epilog= 'If there is not a selected argument an ordinary behavior will be adopted!')
parser.add_argument('--golie', '-g', action="store_true", help = 'selects golie behavior')
parser.add_argument('--quarterback', '-q', action="store_true", help = 'selects quarterback behavior')
parser.add_argument('--attacker', '-a', action="store_true", help = 'selects attacker behavior')
parser.add_argument('--naive', '-n', action="store_true", help = 'selects naive behavior')
parser.add_argument('--naive_imu', '-ni', action="store_true", help = 'selects naive behavior with orientation')
parser.add_argument('--naive_imu_dec_turning', '-nidt', action="store_true", help = 'selects naive behavior with orientation')

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

#Naive decision:
elif args.naive == True:
    robot = Naive()

# Naive decision with orientation:
elif args.naive_imu == True:
    robot = NaiveIMU()
    
# Naive decision with orientation:
elif args.naive_imu_dec_turning == True:
    robot = NaiveIMUDecTurning()

#Ordinary decision:
else:
    robot = Ordinary()


#loop
while True:

    if robot.get_referee_usage() == 'yes':
        robot.decision(robot.get_referee()) #will read the referee 
    else:
        robot.decision(2) #always on play

    robot.bkb.write_int(robot.mem, 'DECISION_WORKING', 1)

    time.sleep(0.05) 
    
    
    
