from math import sqrt
from math import atan2
from math import pi
from math import cos
from math import sin



def collide_ball(robot, ball):
    d = sqrt((robot.x - ball.x)**2 + (robot.y - ball.y)**2)

    if d > robot.radius + ball.radius:
        return False

    rb = atan2((robot.y-ball.y), (ball.x-robot.x))
    br = atan2((ball.y-robot.y), (ball.x-robot.x))

    alphab = atan2(ball.speed_y, ball.speed_x)
    speedb = sqrt(ball.speed_x**2+ball.speed_y**2)
    vecb = speedb*cos(alphab-br)

    robot_speed_x = cos(robot.rotate)*robot.front - sin(robot.rotate)*robot.drift
    robot_speed_y = -sin(robot.rotate)*robot.front - cos(robot.rotate)*robot.drift
    alphar = atan2(robot_speed_y, robot_speed_x)
    speedr = sqrt(robot_speed_x**2+robot_speed_y**2)
    vecr = speedr*cos(alphar-rb)

    #print vecb, vecr, speedb

    #ball.put_in_motion(-speedb, alphab)
    #ball.put_in_motion(vecb, rb)
    #ball.put_in_motion(vecr + 0.2, rb)
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

