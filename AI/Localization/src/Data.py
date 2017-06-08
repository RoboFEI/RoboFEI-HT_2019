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
parser.add_argument('-t', '--test', action="store_true", help='Test')

args = parser.parse_args()

qtdparts = 1000

if args.mcl:
    from MCL import *
elif args.amcl:
    from AMCL import *
elif args.srmcl:
    from SRMCL import *
elif args.test:
    from test import *
    qtdparts = 1000
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
        self.bkb.write_float(self.Mem, 'VISION_FIRST_GOALPOST', -999)
        self.bkb.write_float(self.Mem, 'VISION_SECOND_GOALPOST', -999)
        self.bkb.write_float(self.Mem, 'VISION_THIRD_GOALPOST', -999)
        self.bkb.write_float(self.Mem, 'VISION_FOURTH_GOALPOST', -999)
        self.bkb.write_float(self.Mem, 'VISION_FIELD', 0)

    #----------------------------------------------------------------------------------------------
    #   Localization's main method.
    #----------------------------------------------------------------------------------------------
    def main(self):
        screen = Screen(self.args.graphs) # Creates a new screen

        if self.args.graphs:
            simul = Simulation(screen) # Creates the interface structure
            field = SoccerField(screen) # Draws the field
            simul.field = field # Passes the field to the simulation

        index = 0

        self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', 999)

        while True:
            if index < 60 or 120 <= index and index < 180:
                PF = MonteCarlo(1000, 1000, [1, 2, 1, 0, 0,  1, 2, 1, 0, 0,  1, 2, 1, 0, 0]) # Starts the Particle Filter
            elif index < 120 or 180 <= index and index < 240:
                PF = MonteCarlo(1000, 30, [1, 2, 1, 0, 0,  1, 2, 1, 0, 0,  1, 2, 1, 0, 0]) # Starts the Particle Filter
            elif index < 300 or 360 <= index and index < 420:
                PF = MonteCarlo(1000, 1000, [1, 2, 1, 500, 0,  1, 2, 1, 500, 0,  1, 2, 1, 100, 0]) # Starts the Particle Filter
            elif index < 360 or 420 <= index and index < 480:
                PF = MonteCarlo(1000, 30, [1, 2, 1, 500, 0,  1, 2, 1, 500, 0,  1, 2, 1, 100, 0]) # Starts the Particle Filter

            std = 100
            hp = -999
            weight = 1

            flag = self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING')
            execute = False

            text = ""

            if flag == 11100:
                self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 0)
                execute = True
            elif flag == 11111:
                self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 0)
                exit()

            count = 0

            time.sleep(0.01)

            # There will be 8 experiments each executed 30 times for each 2 tracks, in the end it sums up to 480 archives!
            # - First, test the localization algorithm in its purity! 0~59
            #   - Uses both tracks separately.
            # - Second, test the use of standard deviation for changing particles quantity. 60~119
            #   - Uses both tracks separately.
            # - Third, test the Value of the Perfect Information. 120~179
            #   - Uses both tracks separately.
            # - Fourth, test both, the standard deviation and the VPI. 180~239
            #   - Uses both tracks separately.
            # - Fifth, test the particle error in function of its weight. 240~299
            #   - Uses both tracks alternated.
            # - Sixth, test the particle error and standard deviation. 300~359
            #   - Uses both tracks alternated.
            # - Seventh, test the particle error and VPI. 360~419
            #   - Uses both tracks alternated.
            # - Eighth, test everything at once. 420~479
            #   - Uses both tracks alternated.

            # Main loop
            while execute:
                flag = self.bkb.read_int(self.Mem, 'LOCALIZATION_WORKING')

                if flag == 11110:
                    index += 1
                    with open('/home/fei/Dropbox/Masters/Experiment/local'+str(index), 'w') as file:
                        file.write(text)
                    text = ""
                    self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', 999)
                    self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 0)
                    break
                elif flag == 11111:
                    self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 0)
                    exit()
                
                # Process interactions events
                if self.args.graphs:
                    simul.perform_events()

                # Gets the motion command from the blackboard.
                u = self.GetU(self.bkb.read_int(self.Mem, 'CONTROL_ACTION'))

                orientation = self.bkb.read_float(self.Mem, 'IMU_EULER_Z')

                # landmarks = []
                # landmarks.append(self.bkb.read_float(self.Mem, 'VISION_FIRST_GOALPOST'))
                # self.bkb.write_float(self.Mem, 'VISION_FIRST_GOALPOST', -999)
                # landmarks.append(self.bkb.read_float(self.Mem, 'VISION_SECOND_GOALPOST'))
                # self.bkb.write_float(self.Mem, 'VISION_SECOND_GOALPOST', -999)
                # landmarks.append(self.bkb.read_float(self.Mem, 'VISION_THIRD_GOALPOST'))
                # self.bkb.write_float(self.Mem, 'VISION_THIRD_GOALPOST', -999)
                # landmarks.append(self.bkb.read_float(self.Mem, 'VISION_FOURTH_GOALPOST'))
                # self.bkb.write_float(self.Mem, 'VISION_FOURTH_GOALPOST', -999)

                fieldpoints = self.bkb.read_float(self.Mem, 'VISION_FIELD')

                if fieldpoints == -999:
                    fieldpoints = None
                else:
                    self.bkb.write_float(self.Mem, 'VISION_FIELD', -999)

                landmarks = None

                if fieldpoints != None or landmarks != None:
                    z = [landmarks, fieldpoints, orientation]
                else:
                    z = [None, None, None]

                pos, std = PF.main(u,z)

                text += str(time.time()) + " " + str(pos[0]) + " " + str(pos[1]) + " " + str(pos[2]) + " " + str(std) + " " + str(PF.qtd) + "\n"

                if fieldpoints != None:
                    if (120 <= index and index < 240 or index > 360):
                        hp = PF.PerfectInformation(u, self.bkb.read_float(self.Mem, 'VISION_PAN_DEG'), 5)
                    else:
                        hp = -999
                self.bkb.write_int(self.Mem, 'DECISION_LOCALIZATION', hp)

                if PF.meanweight < 1:                
                    weight = PF.meanweight                

                if self.args.graphs:
                    # Redraws the screen background
                    field.draw_soccer_field()
                    simul.DrawStd(pos, std, weight, hp)

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
            return (0,0,18.7,1,self.dt()) # Turn Right
        elif Action == 3:
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

