from World import *
from math import cos
from math import sin
from math import radians


class Robot(pygame.sprite.Sprite):
    def __init__(self,x,y,theta):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.theta = radians(theta)
        self.new_x = x
        self.new_y = y
        self.front = 0
        self.rotate = 0
        self.index = 0
        self.radius = 22

    def draw_robot(self,robot_index):
        pygame.draw.circle(screen,(0,0,0),(self.x ,self.y),self.radius,0)
        pygame.draw.circle(screen,(0,0,200),(self.x ,self.y),self.radius-2,0)
        x_theta = cos(self.theta)*20
        y_theta = sin(self.theta)*20
        pygame.draw.line(screen,(0,0,0),(self.x ,self.y),(x_theta+self.x ,y_theta+self.y),3)
        font = pygame.font.Font(None, 20)
        self.index = robot_index
        robot_name = "B" + str(self.index)
        text = font.render(robot_name, 1, (10, 10, 10))
        textpos = (self.x - 5, self.y - 40)
        screen.blit(text, textpos)

    def motion_model(self,front,rotate):
        self.front = front
        self.rotate = (self.rotate + rotate) % 360
        self.new_x += cos(radians(self.rotate))*front
        self.new_y += sin(radians(self.rotate))*front

        self.x = int(self.new_x)
        self.y = int(self.new_y)

        if self.x > 1040:
            self.x = 1040
        elif self.x < 0:
            self.x = 0

        if self.y > 740:
            self.y = 740
        elif self.y < 0:
            self.y = 0


        self.theta = radians(self.rotate)
