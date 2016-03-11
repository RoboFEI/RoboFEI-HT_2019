import pygame

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
BLUE = (0, 0, 200)

pygame.init()

screen_width = 1040
screen_height = 740

dimension = screen_width, screen_height

robots_group = pygame.sprite.Group()

screen = pygame.display.set_mode(dimension)
pygame.display.set_caption('RoboFEI-HT- Soccer Simulator')

robofei_logo = pygame.image.load("RoboFEI_logo.png")
robofei_logo = pygame.transform.scale(robofei_logo,(100,82))
pygame.display.set_icon(robofei_logo)

clock = pygame.time.Clock()

def draw_soccer_field():
    #background is green
    screen.fill([0,150,0])

    #field lines
    field_points = [(70,70),(520,70),(520,670),(970,670),(970,542),(910,542),(910,197),(970,197),(970,542),(970,70),(520,70),(520,670),(70,670),(70,542),(130,542),(130,197),(70,197),(70,542),(70,70)]
    pygame.draw.lines(screen,(255,255,255), False, field_points, 5)

    #areas
    pygame.draw.line(screen,(255,255,255),(245,370),(255,370), 7)
    pygame.draw.line(screen,(255,255,255),(250,365),(250,375), 7)

    #central circle
    pygame.draw.circle(screen,(255,255,255),(520,370),75,5)

    #penalty marks
    pygame.draw.line(screen,(255,255,255),(775,370),(785,370), 7)
    pygame.draw.line(screen,(255,255,255),(780,365),(780,375), 7)

    pygame.draw.line(screen,(255,255,255),(515,370),(525,370), 7)
    pygame.draw.line(screen,(255,255,255),(520,365),(520,375), 7)

    #text
    font = pygame.font.Font(None, 36)
    text = font.render("RoboFEI-HT Simulator", 1, (255, 255, 255))
    textpos = text.get_rect()
    textpos.centery = 30
    textpos.centerx = screen.get_rect().centerx
    screen.blit(text, textpos)
    screen.blit(robofei_logo,(950,2))