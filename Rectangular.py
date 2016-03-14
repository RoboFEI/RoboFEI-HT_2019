import random
from math import cos
from math import sin

def toRectangular(point):
    r = point[0]
    a = point[1]
    return (r * cos(a), r * sin(a))

