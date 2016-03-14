from init import *

class SoccerField():
    def __init__(self):
        self.robofei_logo = pygame.image.load("RoboFEI_logo.png")
        self.robofei_logo_scaled = pygame.transform.scale(self.robofei_logo,(100,82))

    def draw_soccer_field(self):
        #background is green
        screen.fill(GREEN)

        #field lines
        field_points = [(70,70),(520,70),(520,670),(970,670),(970,542),(910,542),(910,197),(970,197),(970,542),(970,70),(520,70),(520,670),(70,670),(70,542),(130,542),(130,197),(70,197),(70,542),(70,70)]
        pygame.draw.lines(screen,WHITE, False, field_points, 5)

        #areas
        pygame.draw.line(screen,WHITE,(245,370),(255,370), 7)
        pygame.draw.line(screen,WHITE,(250,365),(250,375), 7)

        #central circle
        pygame.draw.circle(screen,WHITE,(520,370),75,5)

        #penalty marks
        pygame.draw.line(screen,WHITE,(775,370),(785,370), 7)
        pygame.draw.line(screen,WHITE,(780,365),(780,375), 7)

        pygame.draw.line(screen,WHITE,(515,370),(525,370), 7)
        pygame.draw.line(screen,WHITE,(520,365),(520,375), 7)

        #text
        font = pygame.font.Font(None, 36)
        text = font.render("RoboFEI-HT Simulator", 1, WHITE)
        textpos = text.get_rect()
        textpos.centery = 30
        textpos.centerx = screen.get_rect().centerx
        screen.blit(text, textpos)
        screen.blit(self.robofei_logo_scaled,(950,2))
