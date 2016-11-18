

from collisions import *
from telemetry import *
import sys
sys.path.append('../AI/Localization/src/')
from particle import *

class Simulation():
    def __init__(self, screen):
        self.mx = 0
        self.my = 0
        self.screen = screen

        self.field = None

        self.tele = []
        self.side = False
        self.timestamp = 0
        self.sock = []
        for c in range(4):
            self.sock.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
            self.sock[c].bind(('255.255.255.255', 1241+c))
            self.sock[c].settimeout(0.001)

        self.gamecontroller = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.gamecontroller.bind(('255.255.255.255', 3838))
        self.gamecontroller.settimeout(0.001)

    def update_mouse_pos(self):
        self.mx, self.my = pygame.mouse.get_pos()

    def perform_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.side = not self.side

            try:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.update_mouse_pos()
                    for tele in self.tele:
                        if self.mx > tele.x and self.mx < tele.x+260 and self.my > tele.y and self.my < tele.y + 20 + tele.size * (not(tele.minimize)):
                            if event.button == 1:
                                tele.click(self.mx, self.my)
                            elif event.button == 4:
                                tele.scroll(True)
                            elif event.button == 5:
                                tele.scroll(False)

                if event.type == pygame.MOUSEBUTTONUP:
                    for tele in self.tele:
                        tele.stop_drag()
                        tele.stop_resize()
            except:
                print "Telemetry Error"

    def display_update(self):

        for tele in self.tele:
            for auxtele in self.tele:
                if tele != auxtele:
                    telemetry_collision(tele, auxtele)
            tele.draw(self.screen.background, self.side)

        timer = time.time() - self.timestamp
        if timer > 0.5: # Period to update telemetry in seconds
            TelemetryControl(self.tele, self.sock)
            self.timestamp = time.time()

        try:
            data = self.gamecontroller.recv(1024, socket.MSG_DONTWAIT) # Reads GameController
            v = memoryview(data) # Gets the memory address
            x = v.tolist() # Converts the memory into useful data
            if len(x) == 158:
                State = x[7] # Gets game state
                Time = x[15]*256 + x[14] # Gets remaining time, in seconds.
                if x[18] == 18: # Find the first team
                    FGoal = x[20] # Saves the team's score
                    EGoal = x[90] # Saves the opponent's score
                else:
                    FGoal = x[90] # Saves the team's score
                    EGoal = x[20] # Saves the opponent's score

                if State == 3:
                    self.field.GameStop = False
                else:
                    self.field.GameStop = True

                self.field.Counter = Time * 1000

                self.field.FriendGoals = FGoal
                self.field.EnemyGoals = EGoal
        except:
            pass

        pygame.display.flip()
