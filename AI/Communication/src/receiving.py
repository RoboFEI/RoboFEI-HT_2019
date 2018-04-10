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
# UDP_PORT1 = 3939
# UDP_PORT2 = 3838
# UDP_PORT3 = 3737
# UDP_PORT4 = 3636

if bkb.read_int(mem,'ROBOT_NUMBER')==1:
    UDP_PORT = 1231
elif bkb.read_int(mem,'ROBOT_NUMBER')==2:
    UDP_PORT = 1232
elif bkb.read_int(mem,'ROBOT_NUMBER')==3:
    UDP_PORT = 1233
elif bkb.read_int(mem,'ROBOT_NUMBER')==4:
    UDP_PORT = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data
    data1 = data.split()
    if data1[0] == '2':  #code #2 - receives distance value
        bkb.write_floatDynamic(mem,'DECISION_RBT01_DIST_BALL',int(data1[1])-1,float(data1[2]))
    time.sleep(1)