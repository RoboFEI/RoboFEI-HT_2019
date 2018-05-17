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
parser.add_argument('--localize', '-l', action="store_true", help = 'selects decision with localization')


args = parser.parse_args()

robot = Ordinary()

robot.run()
