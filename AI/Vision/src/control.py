
import scipy.io as sio

class Control:
    sss = 0
    def __init__(self):
        self.sss = sio.loadmat("matlab.mat")
