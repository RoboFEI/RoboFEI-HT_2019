import pygame

class Screen():
    def __init__(self):
        #Colors
        self.screen_width = 1040
        self.screen_height = 740
        self.background = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        print 'Localization Graphical Viewer'
        pygame.init()
        pygame.display.set_caption('Localization Graphical Viewer')
