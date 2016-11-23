__author__ = "RoboFEI-HT"
__authors__ = "Aislan C. Almeida"
__license__ = "GNU General Public License v3.0"

from math import *
import random as rnd
from particle import *

#--------------------------------------------------------------------------------------------------
#   This class implements the Monte Carlo's Particle Filter
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

        self.totalweight = 0

    #----------------------------------------------------------------------------------------------
    #   Prediction step
    #----------------------------------------------------------------------------------------------
    def Prediction(self, u=None):
        # If there was movement, run the predction step
        if u != None:
            for particle in self.particles:
                particle.Motion(u[0], u[1], u[2])

    #----------------------------------------------------------------------------------------------
    #   Update step
    #----------------------------------------------------------------------------------------------
    def Update(self, z=None):
        # If there was any measure, run the update step
        if z != None:
            for particle in self.particles:
                self.totalweight += particle.Sensor(z)

    
    #----------------------------------------------------------------------------------------------
    #   Resample step
    #----------------------------------------------------------------------------------------------
    def Resample(self, qtd):
        parts = [] # Starts a empty list.

        step = self.totalweight / qtd # Computes the step size
        s = step/2 # the first step is given by half the total.

        for p in self.particles: # For each particle,
            while s < p.weight: # while the particles weight is grater than the step,
                s += step # rises the step size,
                parts.append(Particle(p.x, p.y, p.rotation)) # adds the particle to the list.
            s -= p.weight # Removes the used steps.

        self.particles = parts # Overwrites the previous particles.

    #----------------------------------------------------------------------------------------------
    #   Main algorithm
    #----------------------------------------------------------------------------------------------
    def main(self, u=None, z=None):
        self.Prediction(u)
        self.Update(z)
        self.Resample(self.max_qtd)