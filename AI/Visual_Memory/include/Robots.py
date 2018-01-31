# coding: utf-8

# ****************************************************************************
# * @file: Robots.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class Robots
# ****************************************************************************

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append("../include")
sys.path.append("../src")

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.
from BasicThread import *  # Responsible for implementing the methods and variables responsible for managing the thread.


## Class to Robots
# Class responsible for performing robots tracking.
class Robots(BasicThread):

    # ---- Variables ----

    ## listfunction
    # .
    __listfunction = None

    ## robotnumber
    # .
    __robotnumber = None

    ## posdata
    # .
    __posdata = None

    ## contreset
    # .
    __contreset = 0

    ## __lastposdata
    # .
    __lastposdata = None

    ## timenumber
    # .
    timenumber = 0

    ## weight
    # .
    weight = 0

    ## reset
    # .
    def reset(self):
        self.__listfunction = []

        while not self._threadPaused():
            pass

        super(Robots, self)._reset()

        self._A = self._A[:-2, :-2]
        self._B = self._B[:-2, :]
        self._R = self._R[:-2, :-2]
        self._C = self._C[:, :-2]

        self._predictedstate["x"] = self._predictedstate["x"][:-2, :]
        self._predictedstate["covariance"] = self._predictedstate[
            "covariance"][:-2, :-2]

        if self.timenumber == 0:
            return
        elif self.timenumber < 0:
            self._bkb.write_float(
                "VISUAL_MEMORY_OP_" + str(-self.timenumber).zfill(2) + "_X", 0)
            self._bkb.write_float(
                "VISUAL_MEMORY_OP_" + str(-self.timenumber).zfill(2) + "_Y", 0)
            self._bkb.write_float("VISUAL_MEMORY_OP_" +
                                  str(-self.timenumber).zfill(2) + "_MAX_VEL",
                                  0)
            self._bkb.write_float(
                "VISUAL_MEMORY_OP_" + str(-self.timenumber).zfill(2) + "_LOC",
                0)
        else:
            self._bkb.write_float(
                "VISUAL_MEMORY_AL_" + str(self.timenumber).zfill(2) + "_X", 0)
            self._bkb.write_float(
                "VISUAL_MEMORY_AL_" + str(self.timenumber).zfill(2) + "_Y", 0)
            self._bkb.write_float("VISUAL_MEMORY_AL_" +
                                  str(self.timenumber).zfill(2) + "_MAX_VEL",
                                  0)
            self._bkb.write_float(
                "VISUAL_MEMORY_AL_" + str(self.timenumber).zfill(2) + "_LOC",
                0)
        self.timenumber = 0

    ## Constructor Class
    def __init__(self, a, s, pos, n):
        # Instantiating constructor for inherited class.
        super(Robots, self).__init__(a, s, "Robots")

        self.timenumber = n

        self.__posdata = pos

        # Creating characteristic variables for Robots and reading.
        self._parameters.update({"precision": 0.6})
        self._parameters = self._conf.readVariables(self._parameters)

        self.reset()

        self.start()

    ## __predictVector
    # .
    def __predictVector(self, vector):
        tnow, movements = vector
        super(Robots, self)._predict(tnow, movements)

        if tnow == None and self._args.savedata == True:
            try:
                a = np.load("./Data/" + self.getName() + "-Robots.npy")
                a = np.concatenate(
                    (a, [[
                        self._state["time"],
                        [float(i) for i in self._state["x"][:, 0]],
                        [
                            self._state["covariance"][i, i]
                            for i in xrange(self._state["covariance"].shape[0])
                        ],
                        [float(i) for i in self._state["covariance"][:, 0]],
                        self.timenumber,
                    ]]),
                    axis=0)
            except IOError:
                a = [[
                    self._state["time"],
                    [float(i) for i in self._state["x"][:, 0]],
                    [
                        self._state["covariance"][i, i]
                        for i in xrange(self._state["covariance"].shape[0])
                    ],
                    [float(i) for i in self._state["covariance"][:, 0]],
                    self.timenumber,
                ]]
            np.save("./Data/" + self.getName() + "-Robots", a)
        if tnow == None and self.timenumber != 0:
            if self._predictedstate["covariance"][0,
                                                  0] > self._parameters['vision_error'] or self._predictedstate["covariance"][1,
                                                                                                                              1] > self._parameters['vision_error']:
                if self.timenumber > 0:
                    self._bkb.write_float(
                        "VISUAL_MEMORY_AL_" +
                        str(int(self.timenumber)).zfill(2) + "_LOC", 0)
                else:
                    self._bkb.write_float(
                        "VISUAL_MEMORY_OP_" +
                        str(-int(self.timenumber)).zfill(2) + "_LOC", 0)

            elif self.timenumber > 0:
                self._bkb.write_float(
                    "VISUAL_MEMORY_AL_" + str(int(self.timenumber)).zfill(2) +
                    "_X", self._state["x"][0, 0])
                self._bkb.write_float(
                    "VISUAL_MEMORY_AL_" + str(int(self.timenumber)).zfill(2) +
                    "_Y", self._state["x"][1, 0])

                #             if sym.sqrt(self._state["x"][2, 0]**2 + self._state["x"][3, 0]**2) > self._bkb.read_float("VISUAL_MEMORY_AL_" + str(int(timenumber)).zfill(2) + "_MAX_VEL"):
                self._bkb.write_float(
                    "VISUAL_MEMORY_AL_" + str(int(self.timenumber)).zfill(2) +
                    "_MAX_VEL",
                    sym.sqrt(self._state["x"][2, 0]**2 + self._state["x"][3, 0]
                             **2))

                self._bkb.write_float(
                    "VISUAL_MEMORY_AL_" + str(int(self.timenumber)).zfill(2) +
                    "_LOC", 1)
            else:
                self._bkb.write_float(
                    "VISUAL_MEMORY_OP_" + str(-int(self.timenumber)).zfill(2) +
                    "_X", self._state["x"][0, 0])
                self._bkb.write_float(
                    "VISUAL_MEMORY_OP_" + str(-int(self.timenumber)).zfill(2) +
                    "_Y", self._state["x"][1, 0])

                #             if sym.sqrt(self._state["x"][2, 0]**2 + self._state["x"][3, 0]**2) > self._bkb.read_float("VISUAL_MEMORY_OP_" + str(-int(timenumber)).zfill(2) + "_MAX_VEL"):
                self._bkb.write_float(
                    "VISUAL_MEMORY_OP_" + str(-int(self.timenumber)).zfill(2) +
                    "_MAX_VEL",
                    sym.sqrt(self._state["x"][2, 0]**2 + self._state["x"][3, 0]
                             **2))

                self._bkb.write_float(
                    "VISUAL_MEMORY_OP_" + str(-int(self.timenumber)).zfill(2) +
                    "_LOC", 1)

    ## predictThread
    # .
    def predictThread(self, tnow=None, movements=None):
        self.__listfunction.append([self.__predictVector, [tnow, movements]])
        self._resume()

    ## updateVector
    # .
    def __updateVector(self, data):
        super(Robots, self)._update(data)

    ## updateThread
    # .
    def updateThread(self, data):
        self.__listfunction.append([self.__updateVector, data])
        self._resume()

    ## run
    # .
    def run(self):
        self._running = True
        while self._running:
            with self._pausethread:
                while self.__listfunction != []:
                    func, data = self.__listfunction.pop(0)
                    func(data)
            self._pause()

    ## end
    # .
    def end(self):
        self.__listfunction = []
        self._finalize()
        super(Robots, self)._end()

    ## calculatesDistance
    # .
    def calculatesDistance(self):
        if self.__lastposdata == self.__posdata[:2]:
            return

        self._predict(self.__posdata[2], 0)
        self.__lastposdata = copy(self.__posdata[:2])

        self.weight = sym.Matrix(
            self.__posdata[:2]) - self._predictedstate["x"][:2, :2]
        self.weight = 1. / (1 + (self.weight[0]**2 + self.weight[1]**2)**0.5)

    ## __lt__
    # .
    def __lt__(self, other):
        self.calculatesDistance()
        other.calculatesDistance()
        return self.weight < other.weight

    ## testReset
    def testReset(self):
        if self._state["covariance"][0,
                                     0] + self._state["covariance"][1,
                                                                    1] > 3 * self._parameters["vision_error"]:
            self.__contreset += 1
        else:
            self.__contreset = 0

        if self.__contreset == 20:
            self.reset()
            self.__contreset = 0
            return True
        else:
            return False
