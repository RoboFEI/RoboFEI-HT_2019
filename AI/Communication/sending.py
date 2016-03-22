#! /usr/bin/env python

import socket
import time
import sys
sys.path.append('../../Blackboard/src/')
sys.path.append('../../Localization/src/')

from SharedMemory import SharedMemory 
import mnemonics

UDP_IP = "255.255.255.255"
UDP_PORT = 3939
UDP_PORT_ROBOT = 4242

bkb = SharedMemory()

### UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
### broadcast
sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

while(True):
    if bkb.read_int('CONTROL_MESSAGES') == 2:
        message = str(bkb.read_int('ROBOT_NUMBER')) + ' ' + str(bkb.read_int('COM_POS_ORIENT_QUALIT_ROBOT_A')) + ' ' +  str(bkb.read_int('COM_POS_DIST_QUALIT_ROBOT_A')) + ' ' + str(bkb.read_int('LOCALIZATION_FIND_ROBOT'))
        #print "UDP target IP:", UDP_IP
        #print "UDP target port:", UDP_PORT
        print "message:", message
        sock.sendto(message, (UDP_IP, UDP_PORT))
        
        bkb.write_int('CONTROL_MESSAGES', 0)
        time.sleep(1)

        
    if bkb.read_int('CONTROL_MESSAGES') == 3:
        robot_string = ''
        content = [line.strip() for line in open("../../Localization/src/eopra-answer.txt", 'r')]
        print content
        
        for robot in content:
            robot_string = robot + ' ' + robot_string

        message = str(mnemonics.numbers_to_robot_color(bkb.read_int('ROBOT_NUMBER'))) + ' robot' + ' answer: ' + robot_string
        sock.sendto(message, (UDP_IP, UDP_PORT_ROBOT))
        #print "UDP target IP:", UDP_IP
        #print "UDP target port:", UDP_PORT
        print message
        time.sleep(1)

        bkb.write_int('CONTROL_MESSAGES', 0)
        time.sleep(1)

    #time.sleep(1)
