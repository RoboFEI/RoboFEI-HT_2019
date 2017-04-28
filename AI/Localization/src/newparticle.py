__author__ = "RoboFEI-HT"
__authors__ = "Aislan C. Almeida"
__license__ = "GNU General Public License v3.0"

import numpy as np
import scipy.special as sp

# Robot's height!!!
hrobot = 50
# Robot's head's tilt's position
htilt = 17.4

# Distance and angles of the notable points
vpoints = []
# From the most distant to the nearest
for i in [-14, -13.5]:
    for j in [-20, -13.5, -7, 0, 7, 13.5, 20]:
        vpoints.append(((hrobot/np.tan(np.radians(htilt+i)))/np.cos(np.radians(j)), j))
for i in [-20, -13.5, 0, 13.5, 20]:
    vpoints.append(((hrobot/np.tan(np.radians(htilt-12.5)))/np.cos(np.radians(i)), i))
for i in [-11, -7.5]:
    for j in [-20, -7, 7, 20]:
        vpoints.append(((hrobot/np.tan(np.radians(htilt+i)))/np.cos(np.radians(j)), j))        
vpoints.append(((hrobot/np.tan(np.radians(htilt)))/np.cos(np.radians(-13.5)), -13.5))
vpoints.append(((hrobot/np.tan(np.radians(htilt)))/np.cos(np.radians(13.5)), 13.5))
vpoints.append(((hrobot/np.tan(np.radians(htilt+9)))/np.cos(np.radians(0)), 0))

# Vars used to compute the particles likelihood
maxWdelta = None

#--------------------------------------------------------------------------------------------------
#   Class implementing a particle used on Particle Filter Localization
#--------------------------------------------------------------------------------------------------

class Particle(object):
    #----------------------------------------------------------------------------------------------
    #   Particle constructor
    #----------------------------------------------------------------------------------------------
    def __init__(self, x=None, y=None, rotation=None, weight=1, maxweight=1, normals=None, regions=None, factors=None, std=None, spread=1):
        # This block sets the initial position values of the particles.
        #    If there was any given value, adopt it;
        #    else if there was a gaussian possible position given, generate a random position;
        #    else create a totally random one.

        # Note: normals is a 3x2 matrix, where
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
            regions = ((0, 900), (0, 600), (-180, 180))

        if x != None:
            self.x = x
        elif normals:
            self.x = np.random.normal(normals[0][0], normals[0][1])
        else:
            self.x = np.random.randint(regions[0][0], regions[0][1])

        if y != None:
            self.y = y
        elif normals:
            self.y = np.random.normal(normals[1][0], normals[1][1])
        else:
            self.y = np.random.randint(regions[1][0], regions[1][1])

        if rotation != None:
            self.rotation = rotation
        elif normals:
            self.rotation = np.random.normal(normals[2][0], normals[2][1])
        else:
            self.rotation = np.random.randint(regions[2][0], regions[2][1])
        
        self.weight = weight # Holds particles weight, can come from previous iterations
        self.maxweight = maxweight # Holds the previous maximun weight

        # Motion error coefficients
        if factors == None:
            # self.factors = 15*[0]
            self.factors = [1, 2, 1, 500, 10,  1, 2, 1, 500, 20,  1, 2, 1, 100, 10]
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
        self.SigmaA = 30

        self.radius = 20

        self.SigmaIMU = 30

    #----------------------------------------------------------------------------------------------
    #   Method that chooses which movement should be used
    #----------------------------------------------------------------------------------------------
    def Movement(self, straight=0, drift=0, rotational=0, moving=1, dt=0):
        if moving == 1:
            self.Motion(straight, drift, rotational, dt)
        elif moving == 2:
            self.GetUpBackUp()
        elif moving == 3:
            self.GetUpFrontUp()
        else:
            self.Motion(0,0,0,dt)

    #----------------------------------------------------------------------------------------------
    #   Method which moves particles around, reimplement.
    #----------------------------------------------------------------------------------------------
    def Motion(self, straight=0, drift=0, rotational=0, _=0, dt=0):
        # straight is the robot's forward speed in cm/s
        # drift is the robot's sideways speed in cm/s
        # rotational is the robot's angular speed in degrees/s
        
        # Computes the forward speed with error
        Forward = straight + NRnd(self.factors[0]*straight) + NRnd(self.factors[1]*drift) + NRnd(self.factors[2]*rotational) + NRnd(self.factors[3] * (1 - self.weight/self.maxweight) + NRnd(self.factors[4]))
        # Computes the side speed with error
        Side = drift + NRnd(self.factors[5]*straight) + NRnd(self.factors[6]*drift) + NRnd(self.factors[7]*rotational) + NRnd(self.factors[8] * (1 - self.weight/self.maxweight) + NRnd(self.factors[9]))
        # Computes the angular speed with error
        Omega = rotational + NRnd(self.factors[10]*straight) + NRnd(self.factors[11]*drift) + NRnd(self.factors[12]*rotational) + NRnd(self.factors[13] * (1 - self.weight/self.maxweight) + NRnd(self.factors[14]))

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

        # Resets weight variables
        self.weight = 1
        self.maxweight = 1

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
    def Sensor(self, landmarks=None, field=None, orientation=None, weight=1):
        # If it was given landmarks
        if landmarks != None:
            # Computes the landmarks positions
            lm = []
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
                    # W alpha
                    if z == -999:
                        w[i] *= 1 - Walpha(ang, self.gamma, self.Delta)
                    else:
                        w[i] *= Walpha(ang, self.gamma, self.Delta)

                    # W delta
                    if z == -999:
                        w[i] *= 1 - Wdelta(dist, self.psi, self.SigmaO, self.MuF, self.SigmaF, self.MuN, self.SigmaN, self.SigmaA)
                    else:
                        w[i] *= Wdelta(dist, self.psi, self.SigmaO, self.MuF, self.SigmaF, self.MuN, self.SigmaN, self.SigmaA)

                    # W phi
                    if z != -999:
                        w[i] *= ComputeAngLikelihoodDeg(ang, z, self.SigmaA)

                weight *= max(w) # Maximizes the weight
                lm.pop(w.index(max(w))) # Erases the used landmark
        
        # If the given information is the field's points
        if field != None:
            # Finds out the head's position
            if field[0] != 0 and field[1] == 0:
                pan = -90 # Left
            elif field[0] == 0 and field[1] != 0:
                pan = 90 # Right
            else:
                pan = 0 # Center

            ret = [] # Holds the probabilities of each point been 1
            for k in vpoints:
                p = np.radians(-self.rotation + pan + k[1]) # Computes the direction
                i = self.x + k[0] * np.cos(p) # Computes the x position of the point
                j = self.y + k[0] * np.sin(p) # Computes the y position of the point

                ret.append(prob(i, j, self.radius)) # Computes the probability of the point been inside the field

            # Computes a normalization value
            n = 1
            for i in xrange(2, 32):
                n *= 0.99 * field[i] + 0.9 * (1-field[i])

            # Computes the normalized weight
            w = 1
            for i in xrange(2, 32):
                w *= 0.99 * field[i] * ret[i-2] + 0.9 * (1-field[i]) * (1-ret[i-2]) + 0.2 * field[i] * (1-ret[i-2]) + 0.1 * (1-field[i]) * ret[i-2]
            
            w /= n
        
            weight *= w
            # print weight

        # If the IMU's orientation was given
        if orientation != None:
            weight *= ComputeAngLikelihoodDeg(np.degrees(orientation), self.rotation, self.SigmaIMU)
        
        self.weight = weight
        return weight

    def MaxWeight(self, landmarks=None, field=None, orientation=None):
        weight = 1
        if landmarks != None:
            for lm in landmarks:
                if lm != -999:
                    weight *= Walpha(0)
                    weight *= maxWdelta
                else:
                    weight *= 1 - Walpha(0)
                    weight *= 1 - maxWdelta
        print weight
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
        return np.exp(-d/(2*np.power(s,2)))

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
def prob(cx, cy, r, xa=0, xb=1040, ya=0, yb=740):
    w = 1

    if cx+r <= xa or cx-r >= xb:
        return 0
    elif cx-r < xa:
        w *= 0.5 - ((xa-cx)*np.sqrt((r**2)-(xa-cx)**2) + (r**2)*np.arctan((xa-cx)/(np.sqrt((r**2)-(xa-cx)**2))))/((r**2)*np.pi)
    elif cx+r > xb:
        w *= 0.5 + ((xb-cx)*np.sqrt((r**2)-(xb-cx)**2) + (r**2)*np.arctan((xb-cx)/(np.sqrt((r**2)-(xb-cx)**2))))/((r**2)*np.pi)

    if cy+r <= ya or cy-r >= yb:
        return 0
    elif cy-r < ya:
        w *= 0.5 - ((ya-cy)*np.sqrt((r**2)-(ya-cy)**2) + (r**2)*np.arctan((ya-cy)/(np.sqrt((r**2)-(ya-cy)**2))))/((r**2)*np.pi)
    elif cy+r > yb:
        w *= 0.5 + ((yb-cy)*np.sqrt((r**2)-(yb-cy)**2) + (r**2)*np.arctan((yb-cy)/(np.sqrt((r**2)-(yb-cy)**2))))/((r**2)*np.pi)

    return w

def Walpha(ang, gamma=26.13, Delta=90):
    if -Delta+gamma < ang and ang < Delta-gamma:
        return gamma/(Delta-gamma)
    elif ang < -Delta-gamma or ang > Delta+gamma:
        return 0
    else:
        return 0.5 * (Delta+gamma-np.abs(ang))/(Delta-gamma)

def Wdelta(dist, psi=0.7, SigmaO=70, MuF=700, SigmaF=10, MuN=10, SigmaN=1, SigmaA=30):
    return (psi + (1-psi)*np.exp(-np.power(dist,2)/(2*np.power(SigmaO,2)))) * (1 + sp.erf((MuF-dist)/(np.sqrt(2)*SigmaF))) * (1 - sp.erf((MuN-dist)/(np.sqrt(2)*SigmaN))) / 4

if maxWdelta == None:
    gamma = 26.13
    Delta = 90
    psi = 0.7
    SigmaO = 70
    MuF = 700
    SigmaF = 10
    MuN = 10
    SigmaN = 1
    SigmaA = 30
    radius = 20

    SigmaIMU = 30

    d = np.array([])
    for i in xrange(1000):
        d = np.append(d, [np.random.randint(MuN, MuF)])

    w = 0
    while True:
        p = w

        d = np.random.normal(d, 0.3)
        e = Wdelta(d)

        w = np.max(e)

        if np.abs(w-p) < 1e-3:
            d = d[np.argmax(e)]
            break

    maxWdelta = Wdelta(d)