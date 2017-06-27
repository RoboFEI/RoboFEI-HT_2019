import cv2
import numpy as np
import sys

sys.path.append('../../Blackboard/src/') # Creates a link to the Blackboard
from SharedMemory import SharedMemory # Imports Blackboard's class

#--------------------------------------------------------------------------------------------------
#   Class used for the vision system.
#--------------------------------------------------------------------------------------------------
class LocalizationVision():
    #----------------------------------------------------------------------------------------------
    #   Constructor gets the BlackBoard object and the memory key.
    #----------------------------------------------------------------------------------------------
    def __init__(self, bkb, mem):
        self.bkb = bkb # BlackBoard object
        self.mem = mem # Memory key

        # Try to load the points, if it doesn't work, kill the process.
        try:
            self.vector = np.load('vector.npy')
            print "\n-= Succeeded loading points. =-\n"
        except:
            print "\n-= Error loading points. =-\n"

            print "Run \"python pointsCalibration.py\" in order\nto calibrate the points for the Vision System."
            exit()

        self.vals = np.zeros(32)
        self.frames = 5
        self.count = 0

    def Main(self, mask, pan):
        p = []
        for i in self.vector:
            p.append(mask[tuple(i)])

        if self.count < self.frames:
            self.vals += np.array(p)
            self.count += 1
        else:
            self.vals /= self.frames * 255.
            x = np.rint(self.vals)
            s = np.mean(np.abs(self.vals-x))

            print '\nVals:\n', x
            print 'Error: ', s
            print 'intVF: ', write(x)
            print 'floatVF', int(pan) + np.sign(pan)*s

            self.bkb.write_int(self.mem, 'iVISION_FIELD', write(x))
            self.bkb.write_float(self.mem, 'fVISION_FIELD', int(pan)+s)

            self.vals = np.zeros(32)
            self.frames = 5
            self.count = 0

def write(v):
    x = 0
    for i in range(32):
        x += int(v[i]) << i
    # print v
    return x