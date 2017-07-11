# from particle import *
import pygame
import sys
import numpy as np

class Simulation():
    def __init__(self, screen):
        self.mx = 0
        self.my = 0
        self.screen = screen

        self.field = None

    def perform_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def display_update(self, particles):
        
        for particle in particles:
            xi = particle.x
            yi = particle.y
            xm = xi + 2 * np.cos(np.radians(particle.rotation))
            ym = yi - 2 * np.sin(np.radians(particle.rotation))
            xf = xm + 3 * np.cos(np.radians(particle.rotation))
            yf = ym - 3 * np.sin(np.radians(particle.rotation))
            pygame.draw.line(self.screen.background,(0,0,0),(xi,yi),(xm,ym), 1)
            pygame.draw.line(self.screen.background,(0,0,255),(xm,ym),(xf,yf), 1)

        pygame.display.flip()

    def DrawStd(self, pos, std, weight, head):
        x = int(pos[0])
        y = int(pos[1])

        std = max(int(std * 10),7)

        # w = 3 * max(min(np.log(weight)/np.log(1e-20), 1.), 0.)
        w = 3. * weight

        r = np.rint(255. * max(min(w-2., 1.), 0.))
        g = np.rint(255. * max(min(w-1., 1.), 0.))
        b = np.rint(255. * max(min(w, 1.), 0.))

        i = int(x + std * np.cos(np.radians(pos[2])))
        j = int(y - std * np.sin(np.radians(pos[2])))

        if head != -999:
            m = int(x + std * np.cos(np.radians(-head+pos[2])))
            n = int(y - std * np.sin(np.radians(-head+pos[2])))
            pygame.draw.circle(self.screen.background, (r,g,b), (m,n), 10, 3)

        pygame.draw.line(self.screen.background, (r,g,b), (x,y), (i,j), 5)
        pygame.draw.circle(self.screen.background,(r,g,b),(x,y), std, 5)