from robot import *
from ball import *
from collisions import *
import sys
from helpmenu import *
from random import random
from random import randrange
from setupmatch import *

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

        self.field = None

        self.Help = False

    def update_mouse_pos(self):
        self.mx, self.my = pygame.mouse.get_pos()

    def perform_events(self):
        for event in pygame.event.get():
            try:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                        self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 8)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 18)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 2)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 3)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 1)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 17)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 6)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 7)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 9)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 14)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 0)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 11)

                if event.type == pygame.KEYUP and event.key == pygame.K_l:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 5)

                if event.type == pygame.KEYUP and event.key == pygame.K_p:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 4)

                if event.type == pygame.KEYUP and event.key == pygame.K_i:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 12)

                if event.type == pygame.KEYUP and event.key == pygame.K_j:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem, 'DECISION_ACTION_A', 13)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    self.update_mouse_pos()
                    robot = Robot(self.mx, self.my, 0,(len(self.robots)+1)*100, self.screen.CYAN)

                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        robot = Robot(self.mx, self.my, 180, (len(self.robots)+1)* self.screen.KEY_BKB, self.screen.MAGENTA)

                    if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                        robot = Robot(self.mx, self.my,0,(len(self.robots)+1)* self.screen.KEY_BKB, self.screen.YELLOW)

                    if pygame.key.get_mods() & pygame.KMOD_LALT:
                        robot = Robot(self.mx, self.my,180,(len(self.robots)+1)* self.screen.KEY_BKB, self.screen.BLACK)

                    if pygame.key.get_mods() & pygame.KMOD_RSHIFT:
                        robot = Robot(self.mx, self.my,180,(len(self.robots)+1)* self.screen.KEY_BKB, self.screen.ORANGE)

                    robot.bkb.write_int(robot.Mem, 'DECISION_ACTION_A', 0)
                    robot.ball = self.ball
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


                if event.type == pygame.KEYUP and event.key == pygame.K_F1:
                    self.Help = not self.Help

                if event.type == pygame.KEYUP and event.key == pygame.K_F2:
                    self.robots = []
                    self.robots, self.ball, self.field.FriendTeam, self.field.EnemyTeam = setup_match(self.screen)
                    self.field.GameStop = True

                if event.type == pygame.KEYUP and event.key == pygame.K_F3:
                    self.robots = []
                    print '- RESET -'
                    self.robots, self.ball, self.field.FriendTeam, self.field.EnemyTeam = setup_match(self.screen)
                    self.field.FriendGoals = 0
                    self.field.EnemyGoals = 0
                    self.field.Counter = 0
                    self.field.GameStop = True

                if event.type == pygame.KEYUP and event.key == pygame.K_F5:
                    GS = True
                    for goal in self.field.Goals:
                        if self.ball.x - self.ball.radius > goal.x1 and self.ball.x + self.ball.radius < goal.x2 and self.ball.y - self.ball.radius > goal.y1 and self.ball.y + self.ball.radius < goal.y2:
                            GS = False
                    if GS:
                        self.field.GameStop = not self.field.GameStop

                if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem,
                                                                        'VISION_BALL_CENTERED', 1)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    self.robots[self.robot_index_control].bkb.write_int(self.robots[self.robot_index_control].Mem,
                                                                        'VISION_BALL_CENTERED', 0)
            except:
                pass


            if event.type == pygame.QUIT:
                sys.exit()


    def update_pos(self):
        for robot in self.robots:

            robot.motion_model(self.field.LimitLines, self.field.goalpost_list, self.robots)
            robot.control.control_update()

        # ball
        GS, F, E = self.ball.motion_model(self.field.goalpost_list, self.field.LimitLines, self.field.Goals, self.field.PlayField)
        if not self.field.GameStop and GS:
            self.field.FriendGoals += F
            self.field.EnemyGoals += E
            self.field.GameStop = GS

    def display_update(self):
        if self.robots:
            for robot in range(0, len(self.robots)):
                self.robots[robot].draw_robot(robot, self.screen)
                self.robots[robot].draw_vision(self.screen)
                self.robots[robot].vision_process(self.ball.x, self.ball.y, self.robots)
                if self.robots[robot].bkb.read_int(self.robots[robot].Mem,'VISION_BALL_CENTERED') == 1:
                    self.robots[robot].searching()

        if self.ball.x != 0 and self.ball.y != 0 and self.ball.friction != 0:
            self.ball.draw_ball(self.screen)

        if self.Help:
            help(self.screen)

        if not self.field.GameStop:
            self.field.Counter += self.screen.clock.get_time()

        pygame.display.flip()


