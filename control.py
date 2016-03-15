from screen import *
import pygame
from robot import *
from ball import *
from math import cos
from math import sin
from math import radians
from math import sqrt
from math import atan2
from math import pi
from math import exp
from random import gauss

class CONTROL():
    def __init__(self, robot):
        self.robot = robot

        # Config
        self.walk_speed = 0.3
        self.drift_speed = 0.2
        self.turn_speed = 0.3 # Degrees

        # Errors - TODO
        self.errors_on = False # error_variance should not be 0
        self.walk_error_mean = 0
        self.walk_error_variance = 0
        self.drift_error_mean = 0
        self.drift_error_variance = 0
        self.turn_error_mean = 0
        self.turn_error_variance = 0

        # IMU - TODO
        self.orientation = 0
        self.imu_error_mean = 0
        self.imu_error_variance = 0

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

        if self.errors_on:
            self.action_errors = (gauss(self.walk_error_mean, self.walk_error_variance),
                                  gauss(self.turn_error_mean, self.turn_error_variance),
                                  gauss(self.drift_error_mean, self.drift_error_variance))
        else:
            self.action_errors = (0, 0, 0)

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
        self.action_exceptions = (4, 5, 12, 13)



    def action_select(self, flag):
        self.action_flag = flag
        self.action_state = self.action_array[self.action_flag]

        print self.action_state

        if flag in self.action_exceptions:
            pass
        else:
            walk_speed = self.action_errors[0] + self.action_vars[flag][0]
            turn_speed = self.action_errors[1] + self.action_vars[flag][1]
            drift_speed = self.action_errors[2] + self.action_vars[flag][2]
            self.robot.motion_vars(walk_speed, turn_speed, drift_speed)