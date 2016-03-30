import pygame

class Screen():
    def __init__(self):
        #Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 150, 0)
        self.BLUE = (0, 0, 200)
        self.RED = (255, 0, 0)
        self.MAGENTA = (190, 0, 190)
        self.CYAN = (0, 190, 190)
        self.YELLOW = (190, 190, 0)
        self.ORANGE = (229, 83, 0)
        self.GRAY = (128, 128, 128)

        self.screen_width = 1042
        self.screen_height = 742
        self.dimension = self.screen_width,self.screen_height
        self.background = pygame.display.set_mode(self.dimension)
        self.clock = pygame.time.Clock()
        self.KEY_BKB = 100

    def start_simulation(self):
        print 'RoboFEI-HT Simulator'
        pygame.init()
        pygame.display.set_caption('RoboFEI-HT- Soccer Simulator')
