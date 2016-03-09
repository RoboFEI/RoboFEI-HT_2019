#local
from robot import *
from collisions import *

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
robots = [0]
robot_index_control = 0
rotate_control = 0

while 1:

    mx, my = pygame.mouse.get_pos()
    #print mx, my

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            rotate_control = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            rotate_control = -1

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

        if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
            robot_index_control = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            robot_index_control = 1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            robot_index_control = 2

        if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            robot_index_control = 3

        if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
            robot_index_control = 4

        if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
            robot_index_control = 5

        if event.type == pygame.KEYDOWN and event.key == pygame.K_6:
            robot_index_control = 6

        if event.type == pygame.KEYDOWN and event.key == pygame.K_7:
            robot_index_control = 7

        if event.type == pygame.KEYDOWN and event.key == pygame.K_8:
            robot_index_control = 8

        if event.type == pygame.KEYDOWN and event.key == pygame.K_9:
            robot_index_control = 9


        #if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
        #    robot = pygame.transform.rotate(robot,45)

        if event.type == pygame.QUIT:
            sys.exit()

    draw_soccer_field()


    rotate = 0

    if rotate_control == 1:
        rotate = 15
        rotate_control = 0


    elif rotate_control == -1:
        rotate = -15
        rotate_control = 0

    if robot_index_control == 0:
        for robot_index in range(1,len(robots)):
          robots[robot_index].motion_model(front, rotate)
    else:
        robots[robot_index_control].motion_model(front, rotate)
        if len(robots) > 3:
            if collide(robots[1], robots[2]):
                print 'colidiu'


    if robots:
        for robot_index in range(1,len(robots)):
            robots[robot_index].draw_robot(robot_index)




    pygame.display.flip()

    clock.tick(60)


