import pygame
import simulation
import sys


#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
BLUE = (0, 0, 200)

print 'RoboFEI-HT Simulator'
pygame.init()

screen_width = 1040
screen_height = 740

dimension = screen_width, screen_height
screen = pygame.display.set_mode(dimension)
pygame.display.set_caption('RoboFEI-HT- Soccer Simulator')
clock = pygame.time.Clock()


