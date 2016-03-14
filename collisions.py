from init import *
from math import cos
from math import sin
from math import radians
from math import sqrt
from math import atan2
from math import pi
from math import exp

def collide_ball(robot, ball):
    d = sqrt((robot.x - ball.x)**2 + (robot.y - ball.y)**2)

    if d > robot.radius + ball.radius:
        return False

    r = atan2((ball.y-robot.y), (ball.x-robot.x))
    ball.put_in_motion(1, r*180/pi)
    return True

def collide_robot(fst_robot, snd_robot):
    d = sqrt((fst_robot.x - snd_robot.x)**2 + (fst_robot.y - snd_robot.y)**2)

    if d > fst_robot.radius + snd_robot.radius:
        return False
    else:
        return True

    #fst_r = atan2((fst_robot.y-snd_robot.y), (fst_robot.x-snd_robot.x))
    #scn_r = atan2((snd_robot.y-fst_robot.y), (snd_robot.x-fst_robot.x))
    #print fst_r, scn_r

