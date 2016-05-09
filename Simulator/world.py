from screen import *

class SoccerField():
    def __init__(self, screen):
        self.screen = screen
        self.robofei_logo_scaled = pygame.image.load("RoboFEI_scaled80.png")
        self.goalpost_list = []
        self.goalpost = GoalPosts(70,280)
        self.goalpost_list.append(self.goalpost)
        self.goalpost = GoalPosts(70,460)
        self.goalpost_list.append(self.goalpost)
        self.goalpost = GoalPosts(970,280)
        self.goalpost_list.append(self.goalpost)
        self.goalpost = GoalPosts(970,460)
        self.goalpost_list.append(self.goalpost)

        self.LimitLines = []
        self.LimitLines.append(LimitLine(0, 1040, 0))
        self.LimitLines.append(LimitLine(0, 1040, 740))
        self.LimitLines.append(LimitLine(0, 740, 0, False))
        self.LimitLines.append(LimitLine(0, 740, 1040, False))
        self.LimitLines.append(LimitLine(0, 70, 280))
        self.LimitLines.append(LimitLine(0, 70, 460))
        self.LimitLines.append(LimitLine(970, 1040, 280))
        self.LimitLines.append(LimitLine(970, 1040, 460))

        self.Goals = []
        self.Goals.append(SpecialArea(0, 280, 70, 460, True, 'Friend'))
        self.Goals.append(SpecialArea(970, 280, 1040, 460, True, 'Enemy'))

        self.PlayField = SpecialArea(70, 70, 970, 670)

        self.FriendTeam = 'ROBOFEI-HT'
        self.EnemyTeam = 'OTHERS'
        self.FriendGoals = 0
        self.EnemyGoals = 0
        self.GameStop = True
        self.Counter = 0
        self.Lap = 0
        self.show = True

    def draw_soccer_field(self):

        #background is green
        self.screen.background.fill(self.screen.GREEN)

        #field lines
        field_points = [(70,70),(520,70),(520,670),(970,670),(970,542),(910,542),(910,197),(970,197),(970,542),(970,70),(520,70),(520,670),(70,670),(70,542),(130,542),(130,197),(70,197),(70,542),(70,70)]
        pygame.draw.lines(self.screen.background,self.screen.WHITE, False, field_points, 5)

        #areas
        pygame.draw.line(self.screen.background,self.screen.WHITE,(245,370),(255,370), 7)
        pygame.draw.line(self.screen.background,self.screen.WHITE,(250,365),(250,375), 7)

        #central circle
        pygame.draw.circle(self.screen.background,self.screen.WHITE,(520,370),75,5)

        #penalty marks
        pygame.draw.line(self.screen.background,self.screen.WHITE,(775,370),(785,370), 7)
        pygame.draw.line(self.screen.background,self.screen.WHITE,(780,365),(780,375), 7)

        pygame.draw.line(self.screen.background,self.screen.WHITE,(515,370),(525,370), 7)
        pygame.draw.line(self.screen.background,self.screen.WHITE,(520,365),(520,375), 7)

        #goalsposts
        for post in self.goalpost_list:
            post.draw_goalposts(self.screen)

        #limit lines
        for ll in self.LimitLines:
            ll.draw_LimitLine(self.screen)


        #text
        font = pygame.font.SysFont("Arial", 20)
        txt = self.FriendTeam + ' ' + str(self.FriendGoals) + ' x ' + str(self.EnemyGoals) + ' ' + self.EnemyTeam
        text = font.render(txt, 1, self.screen.WHITE)
        textpos = text.get_rect()
        textpos.centery = 30
        textpos.centerx = self.screen.background.get_rect().centerx

        self.screen.background.blit(text, textpos)

        #time
        if self.GameStop:
            tick = pygame.time.get_ticks()
            if tick - self.Lap > 300:
                self.show = not self.show
                self.Lap = tick
        else:
            self.show = True

        if self.show:
            minutes = int(self.Counter / 60000)
            seconds = int(self.Counter / 1000) - minutes * 60
            if minutes < 10:
                mnt = '0' + str(minutes)
            else:
                mnt = str(minutes)

            if seconds < 10:
                snd = '0' + str(seconds)
            else:
                snd = str(seconds)

            txt = mnt + ':' + snd
            text = font.render(txt, 1, self.screen.WHITE)
            textpos = text.get_rect()
            textpos.centery = 50
            textpos.centerx = self.screen.background.get_rect().centerx

            self.screen.background.blit(text, textpos)

        self.screen.background.blit(self.robofei_logo_scaled,(965,2))

class GoalPosts(SoccerField):
    def __init__(self,x,y):
        self.radius = 10 #10cm
        self.x = x
        self.y = y

    def draw_goalposts(self, screen):
        '''draw goalposts'''
        pygame.draw.circle(screen.background,screen.WHITE,(self.x,self.y),self.radius,0)

class LimitLine(SoccerField):
    def __init__(self, a0, a1, b, cte_y = True):
        # True means y constant
        # False means x constante
        self.a0 = a0
        self.a1 = a1
        self.b = b
        self.cte_y = cte_y

    def draw_LimitLine(self, screen):
        if self.cte_y:
            pygame.draw.line(screen.background, screen.WHITE, (self.a0, self.b), (self.a1, self.b), 2)
        else:
            pygame.draw.line(screen.background, screen.WHITE, (self.b, self.a0), (self.b, self.a1), 2)

class SpecialArea(SoccerField):
    def __init__(self, x1, y1, x2, y2, goal = False, side = 'None'):
        # True for goal
        # False for field
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.goal = goal
        self.side = side