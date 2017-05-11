__author__ = "RoboFEI-HT"
__authors__ = "Aislan C. Almeida"
__license__ = "GNU General Public License v3.0"

import numpy as np
from newparticle import *

#--------------------------------------------------------------------------------------------------
#   This class implements the Monte Carlo's Particle Filter
#   - Note that this is the most simples version of Monte Carlo Localization
#--------------------------------------------------------------------------------------------------

class MonteCarlo():
    #----------------------------------------------------------------------------------------------
    #   Constructor of the particle filter
    #----------------------------------------------------------------------------------------------
    def __init__(self, max_qtd=0):
        # Holds the particles objects
        self.particles = []

        # Limits the quantity of particles the filter will have
        self.max_qtd = max_qtd

        # Initializes with the max quantity of particles
        self.qtd = max_qtd

        for i in range(self.qtd):
            # Randomly generates n particles
            self.particles.append(Particle())
            # self.particles.append(Particle(100,500,90))
        
        self.totalweight = 0. # Holds the total sum of particles' weights.
        self.maxweight = 1.
        self.meanweight = 0

        self.mean = [0, 0, 0] # Holds the mean position of the estimated position.
        self.std = 1.

        self.VQPsigma = 3
        self.VQPmean = 10

    #----------------------------------------------------------------------------------------------
    #   Prediction step
    #----------------------------------------------------------------------------------------------
    def Prediction(self, u=None):
        # If there was movement, run the prediction step
        if u != None:
            for particle in self.particles:
                particle.Movement(*u)

    #----------------------------------------------------------------------------------------------
    #   Update step
    #----------------------------------------------------------------------------------------------
    def Update(self, z=None):
        # Clears the last total weight
        self.totalweight = 0

        # Computes the max weight.
        self.maxweight = self.particles[0].MaxWeight(*z)

        # Applies the observation model to each particle
        for particle in self.particles:
            w = particle.Sensor(*z)
            self.totalweight += w # Sum the weight

    #----------------------------------------------------------------------------------------------
    #   Resample step
    #----------------------------------------------------------------------------------------------
    def Resample(self, qtd):
        parts = [] # Starts a empty list.

        np.random.shuffle(self.particles) # Shuffles the particles in place.

        step = self.totalweight / (qtd + 1.) # Computes the step size
        s = 0 # the first step is given by half the total.

        poses = [] # Holds all positions to compute the standard deviation

        i = 1 # Counts the quantity of selected particles
        j = len(self.particles) # Counts down the quantity of particles
        # Until the quantity of particles is reached or there are no more particles to be selected
        self.meanweight = 0
        while i <= qtd and j >= 0: 
            # If the cumulative sum of steps is bigger than the cumulative sum of weights
            if step * i > s:
                j -= 1 # Change the particle to be tested
                s += self.particles[j].weight # Compute the new cumulative weight
            else:
                i += 1 # Moves one step
                p = self.particles[j] # Gets the particle
                parts.append(Particle(*p.copy(), maxweight=self.maxweight)) # adds the particle to the list.
                self.meanweight += p.weight

                # Saves the position for computing the standard deviation
                poses.append([p.x, p.y, np.cos(np.radians(p.rotation))+np.sin(np.radians(p.rotation))*1j])

        self.particles = parts # Overwrites the previous particles.
        self.qtd = len(self.particles) # Saves the new quantity of particles.
        self.meanweight /= self.qtd

        m = np.mean(poses, 0) # Computes the mean of the particles.
        
        self.mean[0] = int(np.real(m[0])) # Get the mean x
        self.mean[1] = int(np.real(m[1])) # Get the mean y
        self.mean[2] = int(np.angle(m[2], True)) # Get the mean angle

        poses = np.matrix(poses-m) # Compute the position error of each particle

        # Compute the standard deviation of the particle set
        self.std = np.power(np.sqrt(np.abs(np.linalg.det(((poses.T * poses) / self.qtd)))), 1/3.)

    #----------------------------------------------------------------------------------------------
    #   Tests which is the best information to be acquired.
    #----------------------------------------------------------------------------------------------
    def PerfectInformation(self, u, hp, time=0):
        if u[3] <= 1:
            np.random.shuffle(self.particles) # Shuffles the particle set.
            parts = [] 
            
            # Takes the first 30 particles of the set
            for P in self.particles[0:30]:
                parts.append(Particle(*P.copy()[0:2], weight=1, maxweight=1))
            
            # Moves the particles for a time!
            uf = [u[0], u[1], u[2], time]
            for P in parts:
                P.Motion(*uf)

            # For each possible observation, compute its utility
            pos = [90, 60, 30, 0, -30, -60, -90]
            uv = []
            for i in pos:
                aux = - np.abs(hp - i) * 7./180. + 7.
                
                d = [i, parts[0].GetDistances(i)]
                tw = 0
                # Computes the particles weight
                for p in parts:
                    tw += p.Sensor(distances=d)

                # "Resamples"
                s = tw/31.

                i = 1
                j = 0
                w = parts[0].weight
                sj = None
                k = 0
                while i < 31.:
                    if s * i > w:
                        j += 1
                        w += parts[j].weight
                    else:
                        i += 1
                        if sj != j:
                            sj = j
                            k += 1
                
                # Weight Standard Deviation
                w = np.array([i.weight for i in parts])
                std = np.sum(np.max(w) - w)
               
                aux += std
                # Counts the losses
                aux += 30-k
                uv.append(aux)
###################################################################################################
                print std, aux, k
###################################################################################################                
            return pos[np.argmax(uv)]
        return -999

    #----------------------------------------------------------------------------------------------
    #   Main algorithm
    #----------------------------------------------------------------------------------------------
    def main(self, u=None, z=None):
        self.Prediction(u) # Executes the prediction
        self.Update(z) # Updates particles' weights
        self.Resample(self.qtd) # Resamples the particles
        self.qtd = Qtd(self.std, maxi=self.max_qtd) # Computes the quantity based on the standard deviation
        
        return self.mean, self.std # Returns everything.

#--------------------------------------------------------------------------------------------------
#   Computes the quantity of particles in function of the standard deviation
#--------------------------------------------------------------------------------------------------
def Qtd(std, mean=6, sigma=2, mini=30, maxi=1000):
    # return np.rint(mini + (maxi-mini)/2. * (1 + sp.erf((std-mean)/(np.sqrt(2)*sigma))))
    return np.rint(np.max([mini, np.min([maxi, std * (maxi-mini)/(4.*sigma) + mini + (maxi-mini)/2. - (maxi-mini)*mean/(4.*sigma)])]))