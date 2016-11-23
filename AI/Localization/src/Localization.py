__author__ = "RoboFEI-HT"
__authors__ = "Aislan C. Almeida"
__license__ = "GNU General Public License v3.0"

from Viewer import *
from MCL import *
import argparse
# Import a shared memory
import sys
sys.path.append('../../Blackboard/src/')

from SharedMemory import SharedMemory 

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

bkb = SharedMemory()
config = ConfigParser()

try:
    config.read('../../Control/Data/config.ini')
    mem_key = int(config.get('Communication', 'no_player_robofei'))*100
except:
    print "#----------------------------------#"
    print "#   Error loading config parser.   #"
    print "#----------------------------------#"
    sys.exit()

Mem = bkb.shd_constructor(mem_key)

parser = argparse.ArgumentParser(description='Robot Localization', epilog= 'Implements particle filters to self-localize a robot on the field.')
parser.add_argument('--nothing', '--n', action="store_true", help='Nothing yet.')

args = parser.parse_args()

if args.nothing:
    print "DO NOTHING"
else:
    print "DO NOT DO NOTHING"

def main():
    screen = Screen()

    simul = Simulation(screen)

    field = SoccerField(screen)

    simul.field = field

    PF = MonteCarlo(1000)

    #Main loop
    while True:

        #Process events
        simul.perform_events()

        # Perform Motion Update
        PF.Prediction((100, 90, 1.0/60))

        #update soccer field
        field.draw_soccer_field()

        #Draw robots, ball and update the current frame
        simul.display_update(PF.particles)

        #Pause for the next frame
        screen.clock.tick(60)

def Test():
    screen = Screen()

    simul = Simulation(screen)

    field = SoccerField(screen)

    simul.field = field

    PF = MonteCarlo(1000)
    u = (100, 0, 1.0/60)
    z = (None, -298.42534123506925, -410.55561227401864, -343.7274482975523)
    PF.main(u, z)

    #Main loop
    while True:

        #Process events
        simul.perform_events()
        
        PF.Prediction((10, 90, 1.0/60))

        #update soccer field
        field.draw_soccer_field()

        #Draw robots, ball and update the current frame
        simul.display_update(PF.particles)

        #Pause for the next frame
        screen.clock.tick(60)

#Call the main function, start up the simulation
if __name__ == "__main__":
    # main()
    Test()