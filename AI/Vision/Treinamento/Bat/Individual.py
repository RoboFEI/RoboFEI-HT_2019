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
class Individual( ):

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
    def __init__(self, net = None):
        if net is None:
            # Generating network architecture
            self.network_architecture = np.array(
                np.random.rand(
                    np.random.randint(9)+1  # quantidade de camadas aleatórias de 1 a 9
                )*49 + 1,  # adaptação necessaria
                dtype=int
            )
        else:
            self.network_architecture = net

        # Instantiated neural network
        self.__network = nn.MLPRegressor(
            solver='lbfgs',
            alpha=1e-5,
            hidden_layer_sizes=self.network_architecture,
            random_state=1,
            max_iter=10000
        )

    ## __calculateWeight
    # .
    def __calculateWeight(self, score):
        self.weight = score

    ## performance
    # .
    def performance(self, intrain, outtrain, intest, outtest):
        # training network
        self.__network.fit(intrain, outtrain)

        # testing network
        score = self.__network.score(intest, outtest)

        # calculating weight
        self.__calculateWeight(score)

    ## cross
    # .
    def cross(self, father):
        try:
            cutme = np.random.randint(len(self.network_architecture)-1)+1
        except ValueError:
            cutme = 1
        try:
            cutfather = np.random.randint(len(father.network_architecture)-1)+1
        except Exception as e:
            cutfather = 1


        son1 = np.concatenate([self.network_architecture[:cutme], father.network_architecture[cutfather:]])
        son2 = np.concatenate([father.network_architecture[:cutfather], self.network_architecture[cutme:]])

        return [Individual(son1), Individual(son2)]

    ## mutation
    # .
    def mutation(self):
        limit = 5

        wolverine = self.network_architecture.copy()

        wolverine[np.random.randint(0, len(self.network_architecture))] += np.random.randint(-limit, limit+1)

        return Individual(wolverine)
