from collisions import *
from telemetry import *
import sys
sys.path.append('../AI/Localization/src/')
from particle import *
from GameState import *

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

        self.gamecontroller = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.gamecontroller.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.gamecontroller.bind(('0.0.0.0', 3838))
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
        # if True:
            data, _ = self.gamecontroller.recvfrom(GameState.sizeof()) # Reads GameController
            data = GameState.parse(data)

            State = data.game_state # Gets game state
            Time = data.secondary_seconds_remaining*256 + data.seconds_remaining # Gets remaining time, in seconds.
            if data.teams[0].team_number == 18: # Find the first team
                FGoal = data.teams[0].score # Saves the team's score
                EGoal = data.teams[1].score # Saves the opponent's score
            else:
                FGoal = data.teams[1].score # Saves the team's score
                EGoal = data.teams[0].score # Saves the opponent's score
            
            if State == 'STATE_PLAYING':
                self.field.GameStop = False
            else:
                self.field.GameStop = True

            self.field.Counter = Time * 1000

            self.field.FriendGoals = FGoal
            self.field.EnemyGoals = EGoal
        except:
            # print 'Not listenning the Gamecontroller at', time.time()
            pass

        pygame.display.flip()
