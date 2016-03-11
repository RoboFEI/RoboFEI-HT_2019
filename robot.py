from World import *
from math import cos
from math import sin
from math import radians
import time


class Robot(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Robot,self).__init__()
        self.r = 22
        self.image = pygame.Surface([2*self.r, 2*self.r])
        self.image.fill(GREEN)
        self.image.set_colorkey(GREEN)
        pygame.draw.circle(self.image,(255,0,0),(22,22),self.r,0)
        self.rect = self.image.get_rect()
        self.front = 0
        self.rotate = 0
        self.rect.x = x
        self.rect.y = y
        self.new_x = x
        self.new_y = y
        self.x_theta = 0
        self.y_theta = 0
        self.x_updated = x
        self.y_updated = y
        self.collision = False


    def draw_robot(self,index):
        self.rect.x = self.x_updated
        self.rect.y = self.y_updated
        pygame.draw.circle(self.image,BLACK,(self.r, self.r), self.r,0)
        pygame.draw.circle(self.image,BLUE,(self.r, self.r), self.r-2,0)
        pygame.draw.line(self.image,(0,0,0),(self.r, self.r),(self.r + self.x_theta, self.r - self.y_theta),3)
        font = pygame.font.Font(None, 20)
        robot_name = "B" + str(index+1)
        text = font.render(robot_name, 1, (250, 250, 250))
        textpos = (self.r - 19, self.r - 5)
        self.image.blit(text, textpos)




    def update(self,front,rotate):
        self.front = front
        if self.collision and self.front == 1:
            self.front = -2
        elif self.collision and self.front == -1:
            self.front = 2
        self.rotate = (self.rotate + rotate) % 360
        self.new_x += cos(radians(self.rotate))*self.front
        self.new_y -= sin(radians(self.rotate))*self.front
        self.x_theta = int(cos(radians(self.rotate))*20)
        self.y_theta = int(sin(radians(self.rotate))*20)


        self.x_updated = int(self.new_x)
        self.y_updated = int(self.new_y)

        if self.x_updated > 1000:
            self.x_updated = 1000
        elif self.x_updated < 0:
            self.x_updated = 0

        if self.y_updated > 700:
            self.y_updated = 700
        elif self.y_updated < 0:
            self.y_updated = 0

        self.collision = False









