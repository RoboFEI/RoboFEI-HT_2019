#! /usr/bin/env python
# coding=utf-8

import socket
import time

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

#looking for the library SharedMemory
import sys
sys.path.append('../../Blackboard/src/')
from SharedMemory import SharedMemory


# instantiate:
config = ConfigParser()

# looking for the file config.ini:
config.read('../../Control/Data/config.ini')

mem_key = int(config.get('Communication', 'no_player_robofei')) * 100

# Instantiate the BlackBoard's class:
bkb = SharedMemory()
mem = bkb.shd_constructor(mem_key)

rbt_number = int(config.get('Communication', 'no_player_robofei'))
bkb.write_int(mem,'ROBOT_NUMBER',rbt_number)

UDP_IP = "255.255.255.255"
UDP_PORT1 = 1231
UDP_PORT2 = 1232
UDP_PORT3 = 1233
UDP_PORT4 = 1234


bkb.write_int(mem, 'CONTROL_MESSAGES', 0)

while(True):
    if bkb.read_int(mem,'CONTROL_MESSAGES') == 2: #code #2 - sends distance value
        message = '2' + ' ' + str(bkb.read_int(mem,'ROBOT_NUMBER')) + ' ' + str(bkb.read_floatDynamic(mem,'DECISION_RBT01_DIST_BALL',bkb.read_int(mem,'ROBOT_NUMBER')-1))
        #message = str(bkb.read_int(mem,'ROBOT_NUMBER')) + ' ' + str(bkb.read_int(mem,'SEND_ACTION'))
        print "message:", message
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)#broadcast
        sock.sendto(message, (UDP_IP, UDP_PORT1))
        sock.sendto(message, (UDP_IP, UDP_PORT2))
        sock.sendto(message, (UDP_IP, UDP_PORT3))
        sock.sendto(message, (UDP_IP, UDP_PORT4))
        bkb.write_int(mem,'CONTROL_MESSAGES',0)
    time.sleep(1)
