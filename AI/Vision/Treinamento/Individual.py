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

    ## Mutation network
    # network architecture created by the mutation and cross over of network_architecture
    new_network_architecture = []

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
        self.new_network_architecture = self.network_architecture
        print "cross"

    # mutation algorithm
    def __mutation(self):
        self.new_network_architecture = 1 * self.network_architecture # lista da nova arquitetura. Assim, mantendo a arquitetura original.
        n = max(np.random.randint(len(self.new_network_architecture)), 1) # quantas camadas serao afetadas
        for __ in xrange(n):
            m = np.random.randint(11)-5 # modifica a camada escolhida de -5 a 5.
            p = np.random.randint((len(self.new_network_architecture)))# Qual camada sera modificada
            self.new_network_architecture[p] = max(self.new_network_architecture[p]+m, 1)
        return self.new_network_architecture

    ## calculateWeight
    # .
    def __calculateWeight(self, score):
        self.weight = score +\
        1./len(self.network_architecture) +\
        1./max(sum(self.network_architecture), 1)

    ## performance
    # .
    def performance(self, intrain, outtrain, intest, outtest):
        # training network
        self.__network.fit(intrain, outtrain)

        # testing network
        score = self.__network.score(intest, outtest)

        # calculating weight
        self.__calculateWeight(score)

    # creates new archtetures throught genetic algorithms
    def geneticAlgorithm(self):
        return self.__mutation()

    def setArchitecture(self, arc):
        self.network_architecture = arc
