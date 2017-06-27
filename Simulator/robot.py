from screen import *
from control import *
from vision import *
from vision_loc import *
import pygame
from math import cos
from math import sin
from math import radians
from math import degrees
from math import sqrt
from math import atan2
from math import exp
from random import gauss

import sys
sys.path.append('../AI/Blackboard/src/')
from SharedMemory import SharedMemory


class Robot(pygame.sprite.Sprite,Vision):
    def __init__(self, x, y, theta, KEY, color):
        pygame.sprite.Sprite.__init__(self)
        Vision.__init__(self)
        self.x = x
        self.y = y
        self.rotate = theta
        self.KEY = KEY
        self.color = color
        self.new_x = x
        self.new_y = y
        self.robot_width = 26
        self.robot_height = 26
        self.radius = 13
        self.index = 0

        self.front = 0
        self.turn = 0
        self.drift = 0
        self.in_motion = False
        self.collision = False
        self.image = pygame.Surface([self.robot_width, self.robot_height])
        self.rect = self.image.get_rect()
        #self.saved_image = self.image
        self.front = 0
        self.rect.x = x
        self.rect.y = y
        self.sum_time = 0
        self.old_x = x
        self.old_y = y

        self.view_rot = theta

        self.bkb = SharedMemory()

        self.Mem = self.bkb.shd_constructor(KEY)
        print 'Shared Memory successfully created as ',KEY
        #TODO remover a linha vision_search_ball.... como nao estou utilizando decisao ainda, estou forcando a busca..
        self.bkb.write_int(self.Mem,'DECISION_SEARCH_ON',1)
        #TODO instanciar a classe visao passando o blackboard


        self.fast_walk_speed = 20
        self.slow_walk_speed = 10
        self.turn_angle = 10
        self.drift_speed = 20
        self.drift_turn_speed = 15

        self.control = CONTROL(self)
        self.vision = VISION(self)
        self.ball = None

        # Errors
        # Mean = 0 for symmetrical errors
        # Variances should not be 0
        self.errors_on = False # Turn errors on and off!
        self.walk_error_mean = 0
        self.walk_error_variance = 0
        self.drift_error_mean = 0
        self.drift_error_variance = 0
        self.turn_error_mean = 0
        self.turn_error_variance = 0

        self.kick_error_angle_mean = 0
        self.kick_error_angle_variance = 0
        self.kick_error_force_mean = 0
        self.kick_error_force_variance = 0

        # IMU
        self.imu_error_mean = 0
        self.imu_error_variance = 0
        self.orientation_error = 0
        self.imu_initial_value = 0

        #EOPRA // StarVars
        self.delta_eopra = 100 # 1 meter
        self.m = 8 # 4 // 6 // 8

    def draw_robot(self,robot_index, screen):
        self.image.fill(screen.GREEN)
        self.image.set_colorkey(screen.GREEN)

        self.rect.x = self.x - 13
        self.rect.y = self.y - 13

        #robot's body
        pygame.draw.rect(self.image, self.color, (3, 0, 16, 26), 0)

        #feet
        pygame.draw.rect(self.image, screen.BLACK, (19, 2, 5, 10), 0)
        pygame.draw.rect(self.image, screen.BLACK, (19, 14, 5, 10), 0)

        #sum time between frames
        self.sum_time = (screen.clock.get_time() + self.sum_time) % 500

        #feet movement while walking
        if self.control.action_flag != 0:
            if self.sum_time < 250:
                pygame.draw.rect(self.image, screen.BLACK, (19, 1, 6, 12), 0)
                pygame.draw.rect(self.image, screen.BLACK, (19, 14, 5, 10), 0)
            else:
                pygame.draw.rect(self.image, screen.BLACK, (19, 2, 5, 10), 0)
                pygame.draw.rect(self.image, screen.BLACK, (19, 13, 6, 12), 0)

        image2 = pygame.transform.rotate(self.image, self.rotate)

        #fix rotation to the center
        rot_rect = image2.get_rect(center=self.rect.center)

        #show
        screen.background.blit(image2, (rot_rect))

        #text
        font = pygame.font.SysFont("Arial", 15)
        self.index = robot_index + 1
        robot_name = "B" + str(self.index)
        text = font.render(robot_name, 1, (10, 10, 10))
        textpos = (self.x - 5, self.y - 40)
        screen.background.blit(text, textpos)

        self.vision.draw(screen.background)

    '''Control'''

    def motion_vars(self, front, rotate, drift):
        self.front = front
        self.turn = rotate
        self.drift = drift

    def set_errors(self, walk_err_mean=0, walk_err_var=0,
                   turn_err_mean=0, turn_err_var=0,
                   drift_err_mean=0, drift_err_var=0,
                   kick_ang_err_mean=0, kick_ang_err_var=0,
                   kick_force_err_mean=0, kick_force_err_var=0,
                   imu_err_mean = 0, imu_err_var = 0):

        self.errors_on = True
        self.walk_error_mean = walk_err_mean
        self.walk_error_variance = walk_err_var
        self.turn_error_mean = turn_err_mean
        self.turn_error_variance = turn_err_var
        self.drift_error_mean = drift_err_mean
        self.drift_error_variance = drift_err_var
        self.kick_error_angle_mean = kick_ang_err_mean
        self.kick_error_angle_variance = kick_ang_err_var
        self.kick_error_force_mean = kick_force_err_mean
        self.kick_error_force_variance = kick_force_err_var
        self.imu_error_mean = imu_err_mean
        self.imu_error_variance = imu_err_var

    def motion_model(self, lines, goals, robots):
        turn = self.turn
        if self.errors_on and self.in_motion:
            turn += gauss(self.turn_error_mean, self.turn_error_variance)

        front = self.front
        if self.errors_on and self.in_motion:
            front += gauss(self.walk_error_mean, self.walk_error_variance)

        drift = self.drift
        if self.errors_on and self.in_motion:
            drift += gauss(self.drift_error_mean, self.drift_error_variance)

        self.rotate = (self.rotate + turn) % 360
        self.view_rot = (self.view_rot + turn) % 360

        self.x += cos(radians(self.rotate)) * front
        self.y -= sin(radians(self.rotate)) * front

        self.x -= sin(radians(self.rotate)) * drift
        self.y -= cos(radians(self.rotate)) * drift

        for line in lines:
            x, y = collision_robot_vs_line(self, line)
            self.x += x
            self.y += y

        for goal in goals:
            x, y = collision_robot_vs_goal(self, goal)
            self.x += x
            self.y += y

        for robot in robots:
            if robot.KEY != self.KEY:
                x, y = collision_robot_vs_robot(self, robot)
                self.x += x
                self.y += y

        collision_robot_vs_ball(self, self.ball)
        self.get_orientation()  # cumulative error

    def get_orientation(self):
        if self.errors_on:
            error = gauss(self.imu_error_mean, self.imu_error_variance)
            self.orientation_error += error
        if self.imu_initial_value == 0:
            if self.rotate > 180:
                return (self.rotate - 360) + self.orientation_error
            else:
                return self.rotate + self.orientation_error
        elif self.imu_initial_value == 180:
            return (self.rotate - 180) + self.orientation_error

    def right_kick(self):
        self.Kick(5, 30)

    def left_kick(self):
        self.Kick(30, 5)

    def pass_left(self):
        self.Kick(30, 30, 90, 8) #leftlimit, rightlimit, direction, force = 1 to 12

    def pass_right(self):
        self.Kick(30, 30, -90, 8) #leftlimit, rightlimit, direction, force 1 to 12

    def Kick(self, LeftLimit, RightLimit, Direction=0, force_limit = 12):
        R = degrees(atan2((self.y - self.ball.y), (self.ball.x - self.x)))
        d = sqrt((self.x - self.ball.x) ** 2 + (self.y - self.ball.y) ** 2)
        force = min(10, force_limit * exp(-((self.radius - d) ** 2) / (force_limit) ** 2))

        r = R
        if R < 0: r = R + 360

        if self.rotate > 360 - LeftLimit and (
                r > self.rotate - RightLimit or r < self.rotate - 360 + LeftLimit) or self.rotate < RightLimit and (
                r > 360 - RightLimit + self.rotate or r < self.rotate + LeftLimit) or r > self.rotate - RightLimit and r < self.rotate + LeftLimit:
            if self.errors_on:
                self.ball.put_in_motion(force + gauss(self.kick_error_force_mean, self.kick_error_force_variance),
                                        self.rotate + Direction + gauss(self.kick_error_angle_mean,
                                                                        self.kick_error_angle_variance))
            else:
                self.ball.put_in_motion(force, self.rotate + Direction)

        self.control.action_select(0)

    '''Vision'''

    def toRectangular(self,point):
        r = point[0]
        a = point[1]
        return (r * cos(a), r * sin(a))


    def draw_vision(self,screen):
        #print '********************************************* ',self.view_rot
        vision_dist = self.vision_dist
        field_of_view = self.field_of_view
        startRad = radians(-35 + self.view_rot)
        endRad = radians(35 + self.view_rot)


        vision_surface = pygame.Surface((vision_dist * 2, vision_dist * 2))
        vision_surface.fill(screen.GREEN)
        vision_surface.set_colorkey(screen.GREEN)
        vision_surface.set_alpha(200)
        vision_surface_center = (vision_dist, vision_dist)


       # if self.view_rot < 0:
       #     self.view_rot = self.view % 360

        #if self.view_rot > (self.rotate + 90):
        #    self.view_rot = self.rotate + 90

        #elif self.view_rot < (self.rotate - 90):
        #    self.view_rot = self.rotate - 90


        theta_vision = radians(self.view_rot)

        angle_1 = -theta_vision + field_of_view/2
        angle_2 = -theta_vision - field_of_view/2

        point_1 = (vision_dist, angle_1)
        point_2 = (vision_dist, angle_2)

        point_1 = self.toRectangular(point_1)
        point_2 = self.toRectangular(point_2)

        point_1 = (point_1[0] + vision_surface_center[0], point_1[1] + vision_surface_center[1])
        point_2 = (point_2[0] + vision_surface_center[0], point_2[1] + vision_surface_center[1])


        pygame.draw.arc(screen.background, screen.WHITE,[self.x - vision_dist, self.y - vision_dist, vision_dist * 2, vision_dist * 2], startRad,endRad, 1)
        pygame.draw.arc(screen.background, screen.WHITE, [self.x - vision_dist/2, self.y - vision_dist/2, vision_dist, vision_dist], startRad, endRad, 1)

        pygame.draw.line(vision_surface, screen.WHITE, vision_surface_center, point_1, 1)
        pygame.draw.line(vision_surface, screen.WHITE, vision_surface_center, point_2, 1)


        position = (
            self.x - vision_dist,
            self.y - vision_dist
        )

        screen.background.blit(vision_surface, position)


    def ball_search(self,x,y):
        self.ball.view_obj(self.Mem, self.bkb,self.x,self.y,x,y,self.rotate,self.vision_dist)

    def perform_pan(self):
        self.view_rot = self.pan(self.view_rot, self.rotate)

    def vision_process(self,ballX,ballY,robots):
        # ball detect
        if self.bkb.read_int(self.Mem, 'DECISION_ACTION_VISION') == 0:  # decision saying to vision to focus on ball
            if self.bkb.read_int(self.Mem, 'DECISION_SEARCH_ON') == 1:  # searching ball
                self.perform_pan()
            view_rot_aux = self.ball_detect(self.Mem, self.bkb, self.view_rot, self.rotate, self.x, self.y, ballX,
                                                ballY)
            if view_rot_aux != None:
                self.view_rot = view_rot_aux

        #DECISION_ACTION_VISION = 1 ---- search for the robots of the team
        if (self.bkb.read_int(self.Mem, 'DECISION_ACTION_VISION') == 1):   #to test the code, please set 0.
            #robot detect
            if robots:
                for j in range(0, len(robots)):
                    if j!=self.index-1 and self.color==robots[j].color:
                        #print 'Oponente: ', robots[j].color
                        self.robot_detect(self.Mem,self.bkb, self.view_rot, self.rotate, self.x, self.y, robots[j].x, robots[j].y, j)

        # DECISION_ACTION_VISION = 2 ---- search for the opponent robots
        if (self.bkb.read_int(self.Mem, 'DECISION_ACTION_VISION') == 2):  # to test the code, please set 0.
            # robot detect
            if robots:
                for j in range(0, len(robots)):
                    if j != self.index - 1 and self.color != robots[j].color:
                        #print 'Robo ', self.index, 'found: '
                        self.robot_detect(self.Mem, self.bkb, self.view_rot, self.rotate, self.x, self.y, robots[j].x, robots[j].y, j, self.index)

    def draw_eopra(self,screen):
        resolution = 180 / self.m
        half_resolution = resolution / 2
        farthest_boundary = self.delta_eopra * self.m / (2 * self.m - (2*self.m - 2))

        if self.m == 6:
            # qualitative distance
            # e * delta / m => e = region / m = granularity

            farthest_boundary = self.delta_eopra * self.m / (2* self.m - 10)
            pygame.draw.circle(screen.background, self.color,(int(self.x), int(self.y)), 2*self.delta_eopra/self.m, 1)
            pygame.draw.circle(screen.background, self.color, (int(self.x), int(self.y)), 4*self.delta_eopra/self.m, 1)
            pygame.draw.circle(screen.background, self.color, (int(self.x), int(self.y)), 6*self.delta_eopra/self.m, 1)
            # delta * m / (2m-e)
            pygame.draw.circle(screen.background, self.color, (int(self.x), int(self.y)), self.delta_eopra * self.m / (2* self.m - 8), 1)
            pygame.draw.circle(screen.background, self.color, (int(self.x), int(self.y)), self.delta_eopra * self.m / (2* self.m - 10), 1)
            # qualitative direction
            pygame.draw.line(screen.background, self.color, (int(self.x), int(self.y)), (
                cos(radians(self.rotate)) * farthest_boundary + int(self.x), int(self.y) -
                sin(radians(self.rotate)) * farthest_boundary), 3)
            for i in range(resolution ,360, resolution):
                pygame.draw.line(screen.background, self.color, (int(self.x), int(self.y)), (
                    cos(radians(self.rotate + i)) * farthest_boundary + int(self.x), int(self.y) -
                    sin(radians(self.rotate + i)) * farthest_boundary), 1)

                # text


        if self.m == 4:
            # e * delta / m => e = region / m = granularity
            pygame.draw.circle(screen.background, self.color, (int(self.x), int(self.y)), 2 * self.delta_eopra / self.m, 1)
            pygame.draw.circle(screen.background, self.color, (int(self.x), int(self.y)), 4 * self.delta_eopra / self.m, 1)
            # delta * m / (2m-e)
            pygame.draw.circle(screen.background, self.color, (int(self.x), int(self.y)),
                               self.delta_eopra * self.m / (2 * self.m - 6), 1)
            # qualitative direction
            pygame.draw.line(screen.background, self.color, (int(self.x), int(self.y)), (
                cos(radians(self.rotate)) * farthest_boundary + int(self.x), int(self.y) -
                sin(radians(self.rotate)) * farthest_boundary), 3)
            for i in range(resolution, 360, resolution):
                pygame.draw.line(screen.background, self.color, (int(self.x), int(self.y)), (
                    cos(radians(self.rotate + i)) * farthest_boundary + int(self.x), int(self.y) -
                    sin(radians(self.rotate + i)) * farthest_boundary), 1)
                    
                    
    def draw_starvars(self,screen):
        resolution = 180 / (self.m/2)
        half_resolution = resolution / 2
        farthest_boundary = 1000
        if self.m == 8:
            # qualitative direction
            pygame.draw.line(screen.background, self.color, (int(self.x), int(self.y)), (
                cos(radians(self.rotate)) * farthest_boundary + int(self.x), int(self.y) -
                sin(radians(self.rotate)) * farthest_boundary), 3)
            for i in range(resolution, 360, resolution):
                pygame.draw.line(screen.background, self.color, (int(self.x), int(self.y)), (
                    cos(radians(self.rotate + i)) * farthest_boundary + int(self.x), int(self.y) -
                    sin(radians(self.rotate + i)) * farthest_boundary), 1)
