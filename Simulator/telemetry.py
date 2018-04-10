import pygame
import random as rnd
from math import cos, sin, radians, degrees, sqrt
import socket
import time
from collections import defaultdict

'''
Sequence of communication Protocol:
0 - Robot Number
----------------------------------
1 - X position
2 - Y position
3 - Rotation
4 - Belief
5 - Ball Distance
6 - Ball Angle
----------------------------------
7 - Control
8 - Vision
9 - Localization
10 - Decision
11 - IMU
----------------------------------
12 - DECISION_ACTION_A
13 - IMU_EULER_Z
14 - VOLTAGE
'''

#--------------------------------------------------------------------------------------------------
#   TELEMETRY CLASS
#--------------------------------------------------------------------------------------------------

class Telemetry(object):

    #----------------------------------------------------------------------------------------------
    #   CLASS CONSTRUCTOR
    #----------------------------------------------------------------------------------------------

    def __init__(self, n):
        self.x = 0  # absolute X position
        self.y = 0  # absolute Y position

        self.px = 0 # previous mouse X position
        self.py = 0 # previous mouse Y position

        self.roll = 0 # used to scroll text
        self.maxscroll = 0 # used to scroll text

        self.number = n
        self.name = "B" + str(n) # robot name
        # Selects the robots color...
        if n == 1:
            self.color = (255, 0, 0)
        elif n == 2:
            self.color = (0, 255, 255)
        elif n == 3:
            self.color = (255, 255, 0)
        elif n == 4:
            self.color = (255, 0, 255)

        self.size = 90 # screen size

        self.todraw = True # indicates if it will be drown

        self.minimize = False    # toogles the minimized screen
        self.hide = False        # toogles the hidden variables

        # Variables to be shown in the window
        self.variables = [['CONTROL_WORKING', True, 'NO'],
                          ['VISION_WORKING', True, 'NO'],
                          ['LOCALIZATION_WORKING', True, 'NO'],
                          ['DECISION_WORKING', True, 'NO'],
                          ['IMU_WORKING', True, 'NO'],
                          ['DECISION_ACTION_A', True, '---'],
                          ['IMU_EULER_Z', True, '---'],
                          ['VOLTAGE', True, '---'],
                          ['VISION_LOST', True, '---']]

        # Variables for probable process' situation
        self.probs = [0.5, 0.5, 0.5, 0.5, 0.5]

        # Controls Dictionary...
        self.dictcontrol = {0: 'Nada a fazer',
                            1: 'Andar para frente',
                            2: 'Virar a esquerda',
                            3: 'Virar a direita',
                            4: 'Chute forte direito',
                            5: 'Chute forte esquerdo',
                            6: 'Andar de Lado esquerda',
                            7: 'Andar de Lado direita',
                            8: 'Andar lento para frente',
                            9: 'Girar em torno da bola para esquerda',
                            10: 'Defender a bola',
                            11: 'Stop com gait',
                            12: 'Passe forte Esquerda',
                            13: 'Passe forte Direita',
                            14: 'Girar em torno da bola para direita',
                            15: 'Levantar de frente',
                            16: 'Levantar de costa',
                            17: 'Andar rapido para traz',
                            18: 'Andar lento para traz',
                            19: 'Greetings',
                            20: 'GoodBye',
                            21: 'Chute fraco direito',
                            22: 'Chute fraco esquerdo'}
        self.dictcontrol = defaultdict(lambda:'ERRO NO DICIONARIO DA TELEMETRIA', self.dictcontrol)
        # Variables which draws things in the screen
        # ------------------------------------------
        # 0 - Robot's X position
        # 1 - Robot's Y position
        # 2 - Robot's rotation
        # 3 - Robot's belief
        # 4 - Ball's X position
        # 5 - Ball's Y position
        # 6 - Battery's Voltage
        self.othervars = [450, 300, 0, 10, 0, 0, 0]

        self.resizing = False   # toogles the resizing function
        self.dragging = False    # toogles the dragging function

        self.font = pygame.font.SysFont('Arial', 12)

        self.timestamp = time.time()

        self.Body = pygame.Surface((260, 742), pygame.SRCALPHA) # surface to draw the interactive window
        self.Robot = pygame.Surface((26,26), pygame.SRCALPHA) # surface to draw robot

    #----------------------------------------------------------------------------------------------
    #   METHOD WHICH UPDATES THE VARS USED IN THE FLOAT PANELS
    #----------------------------------------------------------------------------------------------

    def change(self, data): # Distributes the received messages into the variables.
        # Localization Vars
        try:
            self.othervars[0] = float(data[1])
            self.othervars[1] = float(data[2])
            self.othervars[2] = int(degrees(float(data[3])))
            self.othervars[3] = max(float(data[4])*sqrt(2)*10, 15)

            if data[4] == "-1" or True:
                self.othervars[4] = -1000
                self.othervars[5] = -1000
            else:
                self.othervars[4] = float(data[1]) + float(data[5]) * cos(-radians(float(data[3]) + float(data[6])))
                self.othervars[5] = float(data[2]) + float(data[5]) * sin(-radians(float(data[3]) + float(data[6])))
        except:
            print 'ERROR on telemetry.change() for LOCALIZATION variables!'

        # Panel Vars

        # Variables for the control variables.
        try:
            for i in range(5):
                # Computes the probability of the process been off given the observation.
                if data[i+7] == '0':
                    self.probs[i] = max(0.001, 0.1 * self.probs[i] / (0.99 - 0.89 * self.probs[i]))
                else:
                    self.probs[i] = min(0.999, 0.9 * self.probs[i] / (0.01 + 0.89 * self.probs[i]))

                # Returns the max probable situation.
                if self.probs[i] < 0.5:
                    self.variables[i][2] = 'NO'
                else:
                    self.variables[i][2] = 'YES'
        except:
            print 'ERROR on telemetry.change() for FLAGS!'

        # Gets the Decision Action
        try:
            self.variables[5][2] = self.dictcontrol[int(data[12])]
        except:
            print 'ERROR on telemetry.change() for ACTION_DECISION_A!'

        # Gets the IMU orientation
        try:
            self.variables[6][2] = data[13]
        except:
            print 'ERROR on telemetry.change() for IMU_EULER_Z!'

        # Gets the voltage from the servos.
        try:
            self.variables[7][2] = str(float(data[14])/10) + 'V'
            self.othervars[6] = int(data[14])
        except:
            print 'ERROR of telemetry.change() for VOLTAGE!'

        # Variable of seen ball.
        try:
            if data[15] == '1':
                self.variables[8][2] = "Lost Ball"
            elif data[15] == '0':
                self.variables[8][2] = "Found Ball"
            else:
                self.variables[8][2] = "Wrong Value"
        except:
            print 'ERROR of telemetry.change() for VISION_LOST!'            

        # Test if the Telemetry is updated.
        try:
            if data[16] != 'OUT':
                print 'TELEMETRY IS OUTDATED!'
        except:
            print 'ERROR on telemetry.change()!'

        # Saves a time stamp
        self.timestamp = time.time()

    #----------------------------------------------------------------------------------------------
    #   METHOD THAT RETURNS THE ELAPSED TIME SINCE THE LAST TIMESTAMP
    #----------------------------------------------------------------------------------------------

    def timeout(self): # Returns how long since the last received message
        timer = time.time() - self.timestamp
        return timer

    #----------------------------------------------------------------------------------------------
    #   METHOD THAT DRAWS THINGS ON SCREEN
    #----------------------------------------------------------------------------------------------

    def draw(self, where, side):
        if not self.todraw:
            return None # Do not let the frame be drown

        new = pygame.Surface((1042, 742), pygame.SRCALPHA) # Surface of the Telemetry

        if self.dragging:
            self.drag()     # Drags the object around
        if self.resizing:
            self.resize()   # Resizes the object

        if side:
            pygame.draw.line(new, self.color,(int((2*self.x+260)/2),int((2*self.y+20+self.size*(not(self.minimize)))/2)),(1040-int(self.othervars[0]),740-int(self.othervars[1])), 3) # Draws a line
            pygame.draw.circle(new, (0,0,0,0), (1040 - int(self.othervars[0]), 740 - int(self.othervars[1])), int(self.othervars[3]), 0) # Cuts a circle
            pygame.draw.circle(new, self.color, (1040 - int(self.othervars[0]), 740 - int(self.othervars[1])), int(self.othervars[3]), 3) # Draws a circle
        else:
            pygame.draw.line(new, self.color,(int((2*self.x+260)/2),int((2*self.y+20+self.size*(not(self.minimize)))/2)),(int(self.othervars[0]),int(self.othervars[1])), 3) # Draws a line
            pygame.draw.circle(new, (0,0,0,0), (int(self.othervars[0]), int(self.othervars[1])), int(self.othervars[3]), 0) # Cuts a circle
            pygame.draw.circle(new, self.color, (int(self.othervars[0]), int(self.othervars[1])), int(self.othervars[3]), 3) # Draws a circle
        pygame.draw.rect(new, (0,0,0,0), (self.x, self.y, 260, 20+self.size*(not(self.minimize))), 0) # Cuts a square

        self.Body.fill(pygame.Color(255,255,255,0)) # Clear the window surface
        self.Robot.fill(pygame.Color(255,255,255,0)) # Clear the robot surface

        # Draws the robot
        pygame.draw.rect(self.Robot, self.color + (150,), (3, 0, 16, 26), 0) # Fill Body
        pygame.draw.rect(self.Robot, (0, 0, 0), (3, 0, 16, 26), 1) # Countour Body
        pygame.draw.rect(self.Robot, (0, 0, 0, 150), (19, 2, 5, 10), 0) # Fill feet
        pygame.draw.rect(self.Robot, (0, 0, 0, 150), (19, 14, 5, 10), 0)
        pygame.draw.rect(self.Robot, (0, 0, 0), (19, 2, 5, 10), 1) # Countour feet
        pygame.draw.rect(self.Robot, (0, 0, 0), (19, 14, 5, 10), 1)

        # Rotates robot
        if side:
            aux = pygame.transform.rotate(self.Robot, self.othervars[2] + 180)
        else:
            aux = pygame.transform.rotate(self.Robot, self.othervars[2])
        rr = aux.get_rect()

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

        cg = 51*self.othervars[6] - 8925
        cg = int(min(max(cg, 0), 255))

        cr = (51*self.othervars[6]-8160) * (self.othervars[6] < 170) + (-51*self.othervars[6]+9945) * (self.othervars[6] >= 170)
        cr = int(min(max(cr, 0), 255))

        b = self.othervars[6]/3 - 49
        b = int(min(max(b,1),21))

        pygame.draw.rect(self.Body, (cr,cg,0), (194,4,b,11), 0)

        pygame.draw.line(self.Body, (255,255,255), (244, 9), (255, 9), 2)
        pygame.draw.rect(self.Body, (255,255,255), (244,4,11,11), 2)
        pygame.draw.rect(self.Body, (255,255,255), (224,4,11,11), 2)
        pygame.draw.rect(self.Body, (255,255,255), (194,4,21,11), 2)
        pygame.draw.line(self.Body, (255,255,255), (216, 6), (216, 13), 4)

        self.font.set_bold(True)
        timer = self.timeout()
        if timer < 1.7:
            self.Body.blit(self.font.render(self.name, 1, self.color), (10, 4))
        else:
            self.Body.blit(self.font.render(self.name + ' [TIMEOUT = ' + str(int(timer)) + ' SEC]', 1, self.color), (10, 4))

        pygame.draw.rect(self.Body, (0,0,0), (0,0,259,19), 2)

        # Draw ball
        ball = pygame.image.load("ball.png") # Load Bitmap
        ball = pygame.transform.scale(ball,(19,19)) # Resize it
        if side:
            pygame.draw.circle(where, self.color, (1040 - int(self.othervars[4]), 740 - int(self.othervars[5])), 13, 0) # Circle it
            where.blit(ball,(1040 - int(self.othervars[4]) - 10, 740 - int(self.othervars[5]) - 10)) # Draw on screen
            new.blit(aux, (int(1040 - self.othervars[0]-rr[2]/2), int(740 - self.othervars[1]-rr[3]/2))) # Draws the Robot
        else:
            pygame.draw.circle(where, self.color, (int(self.othervars[4]),int(self.othervars[5])), 13, 0) # Circle it
            where.blit(ball,(int(self.othervars[4]) - 10, int(self.othervars[5]) - 10)) # Draw on screen
            new.blit(aux, (int(self.othervars[0]-rr[2]/2), int(self.othervars[1]-rr[3]/2))) # Draws the Robot
        
        new.blit(self.Body, (int(self.x), int(self.y))) # Draws the object on screen

        where.blit(new, (0,0)) # Draws Telemetry on Screen
        where.blit(self.font.render("PRESS SPACE TO INVERT FIELD VIEW", 1, (255,255,255)), (400,690)) # Print message on screen

    #----------------------------------------------------------------------------------------------
    #   METHOD THAT WRITE ON THE FLOATING PANELS
    #----------------------------------------------------------------------------------------------

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

    #----------------------------------------------------------------------------------------------
    #   CALLBACK METHOD OF THE KEYBOARD
    #----------------------------------------------------------------------------------------------

    def click(self, mx, my):
        # Tests where is the mouse click
        if mx > self.x+244 and mx < self.x+256 and my > self.y+4 and my < self.y+16:
            self.minimize = not(self.minimize) # toogles minimized screen

        elif mx > self.x+224 and mx < self.x+236 and my > self.y+4 and my < self.y+16:
            self.hide = not(self.hide) # toogles hidden atributes

        elif not(self.minimize) and my > self.y + 10 + self.size and my < self.y + 21 + self.size:
            self.start_resize() # starts the resizing function

        elif mx > self.x and mx < self.x + 260 and not(self.minimize) and not(self.hide) and my > self.y + 20 and my < self.y + 20 + self.size:
            pos = self.roll # Positions the button tests

            for x in self.variables:
                if my > self.y+20+pos and my < self.y + pos + 36: # Verifies the position of the click
                    x[1] = not(x[1]) # toogles
                pos += 16

        else:
            self.start_drag() # starts the dragging function

    #----------------------------------------------------------------------------------------------
    #   METHOD USED FOR THE SCROLLBAR
    #----------------------------------------------------------------------------------------------

    def scroll(self, up):
        # Scrolls only if there are things not seen on the screen...
        if up and not(self.minimize) and self.maxscroll > self.size:
            self.roll -= 5

        elif not(up) and not(self.minimize) and self.roll < 0:
            self.roll += 5

    #----------------------------------------------------------------------------------------------
    #   METHOD TO START RESIZING THE FLOATING PANEL
    #----------------------------------------------------------------------------------------------

    def start_resize(self):
        self.px, self.py = pygame.mouse.get_pos() # Saves mouse initial position
        self.resizing = True # starts resizing

    #----------------------------------------------------------------------------------------------
    #   METHOD THAT RESIZES THE FLOATING PANEL SIZE
    #----------------------------------------------------------------------------------------------

    def resize(self):
        dx, dy = pygame.mouse.get_pos() # gets actual mouse position

        self.size += dy - self.py # Compute new size

        # Checks size bounds
        if self.size < 20:
            self.size = 20
        elif self.size > 700:
            self.size = 700

        self.px, self.py = dx, dy # save actual mouse position

    #----------------------------------------------------------------------------------------------
    #   METHOD TO FINISH THE RESIZING OF THE FLOATING PANEL
    #----------------------------------------------------------------------------------------------

    def stop_resize(self):
        self.resizing = False # stops resizing

    #----------------------------------------------------------------------------------------------
    #   METHOD USED TO START DRAGGING THE FLOATING PANEL
    #----------------------------------------------------------------------------------------------

    def start_drag(self):
        self.px, self.py = pygame.mouse.get_pos() # saves mouse initial position
        self.dragging = True # starts dragging

    #----------------------------------------------------------------------------------------------
    #   METHOD USED TO DRAG THE FLOATING PANEL AROUND
    #----------------------------------------------------------------------------------------------

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

    #----------------------------------------------------------------------------------------------
    #   METHOD THAT FINALIZES THE DRAGGING OF A FLOATING PANEL
    #----------------------------------------------------------------------------------------------

    def stop_drag(self):
        self.dragging = False # stops dragging function


#--------------------------------------------------------------------------------------------------
#   FUNCTION WHICH MANAGES THE TELEMETRY CLASS
#--------------------------------------------------------------------------------------------------

def TelemetryControl(tele, sock): # Function to Control the Telemetry Screens
    # Iterates through all ports searching messages
    for s in sock:
        try:
            data = Flush(s) # Clears buffer and returns the last data
            data = data.split() # Splits it into a list
            test = True # Assumes the message is from a new robot

            for t in tele: # Iterates through all opened screens
                if t.number == int(data[0]): # Eventually if the robot exists
                    t.change(data) # Saves the received message into the Telemetry variables
                    t.todraw = True # Turn on the screen telemetry
                    test = False # Confirms the existing robot
                    break # Stops iterations

            if test: # If the robot was not found
                tele.append(Telemetry(int(data[0]))) # Creates a new screen to it
        except:
            # print 'Communication Lost at', time.time()
            pass

    for t in tele: # For all robots
        timer = t.timeout()  # Get's how long since the last received message
        if timer > 10: # If it is ore than 10 seconds
            t.todraw = False

#--------------------------------------------------------------------------------------------------
#   FUNCTION WHICH CLEARS THE COMMUNICATION BUFFER
#--------------------------------------------------------------------------------------------------

def Flush(sock):
    data = None # Initializes a void Data variable
    try:
        while True: # While there is something in the buffer
            data = sock.recv(1024, socket.MSG_DONTWAIT) # Save it into the data
    except:
        return data # Return the last dat in the buffer
