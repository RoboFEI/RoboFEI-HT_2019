from collisions import *
import sys
from telemetry import *

class Simulation():
    def __init__(self, screen):
        self.mx = 0
        self.my = 0
        self.screen = screen

        self.tele = []
        self.timestamp = 0
        self.sock = []
        for c in range(4):
            self.sock.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
            self.sock[c].bind(('255.255.255.255', 1241+c))
            self.sock[c].settimeout(0.001)

    def update_mouse_pos(self):
        self.mx, self.my = pygame.mouse.get_pos()

    def perform_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
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
            tele.draw(self.screen.background)

        timer = time.time() - self.timestamp
        if timer > 0.5:
            TelemetryControl(self.tele, self.sock)
            self.timestamp = time.time()

        pygame.display.flip()
