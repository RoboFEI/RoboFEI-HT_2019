__author__ = "RoboFEI-HT"
__authors__ = "Aislan C. Almeida"
__license__ = "GNU General Public License v3.0"

from math import *
import random as rnd
import pygame


class Particle: # Class implementing a particle
    def __init__(self, x = '', y = '', r = ''): # Constructor
        if x == '':
            self.x = rnd.randrange(70, 970) # Starts at a random X position
        else:
            self.x = x                      # Starts at a given X position

        if y == '':
            self.y = rnd.randrange(70, 670) # Starts at a random Y position
        else:
            self.y = y                      # Starts at a given Y position

        if r == '':
            self.r = rnd.randrange(0, 360) # Starts at a random orientation
        else:
            self.r = r                     # Starts at a given orientation

        self.w = 1 # Particle's weight

        self.rotation_sigma = 0 # Used for errors
        self.moving_sigma = 0   # Used for errors

        self.color = (0,0,0)

    def MotionModel(self, x_motion = 0, y_motion = 0, rotation = 0):
        # Adds motion errors
        x_motion += rnd.gauss(0, self.moving_sigma)
        y_motion += rnd.gauss(0, self.moving_sigma)
        rotation += rnd.gauss(0, self.rotation_sigma)

        self.x += x_motion # Moves in X
        self.y += y_motion # Moves in Y
        self.r += rotation # Rotates

    def ObservationModel(self, measures, static_landmarks, dynamic_landmarks):
        self.w = 1 # Initializes particles weight

        for m in measures: # For each measure

            if m[0] == 0: # Likelihood of orientation {type, reference_angle, sigma}
                self.w *= AngleLikelihood(radians(self.r), radians(m[1]), m[2])

            elif m[0] == 1: # Likelihood of static landmarks {type, landmark_type, landmark_number, reference_distance, sigma}

                if m[1] != 0 and m[1] != 1: # If it is known what kind of static landmark

                    if m[2] != 0: # If it is known which landmark
                        # Just compute the likelihood
                        d = hypot(self.x-static_landmarks[m[1]-1][m[2]-1][0], self.y-static_landmarks[m[1]-1][m[2]-1][1])
                        self.w *= Gauss(d, m[3], m[4])

                    else: # Try all landmarks of given type
                        w = 0
                        for lm in static_landmarks[m[1]-1]:
                            d = hypot(self.x-lm[0], self.y-lm[1])
                            p = Gauss(d, m[3], m[4])
                            if p > w: # Assumes the one with the greatest likelihood is the seen landmark
                                w = p
                        self.w *= w

                elif m[1] == 1: # If it is a field border landmark
                    w = 0
                    if m[2] == 0: # If it is a unknown border
                        distances = [self.x, 1040-self.x, self.y, 740-self.y]
                        for d in distances: # Tests all border
                            p = Gauss(d, m[3], m[4])
                            if p > w: # Gets the one with the greatest likelihood
                                w = p

                    elif m[2] == 1: # It is the defense goal side
                        w = Gauss(self.x, m[3], m[4])

                    elif m[2] == 2: # It is the attack goal side
                        w = Gauss(1040-self.x, m[3], m[4])

                    elif m[2] == 3: # It is the left side
                        w = Gauss(self.y, m[3], m[4])

                    elif m[2] == 4: # It is the right side
                        w = Gauss(740-self.y, m[3], m[4])
                    self.w *= w


                else: # Try all static landmarks
                    w = 0
                    for tp in static_landmarks:
                        for lm in tp:
                            d = hypot(self.x-lm[0], self.y-lm[1])
                            p = Gauss(d, m[3], m[4])
                            if p > w: # Assumes the one with the greatest likelihood is the seen landmark
                                w = p
                    self.w *= w

            elif m[0] == 2: # Likelihood of static landmarks using angles {type, landmark_type, landmark_number, reference_angle, sigma}

                if m[1] != 0 and m[1] != 1: # If it is known what kind of static landmark

                    if m[2] != 0: # If it is known which landmark
                        # Just compute the likelihood
                        t = atan2(self.y-static_landmarks[m[1]-1][m[2]-1][1], self.x-static_landmarks[m[1]-1][m[2]-1][0])
                        self.w *= AngleLikelihood(t, radians(m[3]), m[4])

                    else: # Try all landmarks of given type
                        w = 0
                        for lm in static_landmarks[m[1]-1]:
                            t = atan2(self.y-lm[1], self.x-lm[0])
                            p = AngleLikelihood(t, radians(m[3]), m[4])
                            if p > w: # Assumes the one with the greatest likelihood is the seen landmark
                                w = p
                        self.w *= w

                elif m[1] == 1: # If it is a field border landmark
                    w = 0
                    if m[2] == 0: # If it is a unknown border
                        angles = [180-self.r, -self.r, 90-self.r, -90-self.r]
                        for a in angles: # Tests all border
                            p = AngleLikelihood(radians(a), radians(m[3]), m[4])
                            if p > w: # Gets the one with the greatest likelihood
                                w = p

                    elif m[2] == 1: # It is the defense goal side
                        w = AngleLikelihood(radians(180-self.r), radians(m[3]), m[4])

                    elif m[2] == 2: # It is the attack goal side
                        w = AngleLikelihood(radians(-self.r), radians(m[3]), m[4])

                    elif m[2] == 3: # It is the left side
                        w = AngleLikelihood(radians(90-self.r), radians(m[3]), m[4])

                    elif m[2] == 4: # It is the right side
                        w = AngleLikelihood(radians(-90-self.r), radians(m[3]), m[4])
                    self.w *= w

                else: # Try all static landmarks
                    w = 0
                    for tp in static_landmarks:
                        for lm in tp:
                            t = atan2(self.y-lm[1], self.x-lm[0])
                            p = AngleLikelihood(t, radians(m[3]), m[4])
                            if p > w: # Assumes the one with the greatest likelihood is the seen landmark
                                w = p
                    self.w *= w

            elif m[0] == 3: # Likelihood of the ball {type, distance, angle}

                # Computes the possible ball position through the input data in relation to the particle.
                x = self.x + m[1] * cos(radians(m[2]))
                y = self.y + m[1] * sin(radians(m[2]))

                # Gets the mean position of the ball
                bx = dynamic_landmarks[0][0]
                by = dynamic_landmarks[0][1]
                bsigma = dynamic_landmarks[0][2]

                # Compute likelihood
                self.w *= BDGauss([x,y], [bx,by], bsigma)

            elif m[0] == 4: # Likelihood of the friendly robots {type, distance, angle}

                # Computes the robot seen position in relation to the particle
                x = self.x + m[1] * cos(radians(m[2]))
                y = self.y + m[1] * sin(radians(m[2]))

                # For all friendly robots computing their respectives
                w = []
                for rbt in dynamic_landmarks[1]:
                    w.append(BDGauss([x,y], [rbt[0],rbt[1]], rbt[2]))

                # Gets the maximum one
                self.w *= max(w)

            elif m[0] == 5: # Likelihood of the opponent robots {type, distance, angle}
                pass




    def SetErrors(self, moving_error = 0, rotation_error = 0):
        self.moving_sigma = moving_error
        self.rotation_sigma = rotation_error

    def Draw(self, where):
        px = 5 * cos(radians(self.r)) + self.x
        py = 5 * sin(radians(self.r)) + self.y

        pygame.draw.line(where, self.color, (int(self.x), int(self.y)), (int(px), int(py)), 1)
        pygame.draw.circle(where, self.color, (int(self.x), int(self.y)), 2, 0)

def Gauss(x, mu, sigma):
    if sigma == 0:
        if x == mu:
            return 1
        else:
            return 0
    else:
        return exp(-(x-mu)**2/(2 * sigma**2))/sqrt(2*pi * sigma**2)

def AngleLikelihood(alpha, theta, sigma): # Angles in radians
    x, y = cos(alpha), sin(alpha)
    xr, yr = cos(theta), sin(theta)
    return Gauss(hypot(x-xr, y-yr), 0, sigma)

def BDGauss(x, mu, sigma):
    if sigma == 0:
        if x[0] == mu[0] and x[1] == mu[1]:
            return 1
        else:
            return 0
    else:
        return  exp(-hypot(x[0]-mu[0], x[1]-mu[1])**2/(2*sigma**2))/sqrt(2*pi*sigma**2)