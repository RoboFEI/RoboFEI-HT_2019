
from behavior import *
import time

import sys
sys.path.append('../../Localization/src/')
from eopra_discretization import *


robot = Naive()

while True:
    print 'opra ', opra_discretization(robot.get_motor_pan_degrees())

    print 'distance_eopra', distance_discretization(robot.get_dist_ball())
    time.sleep(2)
