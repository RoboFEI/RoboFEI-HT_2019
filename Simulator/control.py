from screen import *
import pygame
from robot import *
from ball import *

class CONTROL():
    def __init__(self, robot):
        self.robot = robot

        self.bkb = robot.bkb
        self.Mem = robot.Mem

        # Config
        self.walk_speed = 0.015
        self.drift_speed = 0.01
        self.turn_speed = 0.015 # Degrees

        # Actions
        self.action_array = {   0: "Stop",\
                                11: "Gait",\
                                1: "Fast walk forward",\
                                8: "Slow walk forward",\
                                17: "Fast walk backward",\
                                18: "Slow walk backward",\
                                6: "Walk left",\
                                7: "Walk right",\
                                2: "Turn left",\
                                3: "Turn right",\
                                9: "Turn left around the ball",\
                                14: "Turn right around the ball",\
                                5: "Left kick",\
                                4: "Right kick",\
                                12: "Pass to the left",\
                                13: "Pass to the right"}

        self.action_vars = {
            0: (0, 0, 0),\
            11: (0, 0, 0),\
            1: (self.walk_speed * self.robot.fast_walk_speed, 0, 0),\
            8: (self.walk_speed * self.robot.slow_walk_speed, 0, 0),\
            17: (- self.walk_speed * self.robot.fast_walk_speed, 0, 0),\
            18: (- self.walk_speed * self.robot.slow_walk_speed, 0, 0),\
            6: (0, 0, self.drift_speed * self.robot.drift_speed),\
            7: (0, 0, - self.drift_speed * self.robot.drift_speed),\
            2: (0, self.turn_speed * self.robot.turn_angle, 0),\
            3: (0, - self.turn_speed * self.robot.turn_angle, 0),\
            9: (0, - self.turn_speed * self.robot.turn_angle, self.drift_speed * self.robot.drift_turn_speed),\
            14: (0, self.turn_speed * self.robot.turn_angle, - self.drift_speed * self.robot.drift_turn_speed)
        }

        self.action_flag = 0
        self.action_state = self.action_array[self.action_flag]
        self.action_exceptions = (0, 4, 5, 12, 13)


    def action_select(self, flag):
        self.action_flag = flag
        self.action_state = self.action_array[self.action_flag]

        #  print self.action_state

        self.bkb.write_int(self.Mem, 'CONTROL_MOVING', 1)

        if flag in self.action_exceptions:
            if flag == 4:
                self.robot.right_kick()
            elif flag == 5:
                self.robot.left_kick()
            elif flag == 12:
                self.robot.pass_left()
            elif flag == 13:
                self.robot.pass_right()
            elif flag == 0:
                self.robot.in_motion = False
                self.robot.motion_vars(self.action_vars[flag][0],
                                       self.action_vars[flag][1],
                                       self.action_vars[flag][2])
                self.bkb.write_int(self.Mem, 'CONTROL_MOVING', 0)
                self.bkb.write_int(self.Mem, 'DECISION_ACTION_A', 0)
        else:
            self.robot.in_motion = True
            t = True

            if flag == 8:
                self.robot.in_motion = True
                SPEED = self.bkb.read_int(self.Mem, 'DECISION_ACTION_B')
                
                if SPEED < self.robot.slow_walk_speed:
                    self.robot.motion_vars(self.walk_speed * SPEED,
                                           self.action_vars[flag][1],
                                           self.action_vars[flag][2])
                    t = False

            if t:
                self.robot.motion_vars(self.action_vars[flag][0],
                                       self.action_vars[flag][1],
                                       self.action_vars[flag][2])


    def control_update(self):
        self.bkb.write_float(self.Mem, 'IMU_EULER_Z', radians(self.robot.get_orientation()))
        aux = self.bkb.read_int(self.Mem, 'DECISION_ACTION_A')
        if aux == 2:
            self.bkb.write_int(self.Mem, 'CONTROL_ACTION', 3)
        elif aux == 3:
            self.bkb.write_int(self.Mem, 'CONTROL_ACTION', 2)
        else:
            self.bkb.write_int(self.Mem, 'CONTROL_ACTION', aux)
        self.bkb.write_int(self.Mem, 'VOLTAGE', 189)
        self.bkb.write_int(self.Mem, 'CONTROL_WORKING', 1)
        self.bkb.write_int(self.Mem, 'IMU_WORKING', 1)
        # self.bkb.write_int(self.Mem, 'DECISION_WORKING', 1)
        # self.bkb.write_int(self.Mem, 'VISION_WORKING', 1)
        
        if self.action_flag in self.action_exceptions:
            if self.action_flag == 0:
                self.action_select(self.bkb.read_int(self.Mem, 'DECISION_ACTION_A'))
        else:
            flag = self.bkb.read_int(self.Mem, 'DECISION_ACTION_A')
            if flag != self.action_flag:
                self.action_select(flag)