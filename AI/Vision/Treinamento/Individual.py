# coding: utf-8

# ****************************************************************************
# * @file: Individual.py
# * @project: ROBOFEI-HT - FEI 😛
# * @author: Vinicius Nicassio Ferreira
# * @version: V0.0.1
# * @created: 23/10/2017
# * @e-mail: vinicius.nicassio@gmail.com
# * @brief: Class Individual
# ****************************************************************************

# ---- Imports ----

# The standard libraries used in the vision system.
import numpy as np
import sklearn.neural_network as nn
from sklearn.externals import joblib
import random

# The standard libraries used in the visual memory system.

# Used class developed by RoboFEI-HT.

## Class Individual
# .


class Individual():

    # ---- Variables ----

    ## network_architecture
    # The vector representing neural network architecture.
    network_architecture = None

    ## network
    # The neural network created based on vector network_architecture.
    __network = None

    ## weight
    # .
    weight = None

    ## Constructor Class
    def __init__(self):
        # Generating network architecture
        self.network_architecture = np.array(
            np.random.rand(
                np.random.randint(9)+1  # quantidade de camadas aleatórias de 1 a 9
            )*49 + 1,  # adaptação necessaria
            dtype=int
        )

        # Generating network architecture
        self.__network = nn.MLPRegressor(
            solver='lbfgs',
            alpha=1e-5,
            hidden_layer_sizes=self.network_architecture,
            random_state=1,
            max_iter=10000
        )

    # cross architecture
    def __cross(self):
        print "cross"

    # mutation algorithm
    def __mutation(self):
        print "mut"

    def __geneticAlgortithm():
        print"oi"

    ## calculateWeight
    # .
    def __calculateWeight(self, score):
        self.weight = score +\
        1./len(self.network_architecture) +\
        1./sum(self.network_architecture)

    ## performance
    # .
    def performance(self, intrain, outtrain, intest, outtest):
        # training network
        self.__network.fit(intrain, outtrain)

        # testing network
        score = self.__network.score(intest, outtest)

        # calculating weight
        self.__calculateWeight(score)
