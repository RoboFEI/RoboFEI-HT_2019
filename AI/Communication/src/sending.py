#! /usr/bin/env python

import socket
import sys
import time
sys.path.append('../../Blackboard/src/')
sys.path.append('../../Localization/src/')

from SharedMemory import SharedMemory 
 
UDP_IP = "255.255.255.255"
UDP_PORT = 3939

bkb = SharedMemory()

MESSAGE = "Hello, World!"
 
print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

while(True):
    ### UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    ### broadcast
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

    time.sleep(2)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

