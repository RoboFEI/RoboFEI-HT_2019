import pygame
import random as rnd
import socket
import time

class Telemetry(object):
    def __init__(self, n):
        self.x = 0  # absolute X position
        self.y = 0  # absolute Y position

        self.px = 0 # previous mouse X position
        self.py = 0 # previous mouse Y position

        self.roll = 0 # used to scroll text
        self.maxscroll = 0 # used to scroll text

        self.number = n
        self.name = "ROBO " + str(n) # robot name

        self.size = 20 # screen size

        self.minimize = True    # toogles the minimized screen
        self.hide = True        # toogles the hidden variables

        self.variables = [['SOMETHING1', True, 'void'],
                          ['SOMETHING2', False, 'void'],
                          ['SOMETHING3', True, 'void']]

        self.resizing = False   # toogles the resizing function
        self.dragging = False    # toogles the dragging function

        self.font = pygame.font.SysFont('Arial', 12)

        self.timestamp = time.time()

        self.Body = pygame.Surface((260, 742), pygame.SRCALPHA) # surface where everything will be drawn

    def change(self, data):
        self.variables[1][2] = data[1]
        self.variables[2][2] = data[2]
        self.timestamp = time.time()

    def timeout(self):
        timer = time.time() - self.timestamp
        return timer

    def draw(self, where):
        self.Body.fill(pygame.Color(255,255,255,0)) # Clear the surface

        if self.dragging:
            self.drag()     # Drags the object around
        if self.resizing:
            self.resize()   # Resizes the object

        if self.minimize:
            pygame.draw.rect(self.Body, (0,0,0,150), (0,0,260,20))
            pygame.draw.line(self.Body, (255,255,255), (249, 4), (249, 15), 2)
        else:
            pygame.draw.rect(self.Body, (0,0,0,150), (0,0,260,20 + self.size))
            self.Write()
            pygame.draw.line(self.Body, (0,0,0), (0,0), (0,19 + self.size), 2)
            pygame.draw.line(self.Body, (0,0,0), (258,0), (258,19 + self.size), 2)
            pygame.draw.line(self.Body, (0,0,0), (0,17 + self.size), (260,17 + self.size), 5)

        if self.hide:
            pygame.draw.line(self.Body, (255,255,255), (227,4), (227,15), 2)
            pygame.draw.line(self.Body, (255,255,255), (231,4), (231,15), 2)
            pygame.draw.line(self.Body, (255,255,255), (227,9), (232,9), 2)
        else:
            pygame.draw.rect(self.Body, (255,255,255), (224,4,11,11), 0)

        pygame.draw.line(self.Body, (255,255,255), (244, 9), (255, 9), 2)
        pygame.draw.rect(self.Body, (255,255,255), (244,4,11,11), 2)
        pygame.draw.rect(self.Body, (255,255,255), (224,4,11,11), 2)

        self.font.set_bold(True)
        self.Body.blit(self.font.render(self.name, 1, (255,255,0)), (10, 4))

        pygame.draw.rect(self.Body, (0,0,0), (0,0,259,19), 2)

        where.blit(self.Body, (self.x, self.y)) # Draws the object on screen

    def Write(self):
        pos = self.roll # initial text position

        self.font.set_bold(False) # toogles off bold font

        TextBody = pygame.Surface((260, self.size), pygame.SRCALPHA) # creates a surface for the text

        for x in self.variables: # for each variable

            if not(x[1]): # if it is not hidden
                txt = x[0] + " = " + x[2] # reads the variable in the memory...
                TextBody.blit(self.font.render(txt, 1, (255,255,255)), (10, pos)) # print the variable
                pos += 16 # makes a space

            elif not(self.hide) and x[1]: # if hidden variables are not to be hidden
                TextBody.blit(self.font.render(x[0], 1, (128,128,128)), (10, pos)) # print the variable
                pos += 16 # makes a space

        self.maxscroll = pos
        self.Body.blit(TextBody, (0,20)) # draws the texts to the window

    def click(self, mx, my):
        # Tests where is the mouse click
        if mx > self.x+244 and mx < self.x+256 and my > self.y+4 and my < self.y+16:
            self.minimize = not(self.minimize) # toogles minimized screen

        if mx > self.x+224 and mx < self.x+236 and my > self.y+4 and my < self.y+16:
            self.hide = not(self.hide) # toogles hidden atributes

        if mx > self.x and mx < self.x + 260 and not(self.minimize) and not(self.hide) and my > self.y + 20 and my < self.y + 20 + self.size:
            pos = self.roll # Positions the button tests

            for x in self.variables:
                if my > self.y+20+pos and my < self.y + pos + 36: # Verifies the position of the click
                    x[1] = not(x[1]) # toogles
                pos += 16

        if not(self.minimize) and my > self.y+16+self.size and my < self.y+21+self.size:
            self.start_resize() # starts the resizing function
        else:
            self.start_drag() # starts the dragging function

    def scroll(self, up):
        # Scrolls only if there are things not seen on the screen...
        if up and not(self.minimize) and self.maxscroll > self.size:
            self.roll -= 5

        elif not(up) and not(self.minimize) and self.roll < 0:
            self.roll += 5

    def start_resize(self):
        self.px, self.py = pygame.mouse.get_pos() # Saves mouse initial position
        self.resizing = True # starts resizing

    def resize(self):
        dx, dy = pygame.mouse.get_pos() # gets actual mouse position

        self.size += dy - self.py # Compute new size

        # Checks size bounds
        if self.size < 20:
            self.size = 20
        elif self.size > 700:
            self.size = 700

        self.px, self.py = dx, dy # save actual mouse position

    def stop_resize(self):
        self.resizing = False # stops resizing

    def start_drag(self):
        self.px, self.py = pygame.mouse.get_pos() # saves mouse initial position
        self.dragging = True # starts dragging

    def drag(self):
        dx, dy = pygame.mouse.get_pos() # gets actual mouse position

        self.x += dx - self.px # Computes new X position

        # Checks X position boundaries
        if self.x < 0:
            self.x = 0
        elif self.x > 782:
            self.x = 782

        self.y += dy - self.py # Computes new Y position

        # Checks Y position boundaries
        if self.y < 0:
            self.y = 0
        elif self.y > 722:
            self.y = 722

        self.px, self.py = dx, dy # saves actual mouse position

    def stop_drag(self):
        self.dragging = False # stops dragging function

def TelemetryControl(tele, sock):
    for s in sock:
        try:
            data = s.recv(1024, socket.MSG_DONTWAIT)
            data = data.split()
            test = True

            # print data

            for t in tele:
                if t.number == int(data[0]):
                    t.change(data)
                    test = False
                    break

            if test:
                tele.append(Telemetry(int(data[0])))

        except socket.timeout:
            # print "Timeout"
            pass
        except:
            # print "OTHER ERROR"
            pass
    pop = []
    a = 0
    for t in tele:
        timer = t.timeout()
        if timer > 10:
            # print "Disconnect ",t.number, " time ", timer
            pop.append(a)
        a += 1

    for p in pop:
        tele.pop(p)
