#coding: utf-8
 # ----------------------------------------------------------------------------
 # ****************************************************************************
 # * @file behavior.py
 # * @author Danilo H Perico
 # * @ROBOFEI-HT - FEI 😛
 # * @created 15/10/2015
 # * @e-mail danilo.perico@gmail.com
 # * @brief robot behaviors
 # ****************************************************************************

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

#looking for the library SharedMemory
import sys
sys.path.append('../../Blackboard/src/')
from SharedMemory import SharedMemory 

import time
from math import degrees

###############################################################################
#set the distance to kick according the robot
#to real robots: 14 centimeters
#to simulated robots: 28 centimeters

distance_to_kick = 40 #real robot
#distance_to_kick = 29 #simulated robot


###############################################################################

class TreatingRawData(object):

    def __init__(self):
        # instantiate:
        self.config = ConfigParser()
    
        # looking for the file config.ini:
        self.config.read('../../Control/Data/config.ini')
        
        self.mem_key = int(self.config.get('Communication', 'no_player_robofei'))*100

        #Instantiate the BlackBoard's class:
        self.bkb = SharedMemory()
        self.mem = self.bkb.shd_constructor(self.mem_key)

        self.flag_move_ac = False        

        print
        print 'Raw data - read (get) and write (set) methods'
        print
        
        #self.bkb.write_int(self.Mem,'VISION_SEARCH_BALL',1)
        
    def get_referee_usage(self):
        return self.config.get('Decision', 'referee')
        
    def get_orientation_usage(self):
        return self.config.get('Decision', 'orientation')
                    
    def get_distance_to_kick(self):
        return self.config.get('Decision', 'distance_to_kick')

    def get_referee(self):
        return self.bkb.read_int(self.mem, 'COM_REFEREE')

    def get_motor_tilt_degrees(self):
        return self.bkb.read_float(self.mem,'VISION_TILT_DEG')
        
    def get_motor_pan_degrees(self):
        return self.bkb.read_float(self.mem,'VISION_PAN_DEG')


    def get_angle_ball(self):
        return self.bkb.read_float(self.mem,'VISION_BALL_ANGLE')
        
    def get_dist_ball(self):
        return self.bkb.read_float(self.mem,'VISION_BALL_DIST')
        
    ''''def get_head_pan_initial(self):
        return self.config.getint('Offset', 'ID_19')

    def get_head_tilt_initial(self):
        return self.config.getint('Offset', 'ID_20')'''

    def get_search_status(self):
        time.sleep(0.1)
        return self.bkb.read_int(self.mem,'VISION_LOST')

        
    def set_vision_search(self):
        return self.bkb.write_int(self.mem,'DECISION_SEARCH_ON', 1)

    def get_orientation(self):
        #print degrees(self.bkb.read_float(self.mem, 'IMU_EULER_Z'))
        #print self.bkb.read_float(self.mem, 'IMU_EULER_Z')
        return degrees(self.bkb.read_float(self.mem, 'IMU_EULER_Z'))
        
    def set_stand_still(self):
        #print 'stand still'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 0)
        #time.sleep(1)

    def set_walk_forward(self):
        print 'walk forward'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 1)
        
    def set_walk_speed(self,vel):
        self.bkb.write_int(self.mem,'DECISION_ACTION_B', vel)
        
    def set_turn_left(self):
        print 'turn left'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 2)
        
    def set_turn_right(self):
        print 'turn right'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 3)
        
    def set_kick_right(self):
        print 'kick right'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 4)
        self.flag_move_ac = True
        
    def set_kick_left(self):
        print 'kick left'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 5)
        self.flag_move_ac = True
        
    def set_sidle_left(self):
        print 'sidle left'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 6)
        
    def set_sidle_right(self):
        print 'sidle right'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 7)
        
    def set_walk_forward_slow(self,vel):
        print 'walk forward slow'
        self.set_walk_speed(vel)
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 8)
        
    def set_revolve_around_ball_clockwise(self):
        print 'revolve around ball - clockwise'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 9)
        #time.sleep(1) #Tempo de Giro

    def set_revolve_around_ball_anticlockwise(self):
        print 'revolve around ball - anticlockwise'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 14)
        #time.sleep(1) #Tempo de Giro
        
    def set_walk_backward(self):
        print 'walk backward'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 10)
        
    def set_gait(self):
        print 'gait'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 11)
        
    def set_pass_left(self):
        print 'pass left'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 12)
        self.flag_move_ac = True
        
    def set_pass_right(self):
        print 'pass right'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 13)
        self.flag_move_ac = True
        
    def set_vision_ball(self):
        self.bkb.write_int(self.mem,'DECISION_ACTION_VISION', 0)
        #return time.sleep(2)

    def set_vision_robot(self):
        self.bkb.write_int(self.mem,'DECISION_ACTION_VISION', 2)
        #return time.sleep(2)

##############################################################################

class Ordinary(TreatingRawData):
    " " " Ordinary class " " "
    
    def __init__(self):
        super(Ordinary,self).__init__()
        print
        print 'Ordinary behavior called'
        print
                
    def decision(self, referee):
        if referee == 1: #stopped
            print 'stand'
            self.set_stand_still()
            
        elif referee == 11: #ready
            print 'ready'
            self.set_stand_still()
            
        elif referee == 12: #set
            print 'set'
            self.set_stand_still()
            self.set_vision_ball()
            
        elif referee == 2: #play
            print 'play'
            self.set_stand_still()
            time.sleep(1)
            self.set_walk_forward_slow(1000)
            time.sleep(30)
            self.set_turn_right()
            time.sleep(5)
            self.set_stand_still()
            time.sleep(10)
            
            if self.get_search_status() == 1: # 1 - vision lost
                print 'vision lost'
                #self.set_stand_still()
                self.set_vision_search()
                self.set_turn_right()
            elif self.get_search_status() == 0: # 0 - object found
                # align to the ball
                if self.get_motor_pan_degrees() > 40 and self.get_motor_pan_degrees() < 160:
                    self.set_turn_left()
                    #self.set_stand_still()
                elif self.get_motor_pan_degrees() < -40 and self.get_motor_pan_degrees() > -160:
                    self.set_turn_right()
                    #self.set_stand_still()
                else:
                    if self.get_dist_ball() < distance_to_kick and self.get_motor_pan_degrees() <= 0:
                        self.set_kick_right()
                    elif self.get_dist_ball() < distance_to_kick and self.get_motor_pan_degrees() > 0:
                        self.set_kick_left()
                    elif self.get_dist_ball() > 50:
                        #self.set_walk_forward()
                        self.set_walk_forward_slow((self.get_dist_ball() / 5))
                    else:
                        self.set_walk_forward_slow((self.get_dist_ball() / 5))
                        # time.sleep(0.5)
                        # self.set_stand_still()        else:
            print 'Invalid argument received from referee!'

            #############################################################################


class Naive(TreatingRawData):
    " " " Naive class " " "

    def __init__(self):
        super(Naive, self).__init__()
        print
        print 'Naive behavior called'
        print

    def decision(self, referee):
        if referee == 1:  # stopped
            print 'stand'
            self.set_stand_still()

        elif referee == 11:  # ready
            print 'ready'
            self.set_stand_still()

        elif referee == 12:  # set
            print 'set'
            self.set_stand_still()
            self.set_vision_ball()

        elif referee == 2:  # play
            if self.get_search_status() == 1: # 1 - vision lost
                print 'vision lost'
                #self.set_stand_still()
                self.set_vision_search()
                self.set_turn_right()
            elif self.get_search_status() == 0: # 0 - object found
                # align to the ball
                if self.get_motor_pan_degrees() > 40 and self.get_motor_pan_degrees() < 160:
                    self.set_turn_left()
                    #self.set_stand_still()
                elif self.get_motor_pan_degrees() < -40 and self.get_motor_pan_degrees() > -160:
                    self.set_turn_right()
                    #self.set_stand_still()
                else:
                    print self.get_motor_pan_degrees()
                    if self.get_dist_ball() < distance_to_kick and self.get_motor_pan_degrees() <= 0:
                        self.set_kick_right()
                    elif self.get_dist_ball() < distance_to_kick and self.get_motor_pan_degrees() > 0:
                        self.set_kick_left()
                    elif self.get_dist_ball() > 50:
                        #self.set_walk_forward()
                        self.set_walk_forward_slow((self.get_dist_ball() / 5))
                    elif self.get_dist_ball() < 50 and self.get_dist_ball() > 20:
                        self.set_walk_forward_slow((self.get_dist_ball() / 5))
                    else:
                        self.set_gait()
                        # time.sleep(0.5)
                        # self.set_stand_still()        
        else:
            print 'Invalid argument received from referee!'

            #############################################################################

class NaiveIMU(TreatingRawData):
    " " " Naive class " " "

    def __init__(self):
        super(NaiveIMU, self).__init__()
        print
        print 'Naive behavior called'
        print
        self.kickoff_ctrl = 0
        #set a far distance to robots
        self.bkb.write_float(self.mem,'DECISION_RBT01_DIST_BALL',999)
        self.bkb.write_float(self.mem,'DECISION_RBT02_DIST_BALL',999)
        self.bkb.write_float(self.mem,'DECISION_RBT03_DIST_BALL',999)
        self.bkb.write_float(self.mem,'DECISION_RBT04_DIST_BALL',999)

    def decision(self, referee):
        if referee == 1:  # stopped
            print 'stand'
            self.set_stand_still()

        elif referee == 11:  # ready
            print 'ready'
            self.set_stand_still()

        elif referee == 12:  # set
            print 'set'
            self.set_stand_still()
            self.set_vision_ball()

        #opponent kickoff               
        elif referee == 21 and self.kickoff_ctrl == 0:
            print 'walking forward for vision to see anything'
            self.set_vision_ball()
            self.set_walk_forward_slow(10)
            for i in range(0,20):
                time.sleep(1)
                print "time", i
            self.kickoff_ctrl = 1
        
        
        elif referee == 2 or (referee == 21 and self.kickoff_ctrl != 0):  # play
            self.bkb.write_int(self.mem,'CONTROL_MESSAGES',0)
            if self.get_search_status() == 1: # 1 - vision lost
                print 'vision lost'
                self.set_stand_still()
                #self.set_vision_search()
                #self.set_turn_right()
            elif self.get_search_status() == 0: # 0 - object found

                ###### this is the beginning of the strategy: the closest robot goes to the ball: ###################
                #it reads and shares the distance from all robots
                #it compares who is the closest to the ball and it sets as coordinator.
                print 'robot number: ', self.bkb.read_int(self.mem,'ROBOT_NUMBER')

                self.bkb.write_floatDynamic(self.mem,'DECISION_RBT01_DIST_BALL',self.bkb.read_int(self.mem,'ROBOT_NUMBER')-1,self.get_dist_ball())

                self.bkb.write_int(self.mem,'CONTROL_MESSAGES',2)

                print 'dist Robot 1: ',self.bkb.read_float(self.mem,'DECISION_RBT01_DIST_BALL')
                print 'dist Robot 2: ',self.bkb.read_float(self.mem,'DECISION_RBT02_DIST_BALL')
                print 'dist Robot 3: ',self.bkb.read_float(self.mem,'DECISION_RBT03_DIST_BALL')
                print 'dist Robot 4: ',self.bkb.read_float(self.mem,'DECISION_RBT04_DIST_BALL')

                if self.bkb.read_float(self.mem,'DECISION_RBT01_DIST_BALL') < self.bkb.read_float(self.mem,'DECISION_RBT02_DIST_BALL') and self.bkb.read_float(self.mem,'DECISION_RBT01_DIST_BALL') < self.bkb.read_float(self.mem,'DECISION_RBT03_DIST_BALL') and self.bkb.read_float(self.mem,'DECISION_RBT01_DIST_BALL') < self.bkb.read_float(self.mem,'DECISION_RBT04_DIST_BALL'):
                    self.bkb.write_float(self.mem,'CBR_COORDINATOR',1)
                elif self.bkb.read_float(self.mem,'DECISION_RBT02_DIST_BALL') < self.bkb.read_float(self.mem,'DECISION_RBT01_DIST_BALL') and self.bkb.read_float(self.mem,'DECISION_RBT02_DIST_BALL') < self.bkb.read_float(self.mem,'DECISION_RBT03_DIST_BALL') and self.bkb.read_float(self.mem,'DECISION_RBT02_DIST_BALL') < self.bkb.read_float(self.mem,'DECISION_RBT04_DIST_BALL'):
                    self.bkb.write_float(self.mem,'CBR_COORDINATOR',2)
                elif self.bkb.read_float(self.mem,'DECISION_RBT03_DIST_BALL') < self.bkb.read_float(self.mem,'DECISION_RBT02_DIST_BALL') and self.bkb.read_float(self.mem,'DECISION_RBT03_DIST_BALL') < self.bkb.read_float(self.mem,'DECISION_RBT01_DIST_BALL') and self.bkb.read_float(self.mem,'DECISION_RBT03_DIST_BALL') < self.bkb.read_float(self.mem,'DECISION_RBT04_DIST_BALL'):
                    self.bkb.write_float(self.mem,'CBR_COORDINATOR',3)
                elif self.bkb.read_float(self.mem,'DECISION_RBT04_DIST_BALL') < self.bkb.read_float(self.mem,'DECISION_RBT02_DIST_BALL') and self.bkb.read_float(self.mem,'DECISION_RBT04_DIST_BALL') < self.bkb.read_float(self.mem,'DECISION_RBT03_DIST_BALL') and self.bkb.read_float(self.mem,'DECISION_RBT04_DIST_BALL') < self.bkb.read_float(self.mem,'DECISION_RBT01_DIST_BALL'):
                    self.bkb.write_float(self.mem,'CBR_COORDINATOR',4)
                else:
                    self.bkb.write_float(self.mem,'CBR_COORDINATOR',float(self.bkb.read_int(self.mem,'ROBOT_NUMBER')))

                print 'robot_coordinator: ', self.bkb.read_float(self.mem,'CBR_COORDINATOR')

                if  int(self.bkb.read_float(self.mem,'CBR_COORDINATOR')) == self.bkb.read_int(self.mem,'ROBOT_NUMBER'):

                    #print 'dist_ball', self.get_dist_ball()
                    print 'orientation', self.get_orientation()
                    
                    #NOT KICK TWICE
                    if self.bkb.read_int(self.mem,'DECISION_ACTION_A') == 4 or self.bkb.read_int(self.mem,'DECISION_ACTION_A') == 5:
                        self.set_stand_still()

                    if self.get_search_status() == 1: # 1 - vision lost
                        print 'vision lost'
                        self.set_stand_still()
                        #self.set_vision_search()
                        #self.set_turn_right()
                    elif self.get_search_status() == 0: # 0 - object found
                        # align to the ball
                        if self.get_motor_pan_degrees() > 20 and self.get_motor_pan_degrees() < 160:
                            self.set_turn_left()
                            #self.set_stand_still()
                        elif self.get_motor_pan_degrees() < -20 and self.get_motor_pan_degrees() > -160:
                            self.set_turn_right()
                            #self.set_stand_still()
                        else:

                            if self.get_dist_ball() < distance_to_kick and self.get_motor_pan_degrees() <= 0:
                                if self.get_orientation() <= 90 and self.get_orientation() >= -90:
                                    self.set_kick_right()
                                elif self.get_orientation() > 90:
                                    #revolve_clockwise:
                                    self.set_pass_right()
                                    #########
                                elif self.get_orientation() < -90:
                                    #revolve_anticlockwise:
                                    self.set_pass_left()
                                    #########
                            elif self.get_dist_ball() < distance_to_kick and self.get_motor_pan_degrees() > 0:
                                if self.get_orientation() <= 90 and self.get_orientation() >= -90:
                                    self.set_kick_left()
                                elif self.get_orientation() > 90:
                                    #revolve_clockwise:
                                    self.set_pass_right()
                                    #########
                                elif self.get_orientation() < -90:
                                    #revolve_anticlockwise:
                                    self.set_pass_left()
                                    #########
                            elif self.get_dist_ball() > 60:
                                #self.set_walk_forward()
                                self.set_walk_forward_slow((self.get_dist_ball() / 5))
                            #elif self.get_dist_ball() <= 26:
                            #    self.set_stand_still()
                            else:
                                self.set_walk_forward_slow((self.get_dist_ball() / 6))
                                
                                # time.sleep(0.5)
                                # self.set_stand_still()
                else:
                    print 'Invalid argument received from referee!'
                    print referee

#############################################################################

class NaiveIMUDecTurning(TreatingRawData):
    " " " Naive class " " "

    def __init__(self):
        super(NaiveIMUDecTurning, self).__init__()
        print
        print 'Naive behavior called with IMU and turning'
        print
        self.kickoff_ctrl = 0

    def decision(self, referee):
    
        print self.get_motor_pan_degrees()
    
        if referee == 1:  # stopped
            print 'stand'
            self.set_stand_still()

        elif referee == 11:  # ready
            print 'ready'
            self.set_stand_still()

        elif referee == 12:  # set
            print 'set'
            self.set_stand_still()
            self.set_vision_ball()
            
       # elif referee == 21 and self.kickoff_ctrl == 0:
       #     print 'walking forward for vision to see anything'
       #     self.set_vision_ball()
       #     self.set_walk_forward_slow(10)
       #     for i in range(0,20):
       #         time.sleep(1)
       #         print "time", i
       #     self.kickoff_ctrl = 1
       
        elif referee == 2 and self.kickoff_ctrl == 0 and self.get_search_status() == 1:
            print 'walking forward in order to see anything'
            self.set_vision_ball()
            self.set_walk_forward_slow(10)
            for i in range(0,20):
                time.sleep(1)
                print "Counting...", i
            self.kickoff_ctrl = 1
        
        
       # elif referee == 2 or (referee == 21 and self.kickoff_ctrl != 0):  # play
        elif referee == 2:  # play
            self.kickoff_ctrl = 1
            #print 'dist_ball', self.get_dist_ball()
            print 'orientation', self.get_orientation()
            
            self.set_walk_forward_slow(1000)
            time.sleep(22)
            self.set_turn_left()
            time.sleep(7)
            self.set_stand_still()
            
            #do not kick twice - it is not funcionning!!
#            if self.bkb.read_int(self.mem,'DECISION_ACTION_A') == 4 or self.bkb.read_int(self.mem,'DECISION_ACTION_A') == 5:
#		print 'nao chutei pq to aqui!'
#                self.set_stand_still()
            if self.bkb.read_int(self.mem, 'CONTROL_MOVING') == 1 and self.flag_move_ac==True:
                self.bkb.write_int(self.mem, 'DECISION_ACTION_A', 0) # Writing in the memory
                self.flag_move_ac=False
                    
            if self.get_search_status() == 1: # 1 - vision lost
                print 'vision lost'
                self.set_stand_still()
                #self.set_vision_search()
                #self.set_turn_right()
            elif self.get_search_status() == 0: # 0 - object found
                # align to the ball
                if self.get_motor_pan_degrees() > 20 and self.get_motor_pan_degrees() < 160:
                    self.set_turn_left()
                    #self.set_stand_still()
                elif self.get_motor_pan_degrees() < -20 and self.get_motor_pan_degrees() > -160:
                    self.set_turn_right()
                    #self.set_stand_still()
                else:

                    if self.get_dist_ball() < distance_to_kick and self.get_motor_pan_degrees() <= 0:
                        if self.get_orientation() <= 40 and self.get_orientation() >= -40:
                            self.set_kick_right()
                        elif self.get_orientation() > 40:
                            #revolve_clockwise:
                            self.set_pass_right()
                            #########
                        elif self.get_orientation() < -40:
                            #revolve_anticlockwise:
                            self.set_pass_left()
                            #########
                    elif self.get_dist_ball() < distance_to_kick and self.get_motor_pan_degrees() > 0:
                        if self.get_orientation() <= 40 and self.get_orientation() >= -40:
                            self.set_kick_left()
                        elif self.get_orientation() > 40:
                            #revolve_clockwise:
                            self.set_pass_right()
                            #########
                        elif self.get_orientation() < -40:
                            #revolve_anticlockwise:
                            self.set_pass_left()
                            #########
                    elif self.get_dist_ball() > 60:
                        #self.set_walk_forward()
                        self.set_walk_forward_slow((self.get_dist_ball() / 5))
                    #elif self.get_dist_ball() <= 26:
                    #    self.set_stand_still()
                    else:
                        self.set_walk_forward_slow((self.get_dist_ball() / 6))
                        
                        # time.sleep(0.5)
                        # self.set_stand_still()
        else:
            print 'Invalid argument received from referee!'
            print referee

#############################################################################


class Attacker(TreatingRawData):
    " " " Attacker class " " "

    def __init__(self):
        super(Attacker,self).__init__()
        print
        print  'Attacker behavior called' 
        print
        
    def decision(self, referee):
        if referee == 1: #stopped
            print 'stand'
            self.set_stand_still()
            
        elif referee == 11: #ready
            print 'ready'
            self.set_stand_still()
            time.sleep(3)
            
        elif referee == 12: #set
            print 'set'
            self.set_stand_still()
            self.set_vision_ball()
            
        elif referee == 2: #play
            print 'play'
            self.set_walk_forward_slow()



##############################################################################
        
class Quarterback(Ordinary):
    " " " Quarterback class " " "

    def __init__(self):
        print
        print  'Quarterback behavior called' 
        print
        
##############################################################################
        
class Golie(Ordinary):
    " " " Golie class " " "

    def __init__(self):
        print
        print  'Golie behavior called' 
        print
        
