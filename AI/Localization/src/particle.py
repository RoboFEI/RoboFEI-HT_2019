__author__ = "RoboFEI-HT"
__authors__ = "Aislan C. Almeida"
__license__ = "GNU General Public License v3.0"

from math import *
import random as rnd

#--------------------------------------------------------------------------------------------------
#   Class implementing a particle used on Particle Filter Localization
#--------------------------------------------------------------------------------------------------

class Particle(object):
    #----------------------------------------------------------------------------------------------
    #   Particle constructor
    #----------------------------------------------------------------------------------------------
    def __init__(self, x=None, y=None, rotation=None, weight=1, normals=None, regions=None, a=None, std=None):
        
        # This block sets the initial position values of the particles.
        # If there was any given value, adopt it;
        # else if there was a gaussian possible position given, generate a random position;
        # else create a totally random one.

        # Note: normals is a 3x2 matrix, where
        # the first line presents the mean and standard deviation of the x position
        # the second line presents the mean and standard deviation of the y position
        # the third line presents the mean and standard deviation of the rotation

        # Note2: regions is a 3x2 matrix, where
        # the first line presents the min and max values of the x position
        # the second line presents the min and max values of the y position
        # the third line presents the min and max values of the rotation

        if regions == None:
            regions = ((0, 900), (0, 600), (-180, 180))

        if x != None:
            self.x = x
        elif normals:
            self.x = rnd.gauss(normals[0][0], normals[0][1])
        else:
            self.x = rnd.randint(regions[0][0], regions[0][1])

        if y != None:
            self.y = y
        elif normals:
            self.y = rnd.gauss(normals[1][0], normals[1][1])
        else:
            self.y = rnd.randint(regions[1][0], regions[1][1])

        if rotation != None:
            self.rotation = rotation
        elif normals:
            self.rotation = rnd.gauss(normals[2][0], normals[2][1])
        else:
            self.rotation = rnd.randint(regions[2][0], regions[2][1])
        
        self.weight = weight # Holds particles weight, can come from previous iterations

        # Motion error coefficients
        # See Probabilistic Robotics, page 124, Table 5.3 for more details.
        # a0: ordem(-2), a1: ordem(1)
        # a2: ordem(-4), a3: ordem(-1)
        # a4: ordem(-4), a4: ordem(-1)
        if a == None:
            self.a = (0.007, 0.7, 0.00007, 0.07, 0.00007, 0.07)
        else:
            self.a = a

        # Standard deviation used for computing angles likelihoods, in degrees.
        if std == None:
            self.std = 0
        else:
            self.std == std

    #----------------------------------------------------------------------------------------------
    #   Method which moves particles around. (Probabilistic Robotics, pg 124, table 5.1)
    #----------------------------------------------------------------------------------------------
    def Motion(self, translational=0, rotational=0, dt=0):
        # translational is the robot's speed in cm/s
        # rotational is the robot's angular speed in degrees/s

        rtt = radians(rotational) # converts rotational from degrees to radians
        
        # line 2:
        v = rnd.gauss(translational, self.a[0]*translational**2+self.a[1]*rtt**2)
        # line 3:
        w = rnd.gauss(rtt, self.a[2]*translational**2+self.a[3]*rtt**2)
        # line 4:
        g = rnd.gauss(0, self.a[4]*translational**2+self.a[5]*rtt**2)
        
        theta = radians(self.rotation) # converts particle's rotation to radians
        # In case of angle been smaller than 1 degree, execute this part
        
        if degrees(abs(w)) < 1:
            self.x += v * cos(theta) * dt # delocation of x position
            self.y += v * sin(theta) * dt # delocation of y position
        else:
            
            # line 5:
            self.x += -v/w*sin(theta) + v/w*sin(theta + w*dt) 
            # line 6:
            self.y += v/w*cos(theta) - v/w*cos(theta + w*dt)
        # line 7:
        self.rotation = degrees(theta + w*dt + g*dt)

    #----------------------------------------------------------------------------------------------
    #   Likelihood computation
    #----------------------------------------------------------------------------------------------
    def Sensor(self, Measures=None, weight=1):
        # Compute the angles the particle should be perceiving the landmark
        Blue = -degrees(atan2(-self.y, -self.x)) - self.rotation
        Red = -degrees(atan2(-self.y, 900-self.x)) - self.rotation
        Yellow = -degrees(atan2(600-self.y, -self.x)) - self.rotation
        Purple = -degrees(atan2(600-self.y, 900-self.x)) - self.rotation
        
        # Generate a vector with the measures
        M = [Blue, Red, Yellow, Purple]

        # Computes the cumulative likelihood of all particles.
        for i in range(4):
            if Measures[i] != None:
                weight *= ComputeAngLikelihoodDeg(Measures[i], M[i], self.std)

        self.weight = weight
        return weight

#--------------------------------------------------------------------------------------------------
#   Computes the likelihood between two angles in degrees.
#--------------------------------------------------------------------------------------------------
def ComputeAngLikelihoodDeg(ang, base, std_deviation=0):
    # Note: the standard deviation also is in degrees

    # If the standard deviation is null
    if std_deviation == 0: 
        # return a binary answer.
        if ang == base:
            return 1
        else:
            return 0
    else:
        # else computes the cartesian points based on the angles,
        xa = cos(radians(ang))
        ya = sin(radians(ang))
        xb = cos(radians(base))
        yb = sin(radians(base))

        # computes the distance between these points,
        d = hypot(xa-xb, ya-yb)

        # converts the standard deviation into aa distance measure,
        sa = cos(radians(std_deviation))
        sb = sin(radians(std_deviation))
        s = hypot(sa-1, sb)

        # returns the likelihood between the given angles.
        return exp(-(d)/(2*s**2))/sqrt(2*pi*s**2)
