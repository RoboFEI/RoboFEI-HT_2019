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
        self.theta = 0
        self.screen = screen
        self.group_robots = pygame.sprite.Group()

    def update_mouse_pos(self):
        self.mx, self.my = pygame.mouse.get_pos()

    def perform_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 8)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 18)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 2)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 3)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 1)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 17)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 6)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 7)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 9)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 14)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 11)

            if event.type == pygame.KEYUP and event.key == pygame.K_x:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 5)

            if event.type == pygame.KEYUP and event.key == pygame.K_c:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 4)

            if event.type == pygame.KEYUP and event.key == pygame.K_z:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 12)

            if event.type == pygame.KEYUP and event.key == pygame.K_v:
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 13)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.update_mouse_pos()
                robot = Robot(self.mx, self.my, 0,(len(self.robots)+1)*100, self.screen.CYAN)
                robot.bkb.write_int(robot.Mem, 'DECISION_ACTION_A', 0)

                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    robot = Robot(self.mx, self.my, 180, (len(self.robots)+1)*100, self.screen.MAGENTA)

                if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                    robot = Robot(self.mx, self.my,0,(len(self.robots)+1)*100, self.screen.YELLOW)

                if pygame.key.get_mods() & pygame.KMOD_LALT:
                    robot = Robot(self.mx, self.my,180,(len(self.robots)+1)*100, self.screen.BLACK)

                if pygame.key.get_mods() & pygame.KMOD_RSHIFT:
                    robot = Robot(self.mx, self.my,180,(len(self.robots)+1)*100, self.screen.ORANGE)

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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                print 'p'
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem,'VISION_SEARCH_BALL', 1)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                print 'o'
                self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem,'VISION_SEARCH_BALL', 0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                print 'y'
                self.robots[self.robot_index_control].vision_process(self.ball.x,self.ball.y,self.robots)

            if event.type == pygame.QUIT:
                sys.exit()


    def update_pos(self,check_collision):
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
                        collide_ball_goalpost(self.ball,post)
                        if (collide_robot_goalpost(self.robots[robot],post) or
                                (robot != other_robot and
                                collide_robot(self.robots[robot], self.robots[other_robot]))):
                            self.robots[robot].collision = True


    def display_update(self):
        if self.robots:
            for robot in range(0, len(self.robots)):
                self.robots[robot].draw_robot(robot, self.screen)
                self.robots[robot].draw_vision(self.screen)
                #TODO inicia o processo de busca da bola - dar um merge
                self.robots[robot].vision_process(self.ball.x,self.ball.y,self.robots)
                if self.robots[robot].bkb.read_int(self.robots[robot].Mem,'VISION_SEARCH_BALL') == 1:
                    self.robots[robot].searching()


        if self.ball.x != 0 and self.ball.y != 0 and self.ball.friction != 0:
            self.ball.draw_ball(self.screen)




        pygame.display.flip()


