__author__ = "RoboFEI-HT"
__authors__ = "Aislan C. Almeida"
__license__ = "GNU General Public License v3.0"

from Viewer import * # Imports the environment of the viewer
# from AMCL import * # Imports the Particle Filter Class
import time 

# To pass arguments to the function
import argparse
# Import a shared memory
import sys
sys.path.append('../../Blackboard/src/')
from SharedMemory import SharedMemory

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

# To parse arguments on execution
parser = argparse.ArgumentParser(description='Robot Localization', epilog= 'Implements particle filters to self-localize a robot on the field.')
parser.add_argument('-g', '--graphs', action="store_true", help='Shows graphical interface which visualizes the particles.')
parser.add_argument('-l', '--log', action="store_true", help='Print variable logs.')
parser.add_argument('-m', '--mcl', action="store_true", help='Uses Monte-Carlo Localization')
parser.add_argument('-a', '--amcl', action="store_true", help='Uses Augmented Monte-Carlo Localization')
parser.add_argument('-s', '--srmcl', action="store_true", help='Uses Sensor Reseting Monte-Carlo Localization')

args = parser.parse_args()

if args.mcl:
    from MCL import *
elif args.amcl:
    from AMCL import *
elif args.srmcl:
    from SRMCL import *
else:
    print 'Please choose a version of MCL to be used!'
    exit()


#--------------------------------------------------------------------------------------------------
#   Class implementing the Core of the Localization Process
#--------------------------------------------------------------------------------------------------

class Localization():
    #----------------------------------------------------------------------------------------------
    #   Class constructor and pre-processing.
    #----------------------------------------------------------------------------------------------
    def __init__(self):
        self.bkb = SharedMemory() # Instance of a blackboard
        config = ConfigParser()   # Configuration file

        try:
            config.read('../../Control/Data/config.ini') # Reads the config archive
            mem_key = int(config.get('Communication', 'no_player_robofei'))*100 # Get the memory key
        except:
            print "#----------------------------------#"
            print "#   Error loading config parser.   #"
            print "#----------------------------------#"
            sys.exit()

        self.Mem = self.bkb.shd_constructor(mem_key) # Create the link to the blackboard

        self.args = parser.parse_args()

        # Timestamp to use on the time step used for motion
        self.timestamp = time.time()

        # Clears the variables in the blackboard
        self.bkb.write_float(self.Mem, 'VISION_BLUE_LANDMARK_DEG', -999)
        self.bkb.write_float(self.Mem, 'VISION_RED_LANDMARK_DEG', -999)
        self.bkb.write_float(self.Mem, 'VISION_YELLOW_LANDMARK_DEG', -999)
        self.bkb.write_float(self.Mem, 'VISION_PURPLE_LANDMARK_DEG', -999)

    #----------------------------------------------------------------------------------------------
    #   Localization's main method.
    #----------------------------------------------------------------------------------------------
    def main(self):
        screen = Screen(self.args.graphs) # Creates a new screen

        if self.args.graphs:
            simul = Simulation(screen) # Creates the interface structure
            field = SoccerField(screen) # Draws the field
            simul.field = field # Passes the field to the simulation

        PF = MonteCarlo(5000) # Starts the Particle Filter

        print

        zb = []
        zr = []
        zy = []
        zp = []
        timecount = []

        # Main loop
        while True:
            z0 = 0
            z1 = 0
            z2 = 0
            z3 = 0

            self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 1) # Sets the flag for telemetry

            # Process interactions events
            if self.args.graphs:
                simul.perform_events()

            # Gets the motion command from the blackboard.
            u = self.GetU(self.bkb.read_int(self.Mem, 'CONTROL_ACTION'))

            auxtime = time.time()
            try:
                if auxtime-timecount[0] > 0:
                    timecount.pop(0)
                    for zn in [zb, zr, zy, zp]:
                        zn.pop(0)
            except:
                pass

            # print timecount

            timecount.append(auxtime)
            # Gets the measured variable from the blackboard,
            # and free them.
            zb.append(self.bkb.read_float(self.Mem, 'VISION_BLUE_LANDMARK_DEG'))
            self.bkb.write_float(self.Mem, 'VISION_BLUE_LANDMARK_DEG', -999)
            zr.append(self.bkb.read_float(self.Mem, 'VISION_RED_LANDMARK_DEG'))
            self.bkb.write_float(self.Mem, 'VISION_RED_LANDMARK_DEG', -999)
            zy.append(self.bkb.read_float(self.Mem, 'VISION_YELLOW_LANDMARK_DEG'))
            self.bkb.write_float(self.Mem, 'VISION_YELLOW_LANDMARK_DEG', -999)
            zp.append(self.bkb.read_float(self.Mem, 'VISION_PURPLE_LANDMARK_DEG'))
            self.bkb.write_float(self.Mem, 'VISION_PURPLE_LANDMARK_DEG', -999)


            z0 = mean(zb)
            z1 = mean(zr)
            z2 = mean(zy)
            z3 = mean(zp)
            z4 = degrees(self.bkb.read_float(self.Mem, 'IMU_EULER_Z'))

            # print zn[0], z0         

            # Mounts the vector to be sent
            z = (z0, z1, z2, z3, z4)
            # print z
               
            # Performs Particle Filter's Update
            pos, std = PF.main(u,z)

            if std > 1: # Se o erro for muito alto ele acha landmarks
                self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', 1)
            elif std < 1: # Se for pequeno o bastante ele acha a bola
                self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', 0)
            
            if self.args.log:
                print '\t\x1b[32mRobot at', # Prints header
                print '\x1b[32m[x:\x1b[34m{} cm'.format(int(pos[0])), #  Prints the x position
                print '\x1b[32m| y:\x1b[34m{} cm'.format(int(pos[1])), # Prints the y position
                print u'\x1b[32m| \u03B8:\x1b[34m{}\u00B0'.format(int(pos[2])), # Prints the theta
                print u'\x1b[32m| \u03C3:\x1b[34m{} cm\x1b[32m]'.format(int(std)) # Prints the standard deviation

            # Wirte the robot's position on Black Board to be read by telemetry
            self.bkb.write_int(self.Mem, 'LOCALIZATION_X', int(pos[0]))
            self.bkb.write_int(self.Mem, 'LOCALIZATION_Y', int(pos[1]))
            self.bkb.write_int(self.Mem, 'LOCALIZATION_THETA', int(pos[2]))
            self.bkb.write_float(self.Mem, 'LOCALIZATION_RBT01_X', std)

            if self.args.graphs:
                # Redraws the screen background
                field.draw_soccer_field()

                # Draws all particles on screen
                simul.display_update(PF.particles)

            # Updates for the next clock
            screen.clock.tick(60)

    #----------------------------------------------------------------------------------------------
    #   This method returns a command instruction to the particles.
    #----------------------------------------------------------------------------------------------
    def GetU(self, Action):
        if Action in [0, 4, 5, 12, 13, 19, 20, 21, 22]:
            return (0,0,0,0,self.dt()) # Stop or kick
        elif Action == 11:
            return (0,0,0,1,self.dt()) # Gait
        elif Action == 1:
            return (20,0,0,1,self.dt()) # Fast Walk Forward
        elif Action == 8:
            return (10,0,0,1,self.dt()) # Slow Walk Forward
        elif Action == 17:
            return (-20,0,0,1,self.dt()) # Fast Walk Backward
        elif Action == 18:
            return (-10,0,0,1,self.dt()) # Slow Walk Backward
        elif Action == 6:
            return (0,-10,0,1,self.dt()) # Walk Left
        elif Action == 7:
            return (0,10,0,1,self.dt()) # Walk Right
        elif Action == 2:
            return (0,0,20,1,self.dt()) # Turn Right
        elif Action == 3:
            return (0,0,-20,1,self.dt()) # Turn Left
        elif Action == 9:
            return (0,-10,-20,1,self.dt()) # Turn Left Around the Ball
        elif Action == 14:
            return (0,10,20,1,self.dt()) # Turn Right Around the Ball
        elif Action == 16:
            return (0,0,0,2,self.dt()) # Get up, back up
        elif Action == 15:
            return (0,0,0,3,self.dt()) # Get up, front up
        elif Action == 10:
            print "ERROR - Please, edit Localization.GetU() for Goalkeeper before resuming!"
            return (0,0,0,0,self.dt())

    #----------------------------------------------------------------------------------------------
    #   This method returns the time since the last update
    #----------------------------------------------------------------------------------------------
    def dt(self):
        auxtime = time.time()
        timer = auxtime - self.timestamp
        self.timestamp = auxtime
        return timer

def mean(vec):
    s = 0
    n = 0
    m = 0
    for x in vec:
        if x != -999:
            n += 1
            s += x*n
            m += n
    if n == 0:
        return -999
    else:
        return s/m

#Call the main function, start up the simulation
if __name__ == "__main__":
    Loc = Localization()
    Loc.main()