__author__ = "RoboFEI-HT"
__authors__ = "Aislan C. Almeida"
__license__ = "GNU General Public License v3.0"

from math import *
import random as rnd
import pygame

#--------------------------------------------------------------------------------------------------
#   Class implementing a particle used on Particle Filter Localization
#--------------------------------------------------------------------------------------------------

class Particle(object):
    #----------------------------------------------------------------------------------------------
    #   Particle constructor
    #----------------------------------------------------------------------------------------------
    def __init__(self, x = None, y = None, rotation = None, weight = 0, normals = None, regions = None):
        
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

        if not regions:
            regions = ((0, 900), (0, 600), (-180, 180))

        if x:
            self.x = x
        elif normals:
            self.x = rnd.gauss(normals[0][0], normals[0][1])
        else:
            self.x = rnd.randint(regions[0][0], regions[0][1])

        if y:
            self.y = y
        elif normals:
            self.y = rnd.gauss(normals[1][0], normals[1][1])
        else:
            self.y = rnd.randint(regions[1][0], regions[1][1])

        if rotation:
            self.rotation = rotation
        elif normals:
            self.rotation = rnd.gauss(normals[2][0], normals[2][1])
        else:
            self.rotation = rnd.randint(regions[2][0], regions[2][1])
        
        self.weight = weight

        