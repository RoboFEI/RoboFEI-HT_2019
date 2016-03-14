from math import sqrt
from math import atan2
from math import pi
from ball import *
from robot import *

def collide(robot, ball):
    d = sqrt(((robot.rect.x + robot.r) - ball.x)**2 + ((robot.rect.y + robot.r) - ball.y)**2)

    if d > (robot.r + ball.radius):
        return False

    r = atan2((ball.y - (robot.rect.y + robot.r)), (ball.x-(robot.rect.x + robot.r)))
    ball.put_in_motion(1, r*180/pi)
    return True

def collision_robot(fst_robot, snd_robot):
    d = sqrt(((fst_robot.rect.x + fst_robot.r) - (snd_robot.rect.x + snd_robot.r))**2) #+ ((fst_robot.rect.y + fst_robot.r) - (snd_robot.rect.y + snd_robot.r)**2))
    print d
    if d > (fst_robot.r + snd_robot.r):
        return False
    else:
        fst_r = atan2(((fst_robot.rect.y + fst_robot.r) - (snd_robot.rect.y + fst_robot.r)), ((fst_robot.rect.x + fst_robot.r) - (snd_robot.rect.x + fst_robot.r)))
        scn_r = atan2(((fst_robot.rect.y - fst_robot.r) - (snd_robot.rect.y - fst_robot.r)), ((fst_robot.rect.x - fst_robot.r) - (snd_robot.rect.x - fst_robot.r)))
        print fst_r
        print scn_r

