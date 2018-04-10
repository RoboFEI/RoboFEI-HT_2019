__author__ = "RoboFEI-HT"
__authors__ = "Aislan C. Almeida"
__license__ = "GNU General Public License v3.0"

from Viewer import * # Imports the environment of the viewer
from MCL import *
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

args = parser.parse_args()

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
        # self.bkb.write_float(self.Mem, 'VISION_FIRST_GOALPOST', -999)
        # self.bkb.write_float(self.Mem, 'VISION_SECOND_GOALPOST', -999)
        # self.bkb.write_float(self.Mem, 'VISION_THIRD_GOALPOST', -999)
        # self.bkb.write_float(self.Mem, 'VISION_FOURTH_GOALPOST', -999)
        self.bkb.write_int(self.Mem, 'iVISION_FIELD', 0)
        self.bkb.write_float(self.Mem, 'fVISION_FIELD', 0)

    #----------------------------------------------------------------------------------------------
    #   Localization's main method.
    #----------------------------------------------------------------------------------------------
    def main(self):
        screen = Screen(self.args.graphs) # Creates a new screen

        if self.args.graphs:
            simul = Simulation(screen) # Creates the interface structure
            field = SoccerField(screen) # Draws the field
            simul.field = field # Passes the field to the simulation

        PF = MonteCarlo(500)

        std = 100
        hp = -999
        self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', -999)
        weight = 1
        upflag = False

        # Main loop
        while True:
            landmarks = []

            self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 1) # Sets the flag for telemetry

            # Process interactions events
            if self.args.graphs:
                simul.perform_events()

            # Gets the motion command from the blackboard.
            u = self.GetU(self.bkb.read_int(self.Mem, 'CONTROL_ACTION'))

            # Gets the measured variable from the blackboard,
            # and free them.
            # landmarks.append(self.bkb.read_float(self.Mem, 'VISION_FIRST_GOALPOST'))
            # self.bkb.write_float(self.Mem, 'VISION_FIRST_GOALPOST', -999)
            # landmarks.append(self.bkb.read_float(self.Mem, 'VISION_SECOND_GOALPOST'))
            # self.bkb.write_float(self.Mem, 'VISION_SECOND_GOALPOST', -999)
            # landmarks.append(self.bkb.read_float(self.Mem, 'VISION_THIRD_GOALPOST'))
            # self.bkb.write_float(self.Mem, 'VISION_THIRD_GOALPOST', -999)
            # landmarks.append(self.bkb.read_float(self.Mem, 'VISION_FOURTH_GOALPOST'))
            # self.bkb.write_float(self.Mem, 'VISION_FOURTH_GOALPOST', -999)
            
            orientation = self.bkb.read_float(self.Mem, 'IMU_EULER_Z')

            x = self.bkb.read_int(self.Mem, 'iVISION_FIELD')
            y = self.bkb.read_float(self.Mem, 'fVISION_FIELD')
            fieldpoints = [read(x), y]
            
            if x == 0:
                fieldpoints = None
            else:
                self.bkb.write_int(self.Mem, 'iVISION_FIELD', 0)
                self.bkb.write_float(self.Mem, 'fVISION_FIELD', 0)

            # if sum(landmarks) == - 4 * 999:
            #     landmarks = None

            # fieldpoints = None
            # orientation = None
            landmarks = None

            if fieldpoints == None and landmarks == None:
                z = [None, None, None]
            else:
                z = [landmarks, fieldpoints, orientation]

            pos, std = PF.main(u,z)

            # if std > 8 and upflag:
            #     upflag = False
            # elif std < 4 and not upflag:
            #     upflag = True

            if upflag:
                hp = -999
                self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', -999)
            elif fieldpoints != None or self.bkb.read_int(self.Mem, 'DECISION_LOCALIZATION') == 999:
                hp = PF.PerfectInformation(u, self.bkb.read_float(self.Mem, 'VISION_PAN_DEG'), 5)
                self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', hp)

            # hp = self.bkb.read_int(self.Mem, 'DECISION_LOCALIZATION')
            # if fieldpoints != None and hp == -999 and std > 7 or hp == 999:
            #     hp = PF.PerfectInformation(u, self.bkb.read_float(self.Mem, 'VISION_PAN_DEG'), 5)
            #     self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', hp)
            # elif fieldpoints != None and hp == -999 and std < 3:
            #     self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', -999)

            if PF.meanweight < 1:                
                weight = np.log(0.05)/np.log(PF.meanweight)
            
            if self.args.log:
                print '\t\x1b[32mRobot at', # Prints header
                print 'ent\x1b[32m[x:\x1b[34m{} cm'.format(int(pos[0])), #  Prints the x position
                print '\x1b[32m| y:\x1b[34m{} cm'.format(int(pos[1])), # Prints the y position
                print u'\x1b[32m| \u03B8:\x1b[34m{}\u00B0'.format(int(pos[2])), # Prints the theta
                print u'\x1b[32m| \u03C3:\x1b[34m{} cm\x1b[32m]'.format(int(std)) # Prints the standard deviation

            # Write the robot's position on Black Board to be read by telemetry
            self.bkb.write_int(self.Mem, 'LOCALIZATION_X', int(pos[0]))
            self.bkb.write_int(self.Mem, 'LOCALIZATION_Y', int(pos[1]))
            self.bkb.write_int(self.Mem, 'LOCALIZATION_THETA', int(pos[2]))
            self.bkb.write_float(self.Mem, 'LOCALIZATION_RBT01_X', std)

            if self.args.graphs:
                # Redraws the screen background
                field.draw_soccer_field()
                simul.DrawStd(pos, std, weight, hp)

                # Draws all particles on screen
                simul.display_update(PF.particles)

            # Updates for the next clock
            screen.clock.tick(5)

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
        elif Action == 3:
            return (0,0,18.7,1,self.dt()) # Turn Right
        elif Action == 2:
            return (0,0,-18.7,1,self.dt()) # Turn Left
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

def read(x):
    v = []
    for i in xrange(31, -1, -1):
        aux = x >> i
        x -= aux << i
        v.insert(0, abs(aux))

    return v

#Call the main function, start up the simulation
if __name__ == "__main__":
    Loc = Localization()
    Loc.main()

