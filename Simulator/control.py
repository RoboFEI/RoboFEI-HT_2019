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
        self.walk_speed = 0.3
        self.drift_speed = 0.2
        self.turn_speed = 0.3 # Degrees

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
                1: (2*self.walk_speed, 0, 0),\
                8: (self.walk_speed, 0, 0),\
                17: (-2*self.walk_speed, 0, 0),\
                18: (-self.walk_speed, 0, 0),\
                6: (0, 0, self.drift_speed),\
                7: (0, 0, -self.drift_speed),\
                2: (0, self.turn_speed, 0),\
                3: (0, -self.turn_speed, 0),\
                9: (0, -self.turn_speed, 0.9*self.drift_speed),\
                14: (0, self.turn_speed, -0.9*self.drift_speed)
        }

        self.action_flag = 0
        self.action_state = self.action_array[self.action_flag]
        self.action_exceptions = (0, 4, 5, 12, 13)

    def action_select(self, flag):
        self.action_flag = flag
        self.action_state = self.action_array[self.action_flag]

        #print self.action_state

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
        else:
            self.robot.in_motion = True
            self.robot.motion_vars(self.action_vars[flag][0],
                                   self.action_vars[flag][1],
                                   self.action_vars[flag][2])

    def control_update(self):

        self.bkb.write_float(self.Mem, 'IMU_EULER_Z',self.robot.get_orientation())

        if self.action_flag in self.action_exceptions:
            if self.action_flag == 0:
                self.action_select(self.bkb.read_int(self.Mem, 'DECISION_ACTION_A'))
        else:
            flag = self.bkb.read_int(self.Mem, 'DECISION_ACTION_A')
            if flag != self.action_flag:
                self.action_select(flag)
