from robot import *
from ball import *
from collisions import *
import sys

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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.robots[self.robot_index_control].control.action_select(3)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.robots[self.robot_index_control].control.action_select(1)

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


            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.update_mouse_pos()
                robot = Robot(self.mx, self.my)
                self.robots.append(robot)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                self.update_mouse_pos()
                self.ball = Ball(self.mx, self.my, 0.95)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                self.robot_index_control = 'all'

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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                if self.robot_index_control == 'all':
                    for each_robot in self.robots:
                        each_robot.kill()
                else:
                    self.robots[self.robot_index_control].kill()

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.robots[self.robot_index_control].right_kick(self.ball)

            if event.type == pygame.QUIT:
                sys.exit()


    def update_pos(self):
        # robots

        for robot in self.robots:
            robot.motion_model()

        # ball
        self.ball.motion_model()

    def check_collision(self):
        if self.robots:
            for robot in range(0, len(self.robots)):
                collide_ball(self.robots[robot], self.ball)
                if len(self.robots) > 1:
                    for other_robot in range(0, len(self.robots)):
                        if robot != other_robot:
                            if collide_robot(self.robots[robot], self.robots[other_robot]):
                                self.robots[robot].collision = True
                                self.robots[other_robot].collision = True
                                print 'collision'

    def display_update(self):
        if self.robots:
            for robot in range(0, len(self.robots)):
                self.robots[robot].draw_robot(robot, self.screen)

        if self.ball.x != 0 and self.ball.y != 0 and self.ball.friction != 0:
            self.ball.draw_ball(self.screen)

        pygame.display.flip()
