import pygame

def help(screen):
    font = pygame.font.SysFont("Arial", 12)
    color = (255, 255, 255)
    s = pygame.Surface((250, 740))
    s.fill((0, 0, 0))
    s.set_alpha(200)
    screen.background.blit(s, (0, 0))
    font.set_bold(True)
    space = 17
    a = 5
    screen.background.blit(font.render('- HELP -', 1, color), (75, a))
    font.set_bold(False)
    a += space
    screen.background.blit(font.render('A - add a blue robot', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('CTRL+A - add a pink robot', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('LEFTSHIFT+A - add a yellow robot', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('RIGHTSHIFT+A - add a orange robot', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('LEFTALT+A - add a black robot', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('B - place ball', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('C - NOTHING', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('D - turn right', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('E - turn left', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('F - fast walk forward', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('G - NOTHING', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('H - NOTHING', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('I - pass to the left', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('J - pass to the right', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('K - slow walk forward', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('L - left kick', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('M - walk left', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('N - walk right', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('O - rotate around the ball - clockwise', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('P - right kick', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('Q - rotate around the ball - anticlockwise', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('R - slow walk backward', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('S - gait', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('T - stop', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('U - NOTHING', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('V - fast walk backward', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('W - NOTHING', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('X - NOTHING', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('Y - Search Ball', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('Z - Stop searching', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('1~9 - select robot 1 to 9', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('CTRL+0~6 - select robot 10 to 16', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('DELETE - delete robot', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('F1 - toggle help', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('F2 - load setup match archive', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('F3 - reset and load setup match', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('F4 - clean screen', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('F5 - toggle pause', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('F6 - toggle field of view', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('F7 - toggle EOPRA representation', 1, color), (10, a))
    a += space
    screen.background.blit(font.render('F8 - toggle StarVars representation', 1, color), (10, a))