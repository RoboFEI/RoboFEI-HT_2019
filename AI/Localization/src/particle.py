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
            self.rotation = -rotation
        elif normals:
            self.rotation = rnd.gauss(normals[2][0], normals[2][1])
        else:
            self.rotation = rnd.randint(regions[2][0], regions[2][1])
        
        self.weight = weight # Holds particles weight, can come from previous iterations

        # Motion error coefficients
        # a0: ordem(), a1: ordem(), a2: ordem(), a3: ordem()
        # a4: ordem(), a5: ordem(), a6: ordem(), a7: ordem()
        # a8: ordem(), a9: ordem(), a10: ordem(), a11: ordem()
        # a12: ordem(), a13: ordem(), a14: ordem(), a15: ordem()

        if a == None:
            a0 = rnd.gauss(0.007, 0.002)
            a1 = rnd.gauss(7, 2)
            a2 = rnd.gauss(0.00007, 0.00002)
            a3 = rnd.gauss(0.07, 0.02)
            a4 = rnd.gauss(0.00007, 0.00002)
            a5 = rnd.gauss(0.07, 0.02)
            self.a = (a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15)
        else:
            self.a = a

        # Standard deviation used for computing angles likelihoods, in degrees.
        if std == None:
            self.std = 30
        else:
            self.std == std

    #----------------------------------------------------------------------------------------------
    #   Method which moves particles around, reimplement.
    #----------------------------------------------------------------------------------------------
    def Motion(self, straight=0, drift=0, rotational=0, moving=1, dt=0):
        # straight is the robot's forward speed in cm/s
        # drift is the robot's sideways speed in cm/s
        # rotational is the robot's angular speed in degrees/s
        # moving is a boolean which caracterizes a moving robot.

        rtt = radians(rotational) # converts rotational from degrees to radians
        
        # Adds a gaussian error to thhe forward speed
        F = rnd.gauss(straight, self.a[0]*straight**2 + self.a[1]*drift**2 + self.a[2]*rotational + self.a[3]*moving)
        # Adds a gaussian error to the drift speed
        D = rnd.gauss(drift, self.a[4]*straight**2 + self.a[5]*drift**2 + self.a[6]*rotational + self.a[7]*moving)
        # Adds a gaussian error to the rotational speed
        W = rnd.gauss(rotational, self.a[8]*straight**2 + self.a[9]*drift**2 + self.a[10]*rotational + self.a[11]*moving)
        # Adds an error to the final rotational position
        g = rnd.gauss(0, self.a[12]*straight**2 + self.a[13]*drift**2 + self.a[14]*rotational + self.a[15]*moving)


        theta = radians(self.rotation) # converts particle's rotation to radians.

        # In case of angle been smaller than 1 degree, execute this part
        if degrees(abs(W)) < 1:
            self.y += (D*sin(theta) + F*cos(theta))*dt # X position motion
            self.y += (D*cos(theta) + F*sin(theta))*dt # Y position motion
        else:
            # Auxiliar pre-computation
            st = sin(theta)
            sw = sin(W*dt)
            ct = cos(theta)
            cw = cos(W*dt)

            self.x += (D*st*sw - D*ct*cw + F*st*cw + F*ct*sw)/W # X position motion
            self.y += (D*st*cw + D*ct*sw + F*st*sw - F*ct*cw)/W # Y position motion
        
        # Final particle rotation
        self.rotation = degrees(theta + W*dt + g*dt)

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
        # print M, Measures, '\t', weight
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
