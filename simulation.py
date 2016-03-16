from robot import *
from ball import *
from collisions import *
import sys

class Simulation():
    def __init__(self, screen):
        self.rotate_control = 0
        self.front = 0
        self.rotate = 0
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.rotate_control = -1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.rotate_control = 1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.front = 0.5

            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                self.front = 0

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.front = -0.5

            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                self.front = 0

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.update_mouse_pos()
                robot = Robot(self.mx, self.my)
                self.robots.append(robot)
                self.group_robots.add(robot)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                self.update_mouse_pos()
                self.ball = Ball(self.mx, self.my, 0.95)

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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                if self.robot_index_control == -1:
                    for each_robot in self.robots:
                        each_robot.kill()
                else:
                    self.robots[self.robot_index_control].kill()

            if event.type == pygame.KEYUP and event.key == pygame.K_y:
                self.ball.put_in_motion(10, -45)

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.robots[self.robot_index_control].kick(self.ball)

            if event.type == pygame.QUIT:
                sys.exit()


    def update_pos(self,check_collision):
        # robots
        self.rotate = 0

        if self.rotate_control == -1:
            self.rotate = -20
            self.rotate_control = 0

        elif self.rotate_control == 1:
            self.rotate = 20
            self.rotate_control = 0

        if self.robot_index_control == -1:
            for self.robot_index in range(0, len(self.robots)):
                if check_collision == False:
                    self.robots[self.robot_index].collision = False
                self.robots[self.robot_index].motion_model(self.front, self.rotate)
        else:
            if check_collision == False:
                self.robots[self.robot_index_control].collision = False
            self.robots[self.robot_index_control].motion_model(self.front, self.rotate)

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


    def display_update(self):
        if self.robots:
            for robot in range(0, len(self.robots)):
                self.robots[robot].draw_robot(robot, self.screen)

        if self.ball.x != 0 and self.ball.y != 0 and self.ball.friction != 0:
            self.ball.draw_ball(self.screen)

        pygame.display.flip()
