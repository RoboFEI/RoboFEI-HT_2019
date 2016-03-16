from screen import *
from control import *
import pygame
from math import cos
from math import sin
from math import radians
from math import degrees
from math import sqrt
from math import atan2
from math import pi
from math import exp

class Robot():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.new_x = x
        self.new_y = y
        self.front = 0
        self.rotate = 0
        self.index = 0
        self.radius = 22

        self.front = 0
        self.turn = 0
        self.drift = 0
        self.collision = False

        self.control = CONTROL(self)
        self.ball = None

        # Errors - TODO movement errors
        self.errors_on = False # if True *_error_variance can not be 0
        self.walk_error_mean = 0
        self.walk_error_variance = 0
        self.drift_error_mean = 0
        self.drift_error_variance = 0
        self.turn_error_mean = 0
        self.turn_error_variance = 0

        self.kick_error_angle_mean = 0
        self.kick_error_angle_variance = 0
        self.kick_error_force_mean = 0
        self.kick_error_force_variance = 0

        # IMU - TODO imu errors
        self.imu_error_mean = 0
        self.imu_error_variance = 0

    def draw_robot(self,robot_index, screen):
        pygame.draw.circle(screen.background,screen.BLACK,(self.x ,self.y),self.radius,0)
        pygame.draw.circle(screen.background,screen.BLUE,(self.x ,self.y),self.radius-2,0)
        x_theta = cos(radians(self.rotate))*(self.radius-2)
        y_theta = sin(radians(self.rotate))*(self.radius-2)
        pygame.draw.line(screen.background,screen.BLACK,(self.x ,self.y),(self.x + x_theta, self.y - y_theta),3)

        pygame.draw.line(screen.background,screen.BLACK,(self.x ,self.y),(self.x + x_theta, self.y - y_theta),1)

        font = pygame.font.Font(None, 20)
        self.index = robot_index + 1
        robot_name = "B" + str(self.index)
        text = font.render(robot_name, 1, (10, 10, 10))
        textpos = (self.x - 5, self.y - 40)
        screen.background.blit(text, textpos)

    def motion_vars(self, front, rotate, drift):
        self.front = front
        self.turn = rotate
        self.drift = drift

    def motion_model(self):
        if self.collision and self.front == 1:
            self.front = -1
        elif self.collision and self.front == -1:
            self.front = 1

        self.rotate = (self.rotate + self.turn) % 360

        self.new_x += cos(radians(self.rotate))*self.front
        self.new_y -= sin(radians(self.rotate))*self.front

        self.new_x -= sin(radians(self.rotate))*self.drift
        self.new_y -= cos(radians(self.rotate))*self.drift

        self.x = int(self.new_x)
        self.y = int(self.new_y)

        if self.x > 1040:
            self.x = 1040
            self.new_x = 1040
        elif self.x < 0:
            self.x = 0
            self.new_x = 0

        if self.y > 740:
            self.y = 740
            self.new_y = 740
        elif self.y < 0:
            self.y = 0
            self.new_y = 0

        self.collision = False

    def right_kick(self):
        R = degrees(atan2((self.y-self.ball.y), (self.ball.x-self.x)))
        d = sqrt((self.x - self.ball.x)**2+(self.y - self.ball.y)**2)
        force = 15 * exp(-2.3/self.ball.radius*d + 2.3/self.ball.radius*(self.radius+self.ball.radius))

        r = R
        if R < 0: r = R + 360

        if self.rotate < 30 and (r < self.rotate or r > 330 + self.rotate) or r < self.rotate and r > self.rotate - 30:
            self.ball.put_in_motion(force, self.rotate)

    def left_kick(self):
        R = degrees(atan2((self.y-self.ball.y), (self.ball.x-self.x)))
        d = sqrt((self.x - self.ball.x)**2+(self.y - self.ball.y)**2)
        force = 15 * exp(-2.3/self.ball.radius*d + 2.3/self.ball.radius*(self.radius+self.ball.radius))

        r = R
        if R < 0: r = R + 360

        if self.rotate > 330 and (r > self.rotate or r < self.rotate - 330) or r > self.rotate and r < self.rotate + 30:
            self.ball.put_in_motion(force, self.rotate)

    def get_orientation(self):
        # TODO implement IMU cumulative error
        return self.rotate

    def pass_left(self):
        R = degrees(atan2((self.y-self.ball.y), (self.ball.x-self.x)))
        d = sqrt((self.x - self.ball.x)**2+(self.y - self.ball.y)**2)
        force = 15 * exp(-2.3/self.ball.radius*d + 2.3/self.ball.radius*(self.radius+self.ball.radius))

        r = R
        if R < 0: r = R + 360

        if (self.rotate < 15 and (r < self.rotate + 15 or r > self.rotate + 345) or
            self.rotate > 345 and (r > self.rotate - 15 or r < self.rotate - 345) or
            r < self.rotate + 15 and r > self.rotate - 15):
            self.ball.put_in_motion(force, self.rotate + 90)

    def pass_right(self):
        R = degrees(atan2((self.y-self.ball.y), (self.ball.x-self.x)))
        d = sqrt((self.x - self.ball.x)**2+(self.y - self.ball.y)**2)
        force = 15 * exp(-2.3/self.ball.radius*d + 2.3/self.ball.radius*(self.radius+self.ball.radius))

        r = R
        if R < 0: r = R + 360

        if (self.rotate < 15 and (r < self.rotate + 15 or r > self.rotate + 345) or
            self.rotate > 345 and (r > self.rotate - 15 or r < self.rotate - 345) or
            r < self.rotate + 15 and r > self.rotate - 15):
            self.ball.put_in_motion(force, self.rotate - 90)

    def draw_vision(self,rotate):
        field_of_view = 101.75
        vision_dist = 200

        startRad = radians(-35-rotate)
        endRad = radians(35-rotate)
        pygame.draw.arc(screen, (255, 255, 255), [self.x-vision_dist,self.y-vision_dist,vision_dist*2,vision_dist*2], startRad, endRad, 1)

        vision_surface = pygame.Surface((vision_dist * 2, vision_dist * 2))
        vision_surface.fill([0,150,0])
        vision_surface.set_colorkey([0,150,0])
        vision_surface.set_alpha(200)
        vision_surface_center = (vision_dist, vision_dist)

        #print rotate
        #print self.theta
        theta_vision = radians(rotate)

        angle_1 = theta_vision - field_of_view/2
        angle_2 = theta_vision + field_of_view/2

        point_1 = (vision_dist, angle_1)
        point_2 = (vision_dist, angle_2)

        point_1 = toRectangular(point_1)
        point_2 = toRectangular(point_2)

        point_1 = (point_1[0] + vision_surface_center[0], point_1[1] + vision_surface_center[1])
        point_2 = (point_2[0] + vision_surface_center[0], point_2[1] + vision_surface_center[1])


        pygame.draw.arc(vision_surface, (255, 255, 255), [vision_dist/2,vision_dist/2,vision_dist,vision_dist], startRad, endRad, 1)

        pygame.draw.line(vision_surface, (255, 255, 255), vision_surface_center, point_1, 1)
        pygame.draw.line(vision_surface, (255, 255, 255), vision_surface_center, point_2, 1)


        position = (
            self.x - vision_dist,
            self.y - vision_dist
        )

        screen.blit(vision_surface, position)


    def hcc(self,x1,y1,x2,y2):
        return sqrt((x1-x2)**2 + (y1-y2)**2)


    def distD(self, x1, y1, x2, y2):
        return self.hcc(x1, y1, x2, y2)

    def distR(self, x1, y1, x2, y2):
        return atan2((y2-y1), (x2-x1))*180/pi
        # atan2 retorna angulo entre -pi e +pi

    def compAng(self, ang, base):
        angrange = 35
        base = -base
        if(base > 180 - angrange or base < -180 + angrange):
            if(ang > 0 and base < 0):
                return (ang < base + 360 + angrange) and (ang > base + 360 - angrange)
            elif (ang < 0 and base > 0):
                return (ang < base - 360 + angrange) and (ang > base - 360 - angrange)
        return (ang < base + angrange) and (ang > base - angrange)

    def view_obj(self,x,y,rotate):
        field_of_view = 100
        vision_dist = 200  #we need to add as global variavel

        d = self.distD(self.x,self.y,x,y)
        r = self.distR(self.x,self.y,x,y)

        d=random.gauss(d,0.1*d/10)

        if((d < vision_dist) and self.compAng(r,rotate)):
            print 'Inside'
        else:
            print 'Outside'

