#! /usr/bin/env python

import socket
import time
import sys
#sys.path.append('../../Blackboard/src/')

#from SharedMemory import SharedMemory 

UDP_IP = "255.255.255.255"
UDP_PORT = 3939
UDP_PORT_QUEST = 4242


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)#broadcast


while(True):
    ##### sending ######
    print '===== Question ====='
    qualit_direction = raw_input('Qualitative direction (all/f/fl/l/bl/b/br/r/fr): ')
    qualit_distance = raw_input('Qualitative distance (all/at/vc/c/f/vf/ft): ')
    relatum = raw_input('Related to the robot (blue/red/yellow/orange): ')
    message = 'question:' + ' ' + qualit_direction + ' ' + qualit_distance  + ' ' +  relatum
#    print "UDP target IP:", UDP_IP
#    print "UDP target port:", UDP_PORT
    print message
    sock.sendto(message, (UDP_IP, UDP_PORT))
    sock.sendto(message, (UDP_IP, UDP_PORT_QUEST))
    print ''
    time.sleep(3)


