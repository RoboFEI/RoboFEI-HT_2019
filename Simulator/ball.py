
from screen import *
from math import cos
from math import sin
from math import radians
from collisions import *


class Ball():
    def __init__(self, x, y, friction):
        self.x = x
        self.y = y
        self.friction = friction
        self.speed_x = 0
        self.speed_y = 0
        self.radius = 9


    def put_in_motion(self, speed, angle):
        self.speed_x = speed * cos(radians(angle))
        self.speed_y = - speed * sin(radians(angle))

    def motion_model(self, goal_posts, limitlines, goals, field):
            # print "Motion"
            self.speed_x *= self.friction
            self.speed_y *= self.friction

            # print "Speed: " + str(self.speed_x) + "x" + str(self.speed_y)
            # if self.x + self.speed_x > 1040 - self.radius or self.x + self.speed_x < self.radius:
            #     self.speed_x = - self.speed_x
            # if self.y + self.speed_y > 740 - self.radius or self.y + self.speed_y < self.radius:
            #     self.speed_y = - self.speed_y

            self.x += self.speed_x
            self.y += self.speed_y

            for goal in goal_posts:
                collision_ball_vs_goal(self, goal)

            for line in limitlines:
                collision_ball_vs_line(self, line)

            for goal in goals:
                if self.x - self.radius > goal.x1 and self.x + self.radius < goal.x2 and self.y - self.radius > goal.y1 and self.y + self.radius < goal.y2:
                    if goal.side == 'Friend':
                        return True, 0, 1
                    else:
                        return True, 1, 0

            # if not (self.x + self.radius > field.x1 and self.x - self.radius < field.x2 and self.y + self.radius > field.y1 and self.y - self.radius < field.y2):

                # return True, 0, 0
            if (self.x - self.radius > field.x2):
                self.x = 870
                if self.y > 570:
                    self.y = 570
                elif self.y < 170:
                    self.y = 170
                self.put_in_motion(0, 0)
            elif (self.x + self.radius < field.x1):
                self.x = 170
                if self.y > 570:
                    self.y = 570
                elif self.y < 170:
                    self.y = 170
                self.put_in_motion(0, 0)

            if (self.y - self.radius > field.y2):
                self.y = 570
                if self.x > 870:
                    self.x = 870
                elif self.x < 170:
                    self.x = 170
                self.put_in_motion(0, 0)
            elif (self.y + self.radius < field.y1):
                self.y = 170
                if self.x > 870:
                    self.x = 870
                elif self.x < 170:
                    self.x = 170
                self.put_in_motion(0, 0)

            return False, 0, 0

    def draw_ball(self, screen):
        #cirle
        pygame.draw.circle(screen.background, screen.BLACK, (int(self.x),int(self.y)), self.radius-1, 0)
        ball = pygame.image.load("ball.png")
        ball = pygame.transform.scale(ball,(2*self.radius,2*self.radius))
        screen.background.blit(ball,(self.x - self.radius, self.y - self.radius))