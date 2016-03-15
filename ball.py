from screen import *
from math import cos
from math import sin
from math import radians


class Ball():
    def __init__(self, x, y, friction):
        self.x = x
        self.y = y
        self.friction = friction
        self.speed_x = 0
        self.speed_y = 0
        self.radius = 7

    def put_in_motion(self, speed, angle):
        self.speed_x += speed * cos(radians(angle))
        self.speed_y -= speed * sin(radians(angle))

    def motion_model(self):
        # print "Motion"
        self.speed_x *= self.friction
        self.speed_y *= self.friction

        # print "Speed: " + str(self.speed_x) + "x" + str(self.speed_y)
        if self.x + self.speed_x > 1040 - self.radius or self.x + self.speed_x < self.radius:
            self.speed_x = - self.speed_x
        if self.y + self.speed_y > 740 - self.radius or self.y + self.speed_y < self.radius:
            self.speed_y = - self.speed_y

        self.x += self.speed_x
        self.y += self.speed_y

    def draw_ball(self, screen):
        pygame.draw.circle(screen.background, screen.WHITE, (int(self.x), int(self.y)), self.radius, 0)
