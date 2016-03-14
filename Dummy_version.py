from robot import *
from ball import *
from collisions import *


#python
from math import cos

import sys

def update_mouse_pos():
    mx, my = pygame.mouse.get_pos()
    return mx, my

def view_left(view_rot):
    view_rot = (view_rot - 45) % 360
    diff = abs(view_rot-rotate)
    if diff == 315:
        diff = 45
    elif diff == 270:
        diff = 90
    if diff > 90:
        view_rot = (view_rot + 45) % 360
    return view_rot

def view_right(view_rot):
    view_rot = (view_rot + 45) % 360
    diff = abs(view_rot-rotate)
    if diff == 315:
        diff = 45
    elif diff == 270:
        diff = 90
    if diff > 90:
        view_rot = (view_rot - 45) % 360
    return view_rot


def search(view_rot):
    while view_left(view_rot) <= 90:
        view_rot = view_right(view_rot)
    while view_left(view_rot) <= 90:
        view_rot = view_right(view_rot)
    return view_rot

rotate = 0
x_ball, y_ball = -10, -10
front = 0
x,y = 0, 0
robots = []
robot_index_control = 'all'
rotate_control = 0
index = 0
ball = Ball(0,0,0)
view_rot = 0

while 1:

    mx, my = pygame.mouse.get_pos()
    #print mx, my

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            rotate_control = -1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            rotate_control = 1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
            view_rot = view_left(view_rot)


        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
            view_rot = view_right(view_rot)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            front = 1

        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            front = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            front = -1

        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            front = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            robot = Robot(mx,my)
            robots.append(robot)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            ball = Ball(mx, my, 0.95)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
            robot_index_control = 'all'

        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            robot_index_control = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            robot_index_control = 1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            robot_index_control = 2

        if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
            robot_index_control = 3

        if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
            robot_index_control = 4

        if event.type == pygame.KEYDOWN and event.key == pygame.K_6:
            robot_index_control = 5

        if event.type == pygame.KEYDOWN and event.key == pygame.K_7:
            robot_index_control = 6

        if event.type == pygame.KEYDOWN and event.key == pygame.K_8:
            robot_index_control = 7

        if event.type == pygame.KEYDOWN and event.key == pygame.K_9:
            robot_index_control = 8

        if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
            if robot_index_control == 'all':
                for each_robot in robots:
                    each_robot.kill()
            else:
                robots[robot_index_control].kill()

        if event.type == pygame.KEYUP and event.key == pygame.K_y:
            ball.put_in_motion(10, -45)

        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            robots[robot_index_control].kick(ball)


        #if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
        #    robot = pygame.transform.rotate(robot,45)

        if event.type == pygame.QUIT:
            sys.exit()

    field = SoccerField()
    field.draw_soccer_field(screen)


    rotate = 0

    if rotate_control == -1:
        rotate = -45
        rotate_control = 0
        view_rot = (view_rot - 45) % 360


    elif rotate_control == 1:
        rotate = 45
        rotate_control = 0
        view_rot = (view_rot + 45) % 360

    #desenha robos
    if robots:
        for robot in range(0,len(robots)):
            robots[robot].draw_robot(robot)
            robots[robot].draw_vision(view_rot)
            robots[robot].view_obj(550,350,view_rot)
            collide(robots[robot],ball)
            if len(robots) > 1:
                for other_robot in range(0,len(robots)):
                    if robot != other_robot:
                        if collision(robots[robot], robots[other_robot]):
                            robots[robot].collision = True
                            robots[other_robot].collision = True
                            print 'collision'



    if robot_index_control == 'all':
        for robot_index in range(0,len(robots)):
          robots[robot_index].motion_model(front, rotate)
    else:
        robots[robot_index_control].motion_model(front, rotate)


    ball.motion_model()

    if ball.x != 0 and ball.y != 0 and ball.friction != 0:
        ball.draw_ball()

    pygame.display.flip()

    clock.tick(60)


