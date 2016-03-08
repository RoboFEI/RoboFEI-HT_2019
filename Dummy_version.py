#local
from robot import *

#python
from math import cos

import sys

def update_mouse_pos():
    mx, my = pygame.mouse.get_pos()
    return mx, my


def draw_ball(x,y):
    pygame.draw.circle(screen,(255,255,255),(x,y),10,0)

rotate = 0
ball = False
x_ball, y_ball = -10, -10
front = 0
x,y = 0, 0
robots = []
index = 0

while 1:

    mx, my = pygame.mouse.get_pos()
    #print mx, my

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            rotate += 45 % 360
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            rotate -= 45 % 360

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            front = 1

        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            front = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            front = -1

        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            front = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            robot = Robot(mx,my,0)
            robots.append(robot)

        #if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
        #    robot = pygame.transform.rotate(robot,45)

        if event.type == pygame.QUIT:
            sys.exit()

    draw_soccer_field()

    if not robots:
        pass
    else:
        print 'no empty'
        robots[0].movement(front, rotate)


    pygame.display.flip()

    clock.tick(60)


