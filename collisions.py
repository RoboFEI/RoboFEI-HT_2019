from math import sqrt
from math import atan2
from math import pi
from math import cos
from math import sin



def collide_ball(robot, ball):
    d = sqrt((robot.x - ball.x)**2 + (robot.y - ball.y)**2)

    if d > robot.radius + ball.radius:
        return False
    else:
        r = atan2((ball.y-robot.y), (ball.x-robot.x))
        if float(ball.speed_x) <= 1 and  float(ball.speed_y) <= 1:
            ball.put_in_motion( 1, 1, r*180/pi)
        else:
            ball.put_in_motion(-ball.speed_x, -ball.speed_y, r*180/pi)
        return True


def collide_robot(fst_robot, snd_robot):
    dr = sqrt((fst_robot.new_x - snd_robot.new_x)**2 + (fst_robot.new_y - snd_robot.new_y)**2)

    if dr > fst_robot.radius + snd_robot.radius:
        return False
    else:
        return True

    #fst_r = atan2((fst_robot.y-snd_robot.y), (fst_robot.x-snd_robot.x))
    #scn_r = atan2((snd_robot.y-fst_robot.y), (snd_robot.x-fst_robot.x))
    #print fst_r, scn_r

