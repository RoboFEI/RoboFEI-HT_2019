from robot import *
from ball import *
from collisions import *
import sys
from random import random
from random import randrange

class Simulation():
    def __init__(self, screen):
        self.rotate_control = 0
        '''self.front = 0
        self.rotate = 0
        self.drift = 0'''
        self.robot_index_control = -1
        self.robots = []
        self.ball = Ball(0, 0, 0)
        self.mx = 0
        self.my = 0
        self.screen = screen
        self.group_robots = pygame.sprite.Group()

    def update_mouse_pos(self):
        self.mx, self.my = pygame.mouse.get_pos()

    def perform_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.robots[self.robot_index_control].control.action_select(8)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.robots[self.robot_index_control].control.action_select(18)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.robots[self.robot_index_control].control.action_select(2)

            #<<<<<<< HEAD
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            #    self.front = 0.5
            #=======
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.robots[self.robot_index_control].control.action_select(3)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.robots[self.robot_index_control].control.action_select(1)

            #<<<<<<< HEAD
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            #    self.front = -0.5
            #=======
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.robots[self.robot_index_control].control.action_select(17)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.robots[self.robot_index_control].control.action_select(6)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.robots[self.robot_index_control].control.action_select(7)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.robots[self.robot_index_control].control.action_select(9)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                self.robots[self.robot_index_control].control.action_select(14)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                self.robots[self.robot_index_control].control.action_select(0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                self.robots[self.robot_index_control].control.action_select(11)

            if event.type == pygame.KEYUP and event.key == pygame.K_x:
                self.robots[self.robot_index_control].control.action_select(5)

            if event.type == pygame.KEYUP and event.key == pygame.K_c:
                self.robots[self.robot_index_control].control.action_select(4)

            if event.type == pygame.KEYUP and event.key == pygame.K_z:
                self.robots[self.robot_index_control].control.action_select(12)

            if event.type == pygame.KEYUP and event.key == pygame.K_v:
                self.robots[self.robot_index_control].control.action_select(13)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.update_mouse_pos()
                robot = Robot(self.mx, self.my,(len(self.robots)+1)*500)
                self.robots.append(robot)
                self.group_robots.add(robot)
                #print len(self.robots)

                #robot.set_errors(randrange(-1,1), randrange(-1,1), randrange(-1,1), randrange(-1,1), randrange(-1,1), randrange(-1,1), randrange(-1,1), randrange(-1,1), randrange(-1,1), randrange(-1,1), randrange(-1,1), randrange(-1,1))

            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                self.update_mouse_pos()
                self.ball = Ball(self.mx, self.my, 0.95)
                for robot in self.robots:
                    robot.ball = self.ball

            if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                self.robot_index_control = -1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                self.robot_index_control = 0

            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                self.robot_index_control = 1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                self.robot_index_control = 2

            if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                self.robot_index_control = 3

            if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                self.robot_index_control = 4

            if event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                self.robot_index_control = 5

            if event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                self.robot_index_control = 6

            if event.type == pygame.KEYDOWN and event.key == pygame.K_8:
                self.robot_index_control = 7

            if event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                self.robot_index_control = 8

            if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.robot_index_control = 9

            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.robot_index_control = 10

            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.robot_index_control = 11

            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.robot_index_control = 12

            if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.robot_index_control = 13

            if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.robot_index_control = 14

            if event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.robot_index_control = 15

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                if self.robot_index_control == -1:
                    for each_robot in self.robots:
                        each_robot.kill()
                else:
                    self.robots[self.robot_index_control].kill()

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.robots[self.robot_index_control].control.action_select(5)

            if event.type == pygame.QUIT:
                sys.exit()


    def update_pos(self,check_collision):
        # robots
        #<<<<<<< HEAD
        # self.rotate = 0
        #
        # if self.rotate_control == -1:
        #     self.rotate = -15
        #     self.rotate_control = 0
        #
        # elif self.rotate_control == 1:
        #     self.rotate = 15
        #     self.rotate_control = 0
        #
        # if self.robot_index_control == -1:
        #     for self.robot_index in range(0, len(self.robots)):
        #         if check_collision == False:
        #             self.robots[self.robot_index].collision = False
        #         self.robots[self.robot_index].motion_model(self.front, self.rotate)
        # else:
        #     if check_collision == False:
        #         self.robots[self.robot_index_control].collision = False
        #     self.robots[self.robot_index_control].motion_model(self.front, self.rotate)
        #=======
        for robot in self.robots:
            if check_collision == False:
                     robot.collision = False
            robot.motion_model()
            robot.control.control_update()

        # ball
        self.ball.motion_model()

    def check_collision(self,field):
        if self.robots:
            for robot in range(0, len(self.robots)):
                for other_robot in range(0, len(self.robots)):
                    collide_ball(self.robots[other_robot], self.ball)
                    for post in field.goalpost_list:
                        if (collide_robot_goalpost(self.robots[robot],post) or
                                (robot != other_robot and
                                collide_robot(self.robots[robot], self.robots[other_robot]))):
                            self.robots[robot].collision = True


    def display_update(self):
        if self.robots:
            for robot in range(0, len(self.robots)):
                self.robots[robot].draw_robot(robot, self.screen)
                self.robots[robot].draw_vision(self.screen)

        if self.ball.x != 0 and self.ball.y != 0 and self.ball.friction != 0:
            self.ball.draw_ball(self.screen)


        pygame.display.flip()

    def searching(self):
        if self.robots:
            for i in range(0, len(self.robots)):
                self.robots[i].perform_pan(self.ball.x,self.ball.y)
                for j in range(0, len(self.robots)):
                    if i!=j:
                        self.robots[i].perform_pan(self.robots[j].x,self.robots[j].y)
