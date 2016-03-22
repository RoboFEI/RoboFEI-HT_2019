#! /usr/bin/env python

import socket
import sys
import time

UDP_IP = "255.255.255.255"
UDP_PORT = 4242

###UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT)) 

while True:

    print '===== Answers ====='
    data, addr = sock.recvfrom(1024) 
    split_data = data.split()
    print data
    print
    #for i in range (0,int(split_data[0])):
    #    print data
    #    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
   # print '==================='
