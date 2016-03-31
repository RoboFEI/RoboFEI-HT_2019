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

        
        print
        print 'Raw data - read (get) and write (set) methods'
        print
        
        #self.bkb.write_int(self.Mem,'VISION_SEARCH_BALL',1)
        
    def get_referee_usage(self):
        return self.config.get('Decision', 'referee')
        
    def get_orientation_usage(self):
        return self.config.get('Decision', 'orientation')
                    
    def get_referee(self):
        return self.bkb.read_int(self.mem, 'COM_REFEREE')

    def get_motor_tilt_degrees(self):
        return self.bkb.read_float(self.mem,'VISION_TILT_DEG')
        
    def get_motor_pan_degrees(self):
        return self.bkb.read_float(self.mem,'VISION_PAN_DEG')
          
    def get_orientation(self):
        '''1 for correct orientation'''
        return self.bkb.read_int(self.mem,'LOCALIZATION_THETA')

    def get_angle_ball(self):
        return self.bkb.read_float(self.mem,'VISION_ANGLE_BALL')
        
    def get_dist_ball(self):
        return self.bkb.read_float(self.mem,'VISION_BALL_DIST')
        
    ''''def get_head_pan_initial(self):
        return self.config.getint('Offset', 'ID_19')

    def get_head_tilt_initial(self):
        return self.config.getint('Offset', 'ID_20')'''
        
    def get_search_ball_status(self):
        return self.bkb.read_int(self.mem,'VISION_BALL_PAN_ON')
        
    def get_lost_ball_status(self):
        return self.bkb.read_int(self.mem,'VISION_BALL_LOST')
        
    def set_search_ball_status(self):
        return self.bkb.write_int(self.mem,'VISION_BALL_PAN_ON', 1)
        
    def set_stand_still(self):
        print 'stand still'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 0)
        time.sleep(1)
        return 

    def set_walk_forward(self):
        print 'walk forward'
        return self.bkb.write_int(self.mem,'DECISION_ACTION_A', 1)
        
    def set_walk_speed(self,vel):
        return self.bkb.write_int(self.mem,'DECISION_ACTION_B', vel)
        
    def set_turn_left(self):
        print 'turn left'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 2)
        return time.sleep(1)
        
    def set_turn_right(self):
        print 'turn right'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 3)
        return time.sleep(1)
        
    def set_kick_right(self):
        print 'kick right'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 4)
        return self.set_search_ball_status()
        
    def set_kick_left(self):
        print 'kick left'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 5)
        return self.set_search_ball_status()
        
    def set_sidle_left(self):
        print 'sidle left'
        return self.bkb.write_int(self.mem,'DECISION_ACTION_A', 6)
        
    def set_sidle_right(self):
        print 'sidle right'
        return self.bkb.write_int(self.mem,'DECISION_ACTION_A', 7)
        
    def set_walk_forward_slow(self):
        print 'walk forward slow'
        self.set_walk_speed(3)
        return self.bkb.write_int(self.mem,'DECISION_ACTION_A', 8)
        
    def set_revolve_around_ball(self):
        print 'revolve around ball'
        self.bkb.write_int(self.mem,'DECISION_ACTION_A', 9)
        time.sleep(7) #Tempo de Giro
        return self.set_stand_still()
        
    def set_walk_backward(self):
        print 'walk backward'
        return self.bkb.write_int(self.mem,'DECISION_ACTION_A', 10)
        
    def set_gait(self):
        print 'gait'
        return self.bkb.write_int(self.mem,'DECISION_ACTION_A', 11)
        
    def set_pass_left(self):
        print 'pass left'
        return self.bkb.write_int(self.mem,'DECISION_ACTION_A', 12)
        
    def set_pass_right(self):
        print 'pass right'
        return self.bkb.write_int(self.mem,'DECISION_ACTION_A', 13)
        
    def set_jump_left(self):
        return self.bkb.write_int(self.mem,'DECISION_ACTION_A', 14)

    def set_jump_right(self):
        return self.bkb.write_int(self.mem,'DECISION_ACTION_A', 15)
        
    def set_vision_ball(self):
        self.bkb.write_int(self.mem,'DECISION_ACTION_VISION', 0)
        self.bkb.write_int(self.mem,'VISION_BALL_PAN_ON', 1)
        self.bkb.write_int(self.mem,'VISION_BALL_LOST', 1)
        return time.sleep(2)
        
    def set_vision_orientation(self):
        print "orientating"
        self.set_stand_still()
        self.bkb.write_int(self.mem,'LOCALIZATION_THETA', 0)
        self.bkb.write_int(self.mem,'DECISION_ACTION_VISION', 2)
        while(self.get_orientation() == 0):
            pass
        return self.bkb.write_int(self.mem,'DECISION_ACTION_VISION', 0)
        
    def delta_position_pan(self):
        '''right > 0 / left < 0'''
        return self.get_head_pan_initial() - self.get_motor_pan()

    def delta_position_tilt(self):
        '''up > 0 / down < 0 / middle is looking for the horizon'''
        return self.get_head_tilt_initial() - self.get_motor_tilt()

        
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
            self.set_vision_ball() #set vision to find ball
            print 'search ball: ',self.get_search_ball_status()
            print 'lost ball: ',self.get_lost_ball_status()

            if self.get_search_ball_status() == 1: #1 - searching ball
                if self.get_lost_ball_status() == 1: #1 - lost ball
                    self.set_turn_right()
                self.set_stand_still()
            else:
                if (self.get_lost_ball_status() == 0) and (self.get_search_ball_status() == 0): #1 - ball is found
                    #align to the ball
                    print 'angle ', self.get_motor_pan_degrees()
                    if self.get_motor_pan_degrees() > 20 and self.get_motor_pan_degrees() < 160:
                        self.set_turn_left()
                        self.set_stand_still()
                    elif self.get_motor_pan_degrees() < -20 and self.get_motor_pan_degrees() > -160:
                        self.set_turn_right()
                        self.set_stand_still()
                    else:
                        print 'Distance: ', self.get_dist_ball()
                        if self.get_dist_ball() < 29 and self.get_motor_pan_degrees()<=0:
                            self.set_kick_right()
                        elif self.get_dist_ball() < 29 and self.get_motor_pan_degrees()>0:
                            self.set_kick_left()
                        elif self.get_dist_ball() > 80:
                            self.set_walk_forward()
                        else:
                            self.set_walk_forward_slow()
                            time.sleep(1)
                            self.set_stand_still()
        else:
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
            print 'play'
            self.set_vision_ball()  # set vision to find ball
            print 'search ball: ', self.get_search_ball_status()
            print 'lost ball: ', self.get_lost_ball_status()

            if self.get_search_ball_status() == 1:  # 1 - searching ball
                if self.get_lost_ball_status() == 1:  # 1 - lost ball
                    self.set_turn_right()
                self.set_stand_still()
            else:
                if (self.get_lost_ball_status() == 0) and (
                    self.get_search_ball_status() == 0):  # 0 - ball is found
                    # align to the ball
                    print 'angle ', self.get_motor_pan_degrees()
                    if self.get_motor_pan_degrees() > 20 and self.get_motor_pan_degrees() < 160:
                        self.set_turn_left()
                        self.set_stand_still()
                    elif self.get_motor_pan_degrees() < -20 and self.get_motor_pan_degrees() > -160:
                        self.set_turn_right()
                        self.set_stand_still()
                    else:
                        print 'Distance: ', self.get_dist_ball()
                        if self.get_dist_ball() < 29 and self.get_motor_pan_degrees() <= 0:
                            self.set_kick_right()
                        elif self.get_dist_ball() < 29 and self.get_motor_pan_degrees() > 0:
                            self.set_kick_left()
                        elif self.get_dist_ball() > 80:
                            self.set_walk_forward()
                        else:
                            self.set_walk_forward_slow()
                            time.sleep(0.5)
                            self.set_stand_still()
        else:
            print 'Invalid argument received from referee!'

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
        
