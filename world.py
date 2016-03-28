from screen import *

class SoccerField():
    def __init__(self, screen):
        self.screen = screen
        self.robofei_logo = pygame.image.load("RoboFEI_logo.png")
        self.robofei_logo_scaled = pygame.transform.scale(self.robofei_logo,(80,80))
        self.goalpost_list = []
        self.goalpost = GoalPosts(70,280)
        self.goalpost_list.append(self.goalpost)
        self.goalpost = GoalPosts(70,460)
        self.goalpost_list.append(self.goalpost)
        self.goalpost = GoalPosts(970,280)
        self.goalpost_list.append(self.goalpost)
        self.goalpost = GoalPosts(970,460)
        self.goalpost_list.append(self.goalpost)



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


        #text
        font = pygame.font.SysFont("Arial", 20)
        text = font.render("RoboFEI-HT Simulator", 1, self.screen.WHITE)
        textpos = text.get_rect()
        textpos.centery = 30
        textpos.centerx = self.screen.background.get_rect().centerx

        self.screen.background.blit(text, textpos)
        self.screen.background.blit(self.robofei_logo_scaled,(950,2))


class GoalPosts(SoccerField):
    def __init__(self,x,y):
        self.radius = 10 #10cm
        self.x = x
        self.y = y

    def draw_goalposts(self, screen):
        '''draw goalposts'''
        pygame.draw.circle(screen.background,screen.WHITE,(self.x,self.y),self.radius,2)

