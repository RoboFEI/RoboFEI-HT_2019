import sys
import time
import pygame
from math import cos
from math import sin
from math import radians


pygame.init()

screen_width = 1040
screen_height = 740

dimension = screen_width, screen_height

tela = pygame.display.set_mode(dimension)
pygame.display.set_caption('RoboFEI-HT- Soccer Simulator')


robofei_logo = pygame.image.load("RoboFEI_logo.png")
robofei_logo = pygame.transform.scale(robofei_logo,(100,82))
pygame.display.set_icon(robofei_logo)

clock = pygame.time.Clock()

#sound = pygame.mixer.music

#sound.load("musica.mp3")

#sound.set_volume(0.1)


x = 100
y = 100

wall = 1
ceiling = 1

pygame.display.flip()


def draw_soccer_field():

    tela.fill([0,150,0])

    field_points = [(70,70),(520,70),(520,670),(970,670),(970,542),(910,542),(910,197),(970,197),(970,542),(970,70),(520,70),(520,670),(70,670),(70,542),(130,542),(130,197),(70,197),(70,542),(70,70)]
    pygame.draw.lines(tela,(255,255,255), False, field_points, 5)
    pygame.draw.line(tela,(255,255,255),(245,370),(255,370), 7)
    pygame.draw.line(tela,(255,255,255),(250,365),(250,375), 7)

    pygame.draw.line(tela,(255,255,255),(515,370),(525,370), 7)
    pygame.draw.line(tela,(255,255,255),(520,365),(520,375), 7)

    pygame.draw.circle(tela,(255,255,255),(520,370),75,5)

    pygame.draw.line(tela,(255,255,255),(775,370),(785,370), 7)
    pygame.draw.line(tela,(255,255,255),(780,365),(780,375), 7)

    font = pygame.font.Font(None, 36)
    text = font.render("RoboFEI-HT Simulator", 1, (255, 255, 255))
    textpos = text.get_rect()
    textpos.centery = 30
    textpos.centerx = tela.get_rect().centerx
    tela.blit(text, textpos)
    tela.blit(robofei_logo,(950,2))



def draw_robot(x,y,theta):
    pygame.draw.circle(tela,(0,0,0),(x,y),22,0)
    pygame.draw.circle(tela,(0,0,200),(x,y),20,0)
    x_theta = cos(theta)*20
    y_theta = sin(theta)*20
    pygame.draw.line(tela,(0,0,0),(x,y),(x_theta+x,y_theta+y),3)
    font = pygame.font.Font(None, 20)
    text = font.render("B1", 1, (10, 10, 10))
    textpos = (x-5,y-40)
    #tela.blit(robot,(x,y))
    tela.blit(text, textpos)

def draw_ball(x,y):
    pygame.draw.circle(tela,(255,255,255),(x,y),10,0)

rotate = 0
ball = False
x_ball, y_ball = -10, -10
front = 0

while 1:

    mx, my = pygame.mouse.get_pos()
    #print mx, my

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            rotate += 45 % 360
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            rotate -= 45 % 360

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            front = 1

        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            front = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            front = -1

        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            front = 0


        if event.type == pygame.MOUSEBUTTONDOWN:
            print 'bola'
            ball = True


        #if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
        #    robot = pygame.transform.rotate(robot,45)

        if event.type == pygame.QUIT:
            sys.exit()



    draw_soccer_field()

    x = x + cos(radians(rotate))*front
    y = y + sin(radians(rotate))*front

    if x > 1040:
       x = 1040
    elif x < 0:
        x = 0

    if y > 740:
        y = 740
    elif y < 0:
        y = 0

    draw_robot(int(x),int(y),radians(rotate))

    if ball == True:
        x_ball = mx
        y_ball = my
        ball = False

    draw_ball(x_ball,y_ball)

    pygame.display.flip()

    clock.tick(60)


