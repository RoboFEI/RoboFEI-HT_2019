# coding: utf-8

# ****************************************************************************
# * @file: KalmanFilter.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class KalmanFilter
# ****************************************************************************

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append("../include")
sys.path.append("../src")

# The standard libraries used in the visual memory system.
import time  # Libraries used for time management.
import numpy as np  # Used for matrix calculations.

# Used class developed by RoboFEI-HT.
from Basic import *  # Standard and abstract class.
from Speeds import *  # Class responsible for managing the robot"s possible speeds (me).


## Class to KalmanFilter
class KalmanFilter(Basic):
    '''Class responsible for implementing kalman filter methods.'''

    __metaclass__ = ABCMeta

    # ---- Variables ----

    ## _parameters
    # Variable used to instantiate class responsible for robot speed.
    _parameters = None

    ## _speeds
    # Variable used to instantiate class responsible for robot speed.
    _speeds = None

    ## _t
    # Time variable used in kalman filter.
    _t = None

    ## _predictedstate
    # Variable used to make predictions from observations.
    _predictedstate = None

    ## _state
    # Variable used to predict the position of the object at the current instant.
    _state = None

    # Matrix used in kalman filter.
    _A = None
    _B = None
    _R = None
    _C = None
    _Q = None

    # _Status variables.
    _px = None
    _py = None
    _vx = None
    _vy = None
    _ax = None
    _ay = None
    _b_x = None
    _b_y = None

    # _Support variables.
    _sin = None
    _cos = None

    ## _reset
    def _reset(self):
        '''Function used to reset states.'''

        # Creating the Kalman Filter Matrix
        self._A = sym.Matrix([
            [1, 0, self._t, 0, 0.5 * self._t**2, 0],
            [0, 1, 0, self._t, 0, 0.5 * self._t**2],
            [0, 0, 1, 0, self._t, 0],
            [0, 0, 0, 1, 0, self._t],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1],
        ])

        self._B = sym.Matrix([
            [-self._t, 0, -0.5 * self._t**2, 0, self._px],
            [0, -self._t, 0, -0.5 * self._t**2, self._py],
            [
                0, 0, 0, 0,
                self._vx - self._vx * (1 - self._cos) + self._vy * self._sin
            ],
            [
                0, 0, 0, 0,
                self._vy - self._vy * (1 - self._cos) + self._vx * self._sin
            ],
            [
                0, 0, 0, 0,
                self._ax - self._ax * (1 - self._cos) - self._ay * self._sin
            ],
            [
                0, 0, 0, 0,
                self._ay - self._ay * (1 - self._cos) + self._ax * self._sin
            ],
        ])

        self._R = sym.Matrix(sym.Identity(6))

        self._C = sym.Matrix([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
        ])

        self._Q = sym.Matrix(
            sym.Identity(2) * self._parameters["vision_error"])

        # Initial state
        self._predictedstate["x"] = sym.Matrix([0, 0, 0, 0, 0, 0])
        self._predictedstate["covariance"] = sym.Matrix(
            sym.Identity(6) * 10 * self._parameters["vision_error"])
        self._predictedstate["time"] = -1

        self._state = copy(self._predictedstate)

    ## Constructor Class
    @abstractmethod
    def __init__(self, a, s, obj):
        '''Responsible for starting the matrices of kalman patterns.'''
        self._predictedstate = {}
        self._state = {}

        # Instantiating parent class
        super(KalmanFilter, self).__init__(a, "Kalman Filter", obj)

        # Creating standard parameters and reading
        self._parameters = {
            "vision_error": 0.1,
            "linear_acceleration": False,
        }

        self._parameters = self._conf.readVariables(self._parameters)

        # Variable to robot speed
        self._speeds = s

        self._t = sym.symbols("t")  # Declaring variable time

        # _Status variables
        self._px, self._py = sym.symbols("p_x p_y")
        self._vx, self._vy = sym.symbols("v_x v_y")
        self._ax, self._ay = sym.symbols("a_x a_y")

        # _Sine and cosine variables
        self._cos, self._sin = sym.symbols("C S")

    ## __listVariables
    # .
    def __listVariables(self, tnow, movements, data):
        '''Create list of variables that will be used in the formulas.'''

        # Tested null acceleration condition
        if self._speeds[movements]["x_speed"][2,
                                              0] != 0.0 or self._speeds[movements]["x_speed"][3,
                                                                                              0] != 0:
            listsub = [
                # Auxiliary variables
                [
                    self._cos,
                    sym.cos(
                        sym.atan2(0.5 * self._speeds[movements]["x_speed"][
                            3, 0] * self._t**2, 0.5 * self._speeds[movements][
                                "x_speed"][2, 0] * self._t**2))
                ],
                [
                    self._sin,
                    sym.sin(
                        sym.atan2(0.5 * self._speeds[movements]["x_speed"][
                            3, 0] * self._t**2, 0.5 * self._speeds[movements][
                                "x_speed"][2, 0] * self._t**2))
                ],
                [self._t, tnow - data["time"]],  # Inserting delta time

                # State Variables
                [self._px, data["x"][0, 0]],
                [self._py, data["x"][1, 0]],
                [self._vx, data["x"][2, 0]],
                [self._vy, data["x"][3, 0]],
            ]
        else:
            listsub = [
                # Auxiliary variables
                [self._cos, 1],
                [self._sin, 0],
                [self._t, tnow - data["time"]],  # Inserting delta time

                # State Variables
                [self._px, data["x"][0, 0]],
                [self._py, data["x"][1, 0]],
                [self._vx, data["x"][2, 0]],
                [self._vy, data["x"][3, 0]],
            ]

        if len(data["x"]) == 6:
            listsub.extend([
                [self._ax, data["x"][4, 0]],
                [self._ay, data["x"][5, 0]],
            ])

        return listsub

    ## __predictNow
    def __predictNow(self, tnow=None, movements=None):
        '''Performs the prediction using the current instant in time to determine the new state.'''

        self._state = copy(self._predictedstate)

        # Checking if you can hear at least one measurement.
        if self._state["time"] == -1:
            return
        else:
            tnow = time.time()

        #--------------------------------------------------------------------------------------------------

        # Calculating stop time (speed equal to zero)
        if self._parameters["linear_acceleration"] == False and len(
                self._state["x"]) == 6:
            times = [tnow]
            for i in xrange(2, 4):
                a = -self._state["x"][i] / self._state["x"][i + 2]
                if a == sym.nan or a == sym.zoo or a < 0:
                    times.append(tnow)
                else:
                    times.append(float(self._state["time"] + a))
            while tnow > min([n for n in times if n >= 0]):
                self.self._predict(
                    tnow=min([n for n in times if n > 0]), movements=movements)
                times = [tnow]
                for i in xrange(2, 4):
                    a = -self._state["x"][i] / self._state["x"][i + 2]
                    if a == sym.nan or a == sym.zoo:
                        times.append(tnow)
                    else:
                        times.append(float(self._state["time"] + a))

        #--------------------------------------------------------------------------------------------------

        listsub = self.__listVariables(tnow, movements, self._state)

        # Calculating states
        self._state["x"] = (
            self._A * self._state["x"]  # A * x
        ).subs(listsub)

        listsub = self.__listVariables(tnow, movements, self._state)

        self._state["x"] = (
            self._B * self._speeds[movements]["x_speed"]  # B * U
        ).subs(listsub)

        listsub = self.__listVariables(tnow, movements, self._state)

        #--------------------------------------------------------------------------------------------------

        # Calculating covariance
        self._state["covariance"] = (
            2 * self._A * self._state["covariance"] * sym.transpose(self._A) +
            self._R * self._speeds[movements]["R"]
            [:self._R.shape[0], :self._R.shape[1]]  # A*covariance*A.T + R
        ).subs(listsub)

        #--------------------------------------------------------------------------------------------------

        # Rounding value with precision
        self._state["x"] = sym.Matrix(self._state["x"])
        for x in xrange(len(self._state["x"])):
            try:
                if abs(self._state["x"][x, 0]) < self._parameters["precision"]:
                    self._state["x"][x, 0] = 0.0
            except TypeError:
                self._state["x"][x, 0] = 0.0

        #--------------------------------------------------------------------------------------------------

        # Resetting acceleration if velocity is zero.
        if self._parameters["linear_acceleration"] == False and len(
                self._state["x"]) >= 6:
            for x in xrange(2, len(self._state["x"]) - 2):
                if abs(self._state["x"][x, 0]) == 0.0:
                    self._state["x"][x + 2, 0] = 0.0

        self._state["time"] = tnow

    ## __predictTime
    def __predictTime(self, tnow=None, movements=None):
        '''Uses a current instant in time and updates the observation and the current state.'''

        # Checking if you can hear at least one measurement.
        if self._predictedstate["time"] == -1:
            self._predictedstate["time"] = tnow

        #--------------------------------------------------------------------------------------------------

        # Calculating stop time (speed equal to zero)
        if self._parameters["linear_acceleration"] == False and len(
                self._predictedstate["x"]) == 6:
            times = [tnow]
            for i in xrange(2, 4):
                a = -self._predictedstate["x"][i] / self._predictedstate["x"][
                    i + 2]
                if a == sym.nan or a == sym.zoo or a < 0:
                    times.append(tnow)
                else:
                    times.append(float(self._predictedstate["time"] + a))
            while tnow > min([n for n in times if n >= 0]):
                self.self._predict(
                    tnow=min([n for n in times if n > 0]), movements=movements)
                times = [tnow]
                for i in xrange(2, 4):
                    a = -self._predictedstate["x"][i] / self._predictedstate[
                        "x"][i + 2]
                    if a == sym.nan or a == sym.zoo:
                        times.append(tnow)
                    else:
                        times.append(float(self._predictedstate["time"] + a))

        #--------------------------------------------------------------------------------------------------

        listsub = self.__listVariables(tnow, movements, self._predictedstate)

        # Calculating states

        self._predictedstate["x"] = (
            self._A * self._predictedstate["x"]  # A * x
        ).subs(listsub)

        listsub = self.__listVariables(tnow, movements, self._predictedstate)

        self._predictedstate["x"] = (
            self._B * self._speeds[movements]["x_speed"]  # B * U
        ).subs(listsub)

        listsub = self.__listVariables(tnow, movements, self._predictedstate)

        #--------------------------------------------------------------------------------------------------

        # Calculating covariance
        self._predictedstate["covariance"] = (
            self._A * self._predictedstate["covariance"] *
            sym.transpose(self._A) + self._R * self._speeds[movements]["R"]
            [:self._R.shape[0], :self._R.shape[1]]  # A*covariance*A.T + R
        ).subs(listsub)

        #--------------------------------------------------------------------------------------------------

        # Rounding value with precision
        self._predictedstate["x"] = sym.Matrix(self._predictedstate["x"])
        for x in xrange(len(self._predictedstate["x"])):
            try:
                if abs(self._predictedstate["x"]
                       [x, 0]) < self._parameters["precision"]:
                    self._predictedstate["x"][x, 0] = 0.0
            except TypeError:
                self._predictedstate["x"][x, 0] = 0.0

        #--------------------------------------------------------------------------------------------------

        # Resetting acceleration if velocity is zero.
        if self._parameters["linear_acceleration"] == False and len(
                self._predictedstate["x"]) == 6:
            for x in xrange(2, len(self._predictedstate["x"]) - 2):
                if abs(self._predictedstate["x"][x, 0]) == 0.0:
                    self._predictedstate["x"][x + 2, 0] = 0.0

        self._predictedstate["time"] = tnow

    ## predict
    def _predict(self, tnow=None, movements=None):
        '''Used to predict the object.'''

        {
            (float, int): self.__predictTime,
            (type(None), int): self.__predictNow,
        }[(type(tnow), type(movements))](tnow, movements)

    ## update
    def _update(self, data):
        '''Function used to perform the data update.'''

        # Predicting value in observation time.
        self._predict(data["time"], data["movement"])

        k = self._predictedstate["covariance"] * sym.transpose(
            self._C) * sym.inv_quick(  # covariance*C.T*(_)^(-1)
                self._C * self._predictedstate["covariance"] * sym.transpose(
                    self._C) + self._Q  # C*covariance*C.T + Q
            )

        z = sym.Matrix(data["pos"])

        self._predictedstate["x"] = self._predictedstate["x"] + k * (
            z - self._C * self._predictedstate["x"])  # x + k*(z - C*X)
        self._predictedstate["covariance"] = (
            sym.Matrix(sym.Identity(len(self._predictedstate["x"]))) -
            k * self._C
        ) * self._predictedstate["covariance"]  # (I - k*C)*covariance

        #--------------------------------------------------------------------------------------------------

        # Rounding value with precision
        self._predictedstate["x"] = sym.Matrix(self._predictedstate["x"])
        for x in xrange(len(self._predictedstate["x"])):
            try:
                if abs(self._predictedstate["x"]
                       [x, 0]) < self._parameters["precision"]:
                    self._predictedstate["x"][x, 0] = 0.0
            except TypeError:
                self._predictedstate["x"][x, 0] = 0.0

        #--------------------------------------------------------------------------------------------------

        # Resetting acceleration if velocity is zero.
        if self._parameters["linear_acceleration"] == False and len(
                self._predictedstate["x"]) == 6:
            for x in xrange(2, len(self._predictedstate["x"]) - 2):
                if abs(self._predictedstate["x"][x, 0]) == 0.0:
                    self._predictedstate["x"][x + 2, 0] = 0.0

        self._state = copy(self._predictedstate)
