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

###################################################################################################
Meas = [[None, 16.776029596858255, None, -11.788398177594791],
        [None, 21.11561363593449, None, -27.340053884874557],
        [None, 18.44507091188988, None, -16.59456502293088],
        [None, 15.899967704028018, None, -23.507631033946133],
        [None, 20.696919821801547, None, -17.402454782416868],
        [None, 24.458838610704134, None, -19.808076257337422],
        [None, 21.417991892135387, None, -20.003506624542034],
        [None, 26.005742881135006, None, -18.613755385394867],
        [None, 18.163900092661915, None, -22.69732488508446],
        [None, 21.421797572449805, None, -18.212346750798872],
        [None, 14.792835746609367, None, -17.7806814009839],
        [None, 21.76659027115833, None, -22.514646089106016],
        [None, 22.050743207527624, None, -19.3509262115263],
        [None, 22.2339802708729, None, -21.50333343352544],
        [None, 23.71905807643153, None, -19.820709741019087],
        [None, 22.74467783621826, None, -21.18575695922514],
        [None, 20.103107769822426, None, -25.291745336777357],
        [None, 24.348853901657222, None, -23.247997154482928],
        [None, 20.426538750999715, None, -21.065157742925173],
        [None, 19.181093129138457, None, -24.25989413621879],
        [None, 20.260452224522414, None, -26.2964612353676],
        [None, 30.750075929448904, None, -18.568314905334823],
        [None, 19.7923412454438, None, -19.949901311569477],
        [None, 19.891366025784485, None, -20.097091491302724],
        [None, 26.283099268054563, None, -21.000300448997965],
        [None, 31.03677447960958, None, -17.082499670397475],
        [None, 26.230455416765174, None, -22.59711120417895],
        [None, 26.6547260624425, None, -24.890006373208116],
        [None, 22.4216821173148, None, -23.75845037038939],
        [None, 20.919418802465113, None, -26.098113274397267],
        [None, 16.772100579404807, None, -23.771379375611488],
        [None, 25.43402950019361, None, -26.763833051758766],
        [None, 28.10861888468595, None, -24.21725957254697],
        [None, 26.764565726323383, None, -21.867535264211714],
        [None, 27.155612586975636, None, -28.206341113542948],
        [None, 26.325062997528914, None, -22.710283744450326],
        [None, 27.59793213829151, None, -26.607182930935803],
        [None, 23.359294520261905, None, -25.30891057258969],
        [None, 24.971867692085926, None, -23.3251547585248],
        [None, 19.724721170560105, None, -26.478588574938815],
        [None, 25.551072087322687, None, -29.750651889853508],
        [None, 34.967927282223556, None, -30.917624701781747],
        [None, 29.25179914140719, None, -30.40437725518651],
        [None, 28.20833654986048, None, -27.72177383380312],
        [None, 29.76840729604976, None, -29.65605347745895],
        [None, 30.952893270017203, None, -22.971855639571658],
        [None, 27.059961168399695, None, -29.363888025384387],
        [None, 25.84244642589332, None, -27.23562526805551],
        [None, 26.380978466037586, None, -29.666355473615234],
        [None, 27.605773003034567, None, -31.70959847520863],
        [None, 28.567525541985457, None, -27.6840702118043],
        [None, 31.862432206948068, None, -28.23087991715935],
        [None, 27.40982612546359, None, -29.69993829508206],
        [None, 32.4212394263291, None, -32.77940933221336],
        [None, 29.36399848827077, None, -31.60925628181757],
        [None, 32.20349548537217, None, -30.021413115030754],
        [None, 32.059552559829335, None, -30.64177856271659],
        [None, 34.170670235640394, None, -26.4724907900232],
        [None, 30.65760410761663, None, -30.16101400372349],
        [None, 26.534486892718686, None, -37.569003014570015],
        [None, 31.622205623478447, None, -29.91122852432271],
        [None, 30.016918113772583, None, -31.379129151918082],
        [None, 30.365396213485987, None, -34.50611055129652],
        [None, 33.14645685974085, None, -33.057821711908694]]
###################################################################################################

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

    PF = MonteCarlo(5000)
    # u = (0, 0, 0, 1.0/60)
    # z = [58.90350285991855, -8.292980444757765, None, -51.1515784530202]
    # z = [-68.5667128132698, None, -383.98066009226767, -292.3215153042386]
    # z = [None, -6.055309739945574, None, None]

    # z = [None, None, None, None]

    # PF.main(u, z)
    # i = 0
    #Main loop
    while True:

        #Process events
        simul.perform_events()

        # z = Meas[i]
        PF.main(u, z)
        
        # u = (0, 0, 0, 1.0/60)
        # i+=1
        # print len(PF.particles)
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