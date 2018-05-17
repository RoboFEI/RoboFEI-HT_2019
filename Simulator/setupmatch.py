from robot import *
from ball import *



# Field sizes:
# in x it is 70 to 970
# in y it is 70 to 670


def setup_match(screen):
    robots = []

    # changes teams names
    LeftTeam = 'ROBOFEI-HT'
    RightTeam = 'OTHERS'

    # Add robots here
    # robots.append(Robot(PosX, PosY, Angle, KEY, COLOR))
    # PosX = x position of the robot on screen
    # PosY = y position of the robot on screen
    # Angle = initial orientation in degrees
    # KEY = use (len(robots)+1)*5 !!!
    # COLOR = any color tuple, you can use the predefined ones...

    robots.append(Robot(320, 170, 0,(len(robots)+1)* screen.KEY_BKB, screen.CYAN))
    robots.append(Robot(200, 370, 0,(len(robots)+1)* screen.KEY_BKB, screen.CYAN))
    robots.append(Robot(320, 570, 0,(len(robots)+1)* screen.KEY_BKB, screen.CYAN))

    robots.append(Robot(720, 170, 180,(len(robots)+1)* screen.KEY_BKB, screen.MAGENTA))
    robots.append(Robot(840, 370, 180,(len(robots)+1)* screen.KEY_BKB, screen.MAGENTA))
    robots.append(Robot(720, 570, 180,(len(robots)+1)* screen.KEY_BKB, screen.MAGENTA))

    robots[0].imu_initial_value = 0
    robots[1].imu_initial_value = 0
    robots[2].imu_initial_value = 0

    robots[3].imu_initial_value = 180
    robots[4].imu_initial_value = 180
    robots[5].imu_initial_value = 180

    # Set robot moving errors
    # robots[i].set_errors(A, B, C, D, E, F, G, H, I, J, K, L)
    # i is the position of the desired robot in the vector robots
    # A and B are the walking errors (forward and backward walking)
    # C and D are the turning errors (left and right turning)
    # E and F are the drifting errors (left and right walking)
    # G and H are the kicking angle errors (in degrees)
    # I and J are the kicking force errors
    # K and L are the orientation sensor error (in degrees and cumulative)

    #robots[0].set_errors(0.01, 0.1, -0.02, 0.1, -0.01, 0.2, 1.0, 5.0, 0.0, 0.5, 0.1, 1)

    # Set the ball here
    # ball = Ball(PosX, PosY, Friction)
    # PosX = ball's x position (use 520)
    # PosY = ball's y position (use 370)
    # Friction = used for the speed calculation 1 is no Friction (use 0.95)

    ball = Ball(520, 370, 0.95)

    # Do not alter from here on!!!

    for rob in robots:
        rob.bkb.write_int(rob.Mem, 'DECISION_ACTION_A', 0)
        rob.ball = ball

    return robots, ball, LeftTeam, RightTeam