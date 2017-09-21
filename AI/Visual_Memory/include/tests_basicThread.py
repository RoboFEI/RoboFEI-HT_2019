# coding: utf-8

# ---- Imports ----

# Libraries to be used.
import sys
sys.path.append('../include')
sys.path.append('../src')

# The standard libraries used in the vision system.

# Used class developed by RoboFEI-HT.
from BasicThread import *

s = Speeds( )

a = BasicThread(s, "Teste Thread")

a.start( )

a.resume( )

a.run( )