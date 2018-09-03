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
    new_network_architecture1 = []

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

    ## calculateWeight
    # .
    def __calculateWeight(self, score):
        self.weight = score
        #+\
        # 1./len(self.network_architecture) +\
        # 1./max(sum(self.network_architecture), 1)

    ## performance
    # .
    def performance(self, intrain, outtrain, intest, outtest):
        # training network
        self.__network.fit(intrain, outtrain)

        # testing network
        score = self.__network.score(intest, outtest)

        # calculating weight
        self.__calculateWeight(score)

    def setArchitecture(self, arc):
        self.network_architecture = arc

    # creates new archtetures throught genetic algorithms

    # cross architecture
    def cross(self, arch2):
        arc = None
        if len(self.network_architecture)>len(arch2):
            arc = 1*arch2
        else: arc = 1*self.network_architecture

        n = max(np.random.randint(len(arc)), 1) #Point of break on the list for crossing
        if n==len(arc-1): n = n -1

        if len(arc)!=1:
            self.new_network_architecture = np.concatenate(arch2[n::], self.network_architecture[::n])
            self.new_network_architecture1 = np.concatenate(self.network_architecture[n::], arch2[::n])

        if len(arc)==1:
            self.new_network_architecture = arch2 + self.network_architecture
            self.new_network_architecture1 = self.network_architecture + arch2

    # mutation algorithm
    def mutation(self):
        self.new_network_architecture = 1 * self.network_architecture # lista da nova arquitetura. Assim, mantendo a arquitetura original.
        n = max(np.random.randint(len(self.new_network_architecture)), 1) # quantas camadas serao afetadas
        for __ in xrange(n):
            m = np.random.randint(11)-5 # modifica a camada escolhida de -5 a 5.
            p = np.random.randint((len(self.new_network_architecture)))# Qual camada sera modificada
            self.new_network_architecture[p] = max(self.new_network_architecture[p]+m, 1)
