#! /usr/bin/env python

import socket
import sys
sys.path.append('../../Blackboard/src/')
sys.path.append('../../Localization/src/')

import mnemonics
from SharedMemory import SharedMemory 
 
UDP_IP = "255.255.255.255"
UDP_PORT = 3939

bkb = SharedMemory()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT)) 

bkb.write_int('CONTROL_MESSAGES',0)

with open("../../Localization/src/eopra-received.txt","w") as f:
    pass

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data
    
    data1 = data.split()
    
    if data1[0] == 'question:':
        bkb.write_int('CONTROL_MESSAGES',1)
        bkb.write_int('ASKED_QUALIT_DIRECT', mnemonics.qualit_directions_to_numbers(data1[1]))
        bkb.write_int('ASKED_QUALIT_DISTANCE', mnemonics.qualit_distances_to_numbers(data1[2]))
        bkb.write_int('ASKED_RELATED_ROBOT', mnemonics.robot_color_to_numbers(data1[3]))
        with open("../../Localization/src/eopra-received.txt","w") as f:
            pass
    else:
        bkb.write_int('RECEIVED_ROBOT_SENDING', int(data1[0]))
        bkb.write_int('RECEIVED_QUAL_ORIENT',  int(data1[1]))
        bkb.write_int('RECEIVED_QUAL_DIST', int(data1[2]))
        bkb.write_int('RECEIVED_ROBOT_SEEN', int(data1[3]))
        with open("../../Localization/src/eopra-received.txt","a") as f:
            f.write(str(bkb.read_int('RECEIVED_ROBOT_SENDING')) + " " + str(bkb.read_int('RECEIVED_QUAL_ORIENT')) + " " + str(bkb.read_int('RECEIVED_QUAL_DIST')) + " " +  str(bkb.read_int('RECEIVED_ROBOT_SEEN')) + "\n")
    
