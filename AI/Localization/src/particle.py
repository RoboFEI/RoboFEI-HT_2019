__author__ = "RoboFEI-HT"
__authors__ = "Aislan C. Almeida"
__license__ = "GNU General Public License v3.0"

import numpy as np
import scipy.special as sp
import time

# Distance and angles of the notable points
vpoints = [
     (1,0),
     (9999999,0),
     
     (100,-45),
     (200,-45),
     (300,-45),

     (70,-30),
     (140,-30),
     (300,-30),
     (530,-30),

     (80,-20),
     (180,-20),
     (420,-20),

     (90,-10),
     (150,-10),
     (300,-10),

     (50,0),
     (100,0),
     (200,0),
     (500,0),

     (90,10),
     (150,10),
     (300,10),

     (80,20),
     (190,20),
     (430,20),

     (70,30),
     (140,30),
     (300,30),
     (530,30),

     (100,45),
     (200,45),
     (300,45)]

# Vars used to compute the particles likelihood
maxWdelta = None

# field = ((8, 1032), (60, 680), (-180, 180))
field = ((0, 1040), (0, 740), (-180, 180))

#--------------------------------------------------------------------------------------------------
#   Class implementing a particle used on Particle Filter Localization
#--------------------------------------------------------------------------------------------------

class Particle(object):
    #----------------------------------------------------------------------------------------------
    #   Particle constructor
    #----------------------------------------------------------------------------------------------
    def __init__(self, x=None, y=None, rotation=None, wfactor=0, weight=1, normals=None, regions=None, factors=None, std=None, spread=1):
        # This block sets the initial position values of the particles.
        #    If there was any given value, adopt it;
        #    else if there was a gaussian possible position given, generate a random position;
        #    else create a totally random one.

        # Note: normals is a Nx3x2 matrix, where
        #    the first line presents the mean and standard deviation of the x position
        #    the second line presents the mean and standard deviation of the y position
        #    the third line presents the mean and standard deviation of the rotation

        # Note2: regions is a 3x2 matrix, where
        #    the first line presents the min and max values of the x position
        #    the second line presents the min and max values of the y position
        #    the third line presents the min and max values of the rotation

        # Note3: factors are the factors for the motion model of the particles

        # Note4: std is a vector with the values used as standard deviation for computing particles' likelihood.
        #    the first for is used for the landmarks, in sequence blue, red, yellow, purple
        #    the last one is used for the IMU orientation

        # Note5: spread determines how much the particles will spread

        if regions == None:
            self.regions = field
        else:
            self.regions = regions

        if normals != None:
            i = np.random.randint(len(normals))

        if x != None:
            self.x = x
        elif normals != None:
            self.x = np.random.normal(normals[i][0][0], normals[i][0][1])
        else:
            self.x = np.random.randint(self.regions[0][0], self.regions[0][1])

        if y != None:
            self.y = y
        elif normals != None:
            self.y = np.random.normal(normals[i][1][0], normals[i][1][1])
        else:
            self.y = np.random.randint(self.regions[1][0], self.regions[1][1])

        if rotation != None:
            self.rotation = rotation
        elif normals != None:
            self.rotation = np.random.normal(normals[i][2][0], normals[i][2][1])
        else:
            self.rotation = np.random.randint(self.regions[2][0], self.regions[2][1])

        self.weight = weight # Holds particles weight, can come from previous iterations

        # Motion error coefficients
        if factors == None:
            self.factors = [1, 2, 1, 500, 5,  1, 2, 1, 500, 7,  1, 2, 1, 100, 5]
            # self.factors = 15*[0]
            # self.factors = [1, 2, 1, 0, 10,  1, 2, 1, 0, 20,  1, 2, 1, 0, 10]
            # self.factors = [0, 0, 0, 0, 10,  0, 0, 0, 0, 20,  0, 0, 0, 0, 10]
            # self.factors = [0, 0, 0, 50, 0,  0, 0, 0, 50, 0,  0, 0, 0, 10, 0]
        else:
            self.factors = factors

        # Standard deviation used for computing angles likelihoods, in degrees.
        if std == None:
            self.std = [5, 30]
        else:
            self.std == std

        # Vars used to compute the particles likelihood
        self.gamma = 26.13
        self.Delta = 90

        self.psi = 0.7
        self.SigmaO = 70
        self.MuF = 700
        self.SigmaF = 10
        self.MuN = 10
        self.SigmaN = 1

        self.SigmaA = 5

        self.radius = (10,50)

        self.SigmaIMU = 20

        self.wfactor = wfactor # Used in order to implement the motion error.

        # Probability factors used to compute particles weights.
        self.probfactors = (1, 1, 1, 1, 0.3, 0.7)

    #----------------------------------------------------------------------------------------------
    #   Method that chooses which movement should be used
    #----------------------------------------------------------------------------------------------
    def Movement(self, straight=0, drift=0, rotational=0, moving=1, dt=0, meanw=1):
        if moving == 1:
            self.Motion(straight, drift, rotational, moving, dt, meanw)
        elif moving == 2:
            self.GetUpBackUp()
        elif moving == 3:
            self.GetUpFrontUp()
        else:
            self.Motion(0,0,0,0,dt,meanw)

    #----------------------------------------------------------------------------------------------
    #   Method which moves particles around, reimplement.
    #----------------------------------------------------------------------------------------------
    def Motion(self, straight=0, drift=0, rotational=0, moving=0, dt=0, meanw=1):
        # straight is the robot's forward speed in cm/s
        # drift is the robot's sideways speed in cm/s
        # rotational is the robot's angular speed in degrees/s

        if type(self.weight) != int:
            self.wfactor = max(min(np.log(meanw/self.weight)/np.log(1000), 2), 0)

        # Computes the forward speed with error
        Forward = straight + NRnd(self.factors[0]*straight) + NRnd(self.factors[1]*drift) + NRnd(self.factors[2]*rotational) + NRnd(self.factors[3] * self.wfactor * moving) + NRnd(self.factors[4])
        # Computes the side speed with error
        Side = drift + NRnd(self.factors[5]*straight) + NRnd(self.factors[6]*drift) + NRnd(self.factors[7]*rotational) + NRnd(self.factors[8] * self.wfactor * moving) + NRnd(self.factors[9])
        # Computes the angular speed with error
        Omega = rotational + NRnd(self.factors[10]*straight) + NRnd(self.factors[11]*drift) + NRnd(self.factors[12]*rotational) + NRnd(self.factors[13] * self.wfactor * moving) + NRnd(self.factors[14])

        # Converts angles to radians
        Omega = np.radians(Omega)
        Theta = np.radians(self.rotation)

        # Computes the new positions
        if Omega == 0:
            Direction = Theta
            x = self.x + Forward * np.cos(Theta) * dt + Side * np.sin(Theta) * dt
            y = self.y - Forward * np.sin(Theta) * dt + Side * np.cos(Theta) * dt
        else:
            Direction = Theta + Omega * dt
            Dir2 = -Theta + Omega * dt
            x = self.x + Forward/Omega * (np.sin(Direction)-np.sin(Theta)) - Side/Omega * (np.cos(-Theta)-np.cos(Dir2))
            y = self.y - Forward/Omega * (np.cos(Theta)-np.cos(Direction)) - Side/Omega * (np.sin(-Theta)-np.sin(Dir2))

        if x < self.regions[0][0] or x > self.regions[0][1] or y < self.regions[1][0] or y > self.regions[1][1]:
            return

        # Saves the new positions
        self.x = x
        self.y = y
        rot = np.degrees(Direction)
        if rot > 180:
            self.rotation = rot - 360
        elif rot < -180:
            self.rotation = rot + 360
        else:
            self.rotation = rot

    #----------------------------------------------------------------------------------------------
    #   Method to replace particles after rising up
    #----------------------------------------------------------------------------------------------
    def GetUpBackUp(self):
        self.x += NRnd(7)
        self.y += NRnd(7)
        self.rotation += NRnd(25)

    #----------------------------------------------------------------------------------------------
    #   Method which replaces particles after turning on the ground
    #----------------------------------------------------------------------------------------------
    def GetUpFrontUp(self):
        self.x += NRnd(7,-30)*np.sin(np.radians(self.rotation))
        self.y += NRnd(7,-30)*np.cos(np.radians(self.rotation))
        self.rotation += NRnd(25)
        self.GetUpBackUp()

    #----------------------------------------------------------------------------------------------
    #   Likelihood computation
    #----------------------------------------------------------------------------------------------
    def Sensor(self, landmarks=None, field=None, orientation=None, distances=None, weight=1):
        # If it was given landmarks
        if landmarks != None:
            # Computes the landmarks positions
            lm = []

            # print
            for z in [(70,280), (70,460), (970,280), (970,460)]:
                dx = z[0]-self.x
                dy = z[1]-self.y

                dist = np.hypot(dx, dy)
                ang = -np.degrees(np.arctan2(dy, dx))-self.rotation

                lm.append([dist, ang])

            # Computes weights using the formulas from the text
            for z in landmarks:
                # aux weight vectors
                w = len(lm)*[1]

                # try each landmark
                for i in range(len(lm)):
                    if z != -999:
                        w[i] *= Wdelta(lm[i][0], self.psi, self.SigmaO, self.MuF, self.SigmaF, self.MuN, self.SigmaN)
                        w[i] *= ComputeAngLikelihoodDeg(lm[i][1], z, self.SigmaA)

                weight *= max(w) # Maximizes the weight
                lm.pop(w.index(max(w))) # Erases the used landmark

        # If the given information is the field's points
        if field != None:
            size = 5. # Frames used for the observation
            pan = int(field[1])  # Gets the head's pan position
            err = np.abs(field[1] - pan) * size # Gets the error of the observation

            ifield = np.abs(field[0]) # Gets the field points with errors

            ret = [] # Holds the probabilities of each point been 1
            for k in vpoints:
                p = np.radians(-self.rotation + pan + k[1]) # Computes the direction
                i = self.x + k[0] * np.cos(p) # Computes the x position of the point
                j = self.y + k[0] * np.sin(p) # Computes the y position of the point

                r = self.regions

                # ret.append(prob(i, j, k[0], 0.1*k[0], k[1], r[0][0], r[0][1], r[1][0], r[1][1])) # Computes the probability of the point been inside the field
                if r[0][0] <= i and i <= r[0][1] and r[1][0] <= j and  j <= r[1][1]:
                    ret.append(1)
                else:
                    ret.append(0)

            # Computes a normalization value
            n = 1
            w = 1
            for i in xrange(32):
                n *= self.probfactors[0] / np.power(vpoints[i][0] * np.cos(np.radians(vpoints[i][1])), -self.probfactors[1]) * (
                    self.probfactors[3] * ifield[i] +
                    self.probfactors[2] * (1-ifield[i]))

            # Computes the normalized weight
                w *= self.probfactors[0] / np.power(vpoints[i][0] * np.cos(np.radians(vpoints[i][1])), -self.probfactors[1]) * (
                    self.probfactors[2] * (1-ifield[i]) * (1-ret[i]) +
                    self.probfactors[3] * ifield[i] * ret[i] +
                    self.probfactors[4] * ifield[i] * (1-ret[i]) +
                    self.probfactors[5] * (1-ifield[i]) * ret[i])

            w /= n

            # w = np.power(w, 1./32)

            weight *= w

        # If the IMU's orientation was given
        if orientation != None:
            weight *= ComputeAngLikelihoodDeg(np.degrees(orientation), self.rotation, self.SigmaIMU)/(np.sqrt(2*np.pi)*self.SigmaIMU)

        self.weight = max(weight, 1e-300)

        # if landmarks != None or field != None or orientation != None:
        #     self.wfactor = max(min(np.log(self.weight)/np.log(1e-10), 2.), 0.)

        # self.wfactor = 0.5
        return self.weight

    #----------------------------------------------------------------------------------------------
    #   Computes the distances for predicting the future.
    #----------------------------------------------------------------------------------------------
    def GetField(self, pan=0):
        ret = []

        # For each point
        for k in vpoints:
            p = np.radians(-self.rotation + pan + k[1]) # Computes the direction
            i = self.x + k[0] * np.cos(p) # Computes the x position of the point
            j = self.y + k[0] * np.sin(p) # Computes the y position of the point

            r = self.regions

            if r[0][0] <= i and i <= r[0][1] and r[1][0] <= j and j <= r[1][1]:
                ret.append(1)
            else:
                ret.append(0)

        # Return the points values
        return ret, pan

    #----------------------------------------------------------------------------------------------
    #   Computes the max weight of the particles, generally 1.
    #----------------------------------------------------------------------------------------------
    def MaxWeight(self, landmarks=None, field=None, orientation=None):
        weight = 1
        if landmarks != None:
            for lm in landmarks:
                if lm != -999:
                    weight *= Walpha(0)
                    weight *= maxWdelta
                else:
                    weight *= 1 - Walpha(0)

        return max(weight, 1e-300)

    #----------------------------------------------------------------------------------------------
    #   Returns a string to print the particle's representation.
    #----------------------------------------------------------------------------------------------
    def __repr__(self):
        return "x: " + str(self.x) + " y: " + str(self.y) + " z: " + str(self.rotation) + " w: " + str(self.weight)

    #----------------------------------------------------------------------------------------------
    #   Returns the variables used to create a new particle from this one.
    #----------------------------------------------------------------------------------------------
    def copy(self):
        return self.x, self.y, self.rotation, self.wfactor, self.weight

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
        # else computes the Cartesian points based on the angles,
        xa = np.cos(np.radians(ang))
        ya = np.sin(np.radians(ang))
        xb = np.cos(np.radians(base))
        yb = np.sin(np.radians(base))

        # computes the distance between these points,
        d = np.hypot(xa-xb, ya-yb)

        # converts the standard deviation into aa distance measure,
        sa = np.cos(np.radians(std_deviation))
        sb = np.sin(np.radians(std_deviation))
        s = np.hypot(sa-1, sb)

        # returns the likelihood between the given angles.
        return np.exp(-np.power(d,2)/(2*np.power(s,2)))

#--------------------------------------------------------------------------------------------------
#   Returns a random number from a normal distribution.
#--------------------------------------------------------------------------------------------------
def NRnd(sigma, mu=0):
    if sigma == 0:
        return mu
    else:
        return np.random.normal(mu, np.abs(sigma))

#--------------------------------------------------------------------------------------------------
#   Returns the probability given the x and y limits, the circle position and its radius.
#--------------------------------------------------------------------------------------------------
def prob(cx, cy, dist, std, ang, xa=0, xb=1040, ya=0, yb=740):
    ax = cx + std * np.cos(ang)
    ay = cy + std * np.sin(ang)

    bx = cx - std * np.cos(ang)
    by = cy - std * np.sin(ang)

    if ax >= xa and bx >= xa and ax <= xb and bx <= xb and ay >= ya and by >= ya and ay <= yb and by <= yb:
        return 1.
    elif ax < xa and bx < xa or ax > xb and bx > xb or ay < ya and by < ya or ay > yb and by > yb:
        return 0.

    sz = np.hypot(ax-bx, ay-by)
    sm = sz

    if ang != 0. and ang != 180. and ang != -180.:
        sm = min(sm, np.hypot(np.abs(ya-by), np.abs(ya-by)*np.abs(ax-bx)/np.abs(ay-by)))
        sm = min(sm, np.hypot(np.abs(yb-by), np.abs(yb-by)*np.abs(ax-bx)/np.abs(ay-by)))

    if ang != 90. and ang != -90.:
        sm = min(sm, np.hypot(np.abs(xa-bx), np.abs(xa-bx)*np.abs(ay-by)/np.abs(ax-bx)))
        sm = min(sm, np.hypot(np.abs(xb-bx), np.abs(xb-bx)*np.abs(ay-by)/np.abs(ax-bx)))

    ret = (np.max([0, 1-np.exp(-12*(sm/sz-0.5))]) + np.min([1, np.exp(12*(sm/sz-0.5))]))/2.
    return ret

#--------------------------------------------------------------------------------------------------
#   Computes the Walpha factor for weight computation
#--------------------------------------------------------------------------------------------------
def Walpha(ang, gamma=26.13, Delta=90):
    if -Delta+gamma < ang and ang < Delta-gamma:
        return gamma/(Delta+gamma)
    elif ang < -Delta-gamma or ang > Delta+gamma:
        return 0
    else:
        return 0.5 * (Delta+gamma-np.abs(ang))/(Delta+gamma)

#--------------------------------------------------------------------------------------------------
#   Computes the Wdelta factor for weight computation
#--------------------------------------------------------------------------------------------------
def Wdelta(dist, psi=0.7, SigmaO=70, MuF=700, SigmaF=10, MuN=10, SigmaN=1):
    return (psi + (1-psi)*np.exp(-np.power(dist,2)/(2*np.power(SigmaO,2)))) * (1 + sp.erf((MuF-dist)/(np.sqrt(2)*SigmaF))) * (1 - sp.erf((MuN-dist)/(np.sqrt(2)*SigmaN))) / 4

#--------------------------------------------------------------------------------------------------
#   Computes the maximum value Wdelta can get.
#--------------------------------------------------------------------------------------------------
if maxWdelta == None:
    psi = 0.7 # Occlusion factor in the infinity
    SigmaO = 70 # Decay rate of the occlusion factor

    MuF = 700 # Farthest distance in which a robot can see any landmark
    SigmaF = 10 # Its decay rate

    MuN = 10 # Nearest distance a robot can see anything
    SigmaN = 1 # Its decay rate

    # Generates a 1000 points in random positions
    d = np.array([])
    for i in xrange(1000):
        d = np.append(d, [np.random.randint(MuN, MuF)])

    w = 0 # Initializes the weight as 0
    while True:
        p = w # Saves the prev. weight

        d = np.random.normal(d, 0.3) # Moves points at random
        e = Wdelta(d) # Computes the new vector of weights

        w = np.max(e) # Get the biggest weight

        if np.abs(w-p) < 1e-3: # If it was just a small change saves it
            d = d[np.argmax(e)]
            break

    maxWdelta = Wdelta(d) # Saves the greatest weight
