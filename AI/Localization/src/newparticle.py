__author__ = "RoboFEI-HT"
__authors__ = "Aislan C. Almeida"
__license__ = "GNU General Public License v3.0"

import numpy as np
import scipy.special as sp

# Robot's height!!!
hrobot = 50
# Robot's head's tilt's position
htilt = 17.4
hfov = 26.13
vfov = 14.58

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
            self.regions = ((0, 1040), (0, 740), (-180, 180))

        if x != None:
            self.x = x
        elif normals:
            self.x = np.random.normal(normals[0][0], normals[0][1])
        else:
            self.x = np.random.randint(self.regions[0][0], self.regions[0][1])

        if y != None:
            self.y = y
        elif normals:
            self.y = np.random.normal(normals[1][0], normals[1][1])
        else:
            self.y = np.random.randint(self.regions[1][0], self.regions[1][1])

        if rotation != None:
            self.rotation = rotation
        elif normals:
            self.rotation = np.random.normal(normals[2][0], normals[2][1])
        else:
            self.rotation = np.random.randint(self.regions[2][0], self.regions[2][1])
        
        self.weight = weight # Holds particles weight, can come from previous iterations
        
        # Motion error coefficients
        if factors == None:
            # self.factors = [1, 2, 1, 500, 10,  1, 2, 1, 500, 15,  1, 2, 1, 100, 10]
            # self.factors = 15*[0]
            self.factors = [1, 2, 1, 0, 10,  1, 2, 1, 0, 20,  1, 2, 1, 0, 10]
            # self.factors = [0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 100, 0]
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

        self.SigmaField = 0.01

        self.wfactor = wfactor # Used in order to implement the motion error.

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
    def Motion(self, straight=0, drift=0, rotational=0, dt=0):
        # straight is the robot's forward speed in cm/s
        # drift is the robot's sideways speed in cm/s
        # rotational is the robot's angular speed in degrees/s

        # wfactor = max(min(np.log(self.weight/self.maxweight)/np.log(1e-20), 1.), 0.)

        # Computes the forward speed with error
        Forward = straight + NRnd(self.factors[0]*straight) + NRnd(self.factors[1]*drift) + NRnd(self.factors[2]*rotational) + NRnd(self.factors[3] * self.wfactor) + NRnd(self.factors[4])
        # Computes the side speed with error
        Side = drift + NRnd(self.factors[5]*straight) + NRnd(self.factors[6]*drift) + NRnd(self.factors[7]*rotational) + NRnd(self.factors[8] * self.wfactor) + NRnd(self.factors[9])
        # Computes the angular speed with error
        Omega = rotational + NRnd(self.factors[10]*straight) + NRnd(self.factors[11]*drift) + NRnd(self.factors[12]*rotational) + NRnd(self.factors[13] * self.wfactor) + NRnd(self.factors[14])

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
    def Sensor(self, landmarks=None, field=None, orientation=None, weight=1):
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
            hpan = int(field) # Extract the pan angle
            points = 30.

            vec = np.array(self.RndGenerate(points)).transpose() # Takes the random generated angles
            green = 0 # Counts how many dots are green
            
            h = hrobot # Adds error to the robot's height
            pan = np.radians(hpan) # Adds error to the horizontal angles
            tilt = np.radians(htilt) # Adds error to the vertical angles

            for i in vec:
                dist = (h / np.tan(tilt + i[0]))/np.cos(i[1]) # Computes the point distance
                ang = - np.radians(self.rotation) + i[1] + pan # Computes the point angle
                px = self.x + dist * np.cos(ang) # Computes point x position
                py = self.y + dist * np.sin(ang) # Computes point y position

                if 0 <= px and px <= 1040 and 0 <= py and py <= 740:
                    # If the dot is "green", save it.
                    green += 1

            s =  max(0.001, min(0.999, green/points))

            weight *= np.exp(-(np.power(s-np.abs(field)+np.abs(hpan), 2))/(2*np.power(self.SigmaField,2)))

        # If the IMU's orientation was given
        if orientation != None:
            weight *= ComputeAngLikelihoodDeg(np.degrees(orientation), self.rotation, self.SigmaIMU)
        
        self.weight = max(weight, 1e-300)
        if landmarks != None and field != None and orientation != None:
            self.wfactor = max(min(np.log(self.weight)/np.log(1e-20), 1.), 0.)
        return self.weight

    def RndGenerate(self, n):
        # Generate n random points
        vrnd = np.random.random([n]) 
        hrnd = np.random.random([n]) 
        hp = np.arctan((1.9*hrnd-0.95) * np.tan(np.radians(hfov))) # Converts to "screen coordinates"
        vp = np.arctan(1/((0.9*vrnd+0.05)*(1/np.tan(np.radians(htilt-vfov))-1/np.tan(np.radians(htilt+vfov)))+1/np.tan(np.radians(htilt+vfov))))-np.radians(htilt)
        # Computes and returns the random generated angles
        return vp, hp

    def Sight(self, angle):
        hpan = angle # Extract the pan angle
        points = 1000.

        vec = np.array(self.RndGenerate(points)).transpose() # Takes the random generated angles
        green = 0 # Counts how many dots are green
        
        h = hrobot # Adds error to the robot's height
        pan = np.radians(hpan) # Adds error to the horizontal angles
        tilt = np.radians(htilt) # Adds error to the vertical angles

        for i in vec:
            dist = (h / np.tan(tilt + i[0]))/np.cos(i[1]) # Computes the point distance
            ang = - np.radians(self.rotation) + i[1] + pan # Computes the point angle
            px = self.x + dist * np.cos(ang) # Computes point x position
            py = self.y + dist * np.sin(ang) # Computes point y position

            if 0 <= px and px <= 1040 and 0 <= py and py <= 740:
                # If the dot is "green", save it.
                green += 1

        s =  max(0.001, min(0.999, green/points))
        if pan < 0:
            return pan - s
        else:
            return pan + s
        
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
#   Computes the Wdelta factor for weight computation
#--------------------------------------------------------------------------------------------------
def Wdelta(dist, psi=0.7, SigmaO=70, MuF=700, SigmaF=10, MuN=10, SigmaN=1):
    return (psi + (1-psi)*np.exp(-np.power(dist,2)/(2*np.power(SigmaO,2)))) * (1 + sp.erf((MuF-dist)/(np.sqrt(2)*SigmaF))) * (1 - sp.erf((MuN-dist)/(np.sqrt(2)*SigmaN))) / 4