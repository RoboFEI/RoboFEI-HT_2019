__author__ = "RoboFEI-HT"
__authors__ = "Aislan C. Almeida"
__license__ = "GNU General Public License v3.0"

from Viewer import * # Imports the environment of the viewer
from MCL import * # Imports the Particle Filter Class
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

        # To parse arguments on execution
        parser = argparse.ArgumentParser(description='Robot Localization', epilog= 'Implements particle filters to self-localize a robot on the field.')
        parser.add_argument('--nothing', '--n', action="store_true", help='Nothing yet.')

        args = parser.parse_args()

        if args.nothing:
            print "DO NOTHING"
        else:
            print "DO NOT DO NOTHING"

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
        screen = Screen() # Creates a new screen

        simul = Simulation(screen) # Creates the interface structure

        field = SoccerField(screen) # Draws the field

        simul.field = field # Passes the field to the simulation

        PF = MonteCarlo(5000) # Starts the Particle Filter

        # Main loop
        while True:

            self.bkb.write_int(self.Mem, 'LOCALIZATION_WORKING', 1) # Sets the flag for telemetry

            # Process interactions events
            simul.perform_events()

            # Gets the motion command from the blackboard.
            u = self.GetU(self.bkb.read_int(self.Mem, 'DECISION_ACTION_A'))

            # Gets the measured variable from the blackboard,
            # and free them.
            z0 = self.bkb.read_float(self.Mem, 'VISION_BLUE_LANDMARK_DEG')
            self.bkb.write_float(self.Mem, 'VISION_BLUE_LANDMARK_DEG', -999)
            z1 = self.bkb.read_float(self.Mem, 'VISION_RED_LANDMARK_DEG')
            self.bkb.write_float(self.Mem, 'VISION_RED_LANDMARK_DEG', -999)
            z2 = self.bkb.read_float(self.Mem, 'VISION_YELLOW_LANDMARK_DEG')
            self.bkb.write_float(self.Mem, 'VISION_YELLOW_LANDMARK_DEG', -999)
            z3 = self.bkb.read_float(self.Mem, 'VISION_PURPLE_LANDMARK_DEG')
            self.bkb.write_float(self.Mem, 'VISION_PURPLE_LANDMARK_DEG', -999)

            # TODO - Pass this convertion to the Particle.Sensor() method.
            # if z0 == -999:
            #     z0 = None
            # if z1 == -999:
            #     z1 = None
            # if z2 == -999:
            #     z2 = None
            # if z3 == -999:
            #     z3 = None

            # Mounts the vector to be sent
            z = [z0, z1, z2, z3]
                    
            # Performs Particle Filter's Update
            pos, std = PF.main(u,z)

            self.bkb.write_int(self.Mem, 'LOCALIZATION_X', int(pos[0]))
            self.bkb.write_int(self.Mem, 'LOCALIZATION_Y', int(pos[1]))
            self.bkb.write_int(self.Mem, 'LOCALIZATION_THETA', int(pos[2]))
            self.bkb.write_float(self.Mem, 'LOCALIZATION_RBT01_X', std)

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
        if Action == 0:
            return (0,0,0,0,self.dt()) # Stop
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

    #----------------------------------------------------------------------------------------------
    #   This method returns the time since the last update
    #----------------------------------------------------------------------------------------------
    def dt(self):
        auxtime = time.time()
        timer = auxtime - self.timestamp
        self.timestamp = auxtime
        return timer

#Call the main function, start up the simulation
if __name__ == "__main__":
    Loc = Localization()
    Loc.main()
