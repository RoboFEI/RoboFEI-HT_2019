__author__ = "RoboFEI-HT"
__authors__ = "Aislan C. Almeida"
__license__ = "GNU General Public License v3.0"

from Viewer import *
from MCL import *
import time

import argparse
# Import a shared memory
import sys
sys.path.append('../../Blackboard/src/')
from SharedMemory import SharedMemory 
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

class Localization():
    def __init__(self):

        self.bkb = SharedMemory()
        config = ConfigParser()

        try:
            config.read('../../Control/Data/config.ini')
            mem_key = int(config.get('Communication', 'no_player_robofei'))*100
        except:
            print "#----------------------------------#"
            print "#   Error loading config parser.   #"
            print "#----------------------------------#"
            sys.exit()

        self.Mem = self.bkb.shd_constructor(mem_key)

        parser = argparse.ArgumentParser(description='Robot Localization', epilog= 'Implements particle filters to self-localize a robot on the field.')
        parser.add_argument('--nothing', '--n', action="store_true", help='Nothing yet.')

        args = parser.parse_args()

        if args.nothing:
            print "DO NOTHING"
        else:
            print "DO NOT DO NOTHING"

        self.timestamp = time.time()

        self.bkb.write_float(self.Mem, 'VISION_BLUE_LANDMARK_DEG', -999)
        self.bkb.write_float(self.Mem, 'VISION_RED_LANDMARK_DEG', -999)
        self.bkb.write_float(self.Mem, 'VISION_YELLOW_LANDMARK_DEG', -999)
        self.bkb.write_float(self.Mem, 'VISION_PURPLE_LANDMARK_DEG', -999)

    def main(self):
        screen = Screen()

        simul = Simulation(screen)

        field = SoccerField(screen)

        simul.field = field

        PF = MonteCarlo(5000)

        #Main loop
        while True:

            #Process events
            simul.perform_events()

            u = self.GetU(self.bkb.read_int(self.Mem, 'DECISION_ACTION_A'))

            z0 = self.bkb.read_float(self.Mem, 'VISION_BLUE_LANDMARK_DEG')
            self.bkb.write_float(self.Mem, 'VISION_BLUE_LANDMARK_DEG', -999)
            z1 = self.bkb.read_float(self.Mem, 'VISION_RED_LANDMARK_DEG')
            self.bkb.write_float(self.Mem, 'VISION_RED_LANDMARK_DEG', -999)
            z2 = self.bkb.read_float(self.Mem, 'VISION_YELLOW_LANDMARK_DEG')
            self.bkb.write_float(self.Mem, 'VISION_YELLOW_LANDMARK_DEG', -999)
            z3 = self.bkb.read_float(self.Mem, 'VISION_PURPLE_LANDMARK_DEG')
            self.bkb.write_float(self.Mem, 'VISION_PURPLE_LANDMARK_DEG', -999)

            if z0 == -999:
                z0 = None
            if z1 == -999:
                z1 = None
            if z2 == -999:
                z2 = None
            if z3 == -999:
                z3 = None

            z = [z0, z1, z2, z3]
                    
            # Perform Motion Update
            PF.main(u,z)

            #update soccer field
            field.draw_soccer_field()

            #Draw robots, ball and update the current frame
            simul.display_update(PF.particles)

            #Pause for the next frame
            screen.clock.tick(60)

    def GetU(self, Action):
        if Action == 0:
            return self.ctrl_Stop()
        elif Action == 11:
            return self.ctrl_Gait()
        elif Action == 1:
            return self.ctrl_FFWalk()
        elif Action == 8:
            return self.ctrl_SFWalk()
        elif Action == 17:
            return self.ctrl_FBWalk()
        elif Action == 18:
            return self.ctrl_SBWalk()
        elif Action == 6:
            return self.ctrl_LWalk()
        elif Action == 7:
            return self.ctrl_RWalk()
        elif Action == 2:
            return self.ctrl_LTurn()
        elif Action == 3:
            return self.ctrl_RTurn()
        elif Action == 9:
            return self.ctrl_LATurn()
        elif Action == 14:
            return self.ctrl_RATurn()

    def dt(self):
        auxtime = time.time()
        timer = auxtime - self.timestamp
        self.timestamp = auxtime
        return timer

    def ctrl_Stop(self):
        return (0,0,0,0,self.dt())

    def ctrl_Gait(self):
        return (0,0,0,1,self.dt())

    def ctrl_FFWalk(self):
        return (20,0,0,1,self.dt())

    def ctrl_SFWalk(self):
        return (10,0,0,1,self.dt())

    def ctrl_FBWalk(self):
        return (-20,0,0,1,self.dt())

    def ctrl_SBWalk(self):
        return (-10,0,0,1,self.dt())

    def ctrl_LWalk(self):
        return (0,-10,0,1,self.dt())

    def ctrl_RWalk(self):
        return (0,10,0,1,self.dt())

    def ctrl_LTurn(self):
        return (0,0,20,1,self.dt())

    def ctrl_RTurn(self):
        return (0,0,-20,1,self.dt())

    def ctrl_RATurn(self):
        return (0,10,-20,1,self.dt())

    def ctrl_LATurn(self):
        return (0,-10,20,1,self.dt())


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

        print self.bkb.read_float(self.Mem, 'VISION_BLUE_LANDMARK_DEG')

        #Process events
        simul.perform_events()

        # z = Meas[i]
        # PF.main(u, z)
        
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
    Loc = Localization()
    Loc.main()
    # Test()
