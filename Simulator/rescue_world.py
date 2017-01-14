from screen import *
from world import *

class Rescue_World():
    def __init__(self, screen):
        self.screen = screen
        self.robofei_logo_scaled = pygame.image.load("RoboFEI_scaled80.png")
        self.goalpost_list = []
        goalpost = GoalPosts(500,300)
        goalpost.radius = 70
        goalpost.color = (130,130,100)
        self.goalpost_list.append(goalpost)
        goalpost = GoalPosts(500,400)
        goalpost.radius = 100
        goalpost.color = (130,130,100)
        self.goalpost_list.append(goalpost)

        self.LimitLines = []
        self.LimitLines.append(LimitLine(0, 1040, 0))
        self.LimitLines.append(LimitLine(0, 1040, 740))
        self.LimitLines.append(LimitLine(0, 740, 0, False))
        self.LimitLines.append(LimitLine(0, 740, 1040, False))

        self.Goals = []
        self.PlayField = SpecialArea(0, 0, 1040, 740)

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

        #goalsposts
        for post in self.goalpost_list:
            post.draw_goalposts(self.screen)

        #limit lines
        for ll in self.LimitLines:
            ll.draw_LimitLine(self.screen)

        self.screen.background.blit(self.robofei_logo_scaled,(965,2))