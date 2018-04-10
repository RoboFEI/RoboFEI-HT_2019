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

# Used to centralize the robot somewhere, given it's number.
X_ROBOT = 0
Y_ROBOT = 0
if rbt_number % 2 == 1:
    X_ROBOT = 295
else:
    X_ROBOT = 745

if rbt_number > 2:
    Y_ROBOT = 520
else:
    Y_ROBOT = 220
# This will be removed after Localization is finished.

UDP_IP = "255.255.255.255"
UDP_PORT1 = 1231
UDP_PORT2 = 1232
UDP_PORT3 = 1233
UDP_PORT4 = 1234

UDP_PORT_TELE = 1240 + rbt_number

# Opens only once the socket for communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) # Broadcast

bkb.write_int(mem, 'CONTROL_MESSAGES', 0)
bkb.write_int(mem, 'CONTROL_WORKING', 0) # Sets the flag
bkb.write_int(mem, 'VISION_WORKING', 0) # Sets the flag
bkb.write_int(mem, 'LOCALIZATION_WORKING', 0) # Sets the flag
bkb.write_int(mem, 'DECISION_WORKING', 0) # Sets the flag
bkb.write_int(mem, 'IMU_WORKING', 0) # Sets the flag

while(True):
    if bkb.read_int(mem,'CONTROL_MESSAGES') == 2: #code #2 - sends distance value
        message = '2' + ' ' + str(bkb.read_int(mem,'ROBOT_NUMBER')) + ' ' + str(bkb.read_floatDynamic(mem,'DECISION_RBT01_DIST_BALL',bkb.read_int(mem,'ROBOT_NUMBER')-1))
        #message = str(bkb.read_int(mem,'ROBOT_NUMBER')) + ' ' + str(bkb.read_int(mem,'SEND_ACTION'))
        print "message:", message
        sock.sendto(message, (UDP_IP, UDP_PORT1))
        sock.sendto(message, (UDP_IP, UDP_PORT2))
        sock.sendto(message, (UDP_IP, UDP_PORT3))
        sock.sendto(message, (UDP_IP, UDP_PORT4))
        bkb.write_int(mem,'CONTROL_MESSAGES',0)

    # Used for Telemetry
    message = str(rbt_number) + ' ' # Robot number
    # Localization Variables
    message += str(bkb.read_int(mem,'LOCALIZATION_X')) + ' ' # X Position
    message += str(bkb.read_int(mem,'LOCALIZATION_Y')) + ' ' # Y Position
    message += str(bkb.read_int(mem,'LOCALIZATION_THETA')) + ' ' # THETA Position
    message += str(bkb.read_float(mem,'LOCALIZATION_RBT01_X')) + ' ' # Belief
    message += str(bkb.read_float(mem, 'VISION_BALL_DIST')) + ' ' # Distance Ball's Position
    message += str(bkb.read_float(mem, 'VISION_PAN_DEG')) + ' ' # Angle Ball's Position
    # Flags of Execution
    message += str(bkb.read_int(mem,'CONTROL_WORKING')) + ' ' # Return 1 if Control is working
    bkb.write_int(mem, 'CONTROL_WORKING', 0) # Resets the flag for Control
    message += str(bkb.read_int(mem, 'VISION_WORKING')) + ' ' # Equal previous
    bkb.write_int(mem, 'VISION_WORKING', 0) # Equal previous
    message += str(bkb.read_int(mem, 'LOCALIZATION_WORKING')) + ' ' # Equal previous
    bkb.write_int(mem, 'LOCALIZATION_WORKING', 0) # Equal previous
    message += str(bkb.read_int(mem, 'DECISION_WORKING')) + ' ' # Equal previous
    bkb.write_int(mem, 'DECISION_WORKING', 0) # Equal previous
    message += str(bkb.read_int(mem, 'IMU_WORKING')) + ' ' # Equal previous
    bkb.write_int(mem, 'IMU_WORKING', 0) # Equal previous
    # Other Variables
    message += str(bkb.read_int(mem, 'DECISION_ACTION_A')) + ' ' # Sends the movement the decision is executing.
    message += str(bkb.read_float(mem, 'IMU_EULER_Z')) + ' ' # Sends the orientation of the IMU.
    message += str(bkb.read_int(mem, 'VOLTAGE')) + ' ' # Sends the Voltage on motors.
    message += str(bkb.read_int(mem, 'VISION_LOST')) + ' ' # Lost ball.

    # End of Message
    message += 'OUT'
    # Send the message in broadcast for Telemetry
    sock.sendto(message, (UDP_IP, UDP_PORT_TELE))

    time.sleep(1)
