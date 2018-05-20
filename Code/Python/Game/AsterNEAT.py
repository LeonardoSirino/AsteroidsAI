from PyNEAT import Genome, NEAT
import copy
import matplotlib.pyplot as plt
import numpy as np


myNEAT = NEAT()
myNEAT.SetInitialTopology(2, 4)
myNEAT.PrintSpecies()
print("\n\n")
for i in range(0, 2):
    myNEAT.RandomUpdate()
myNEAT.PrintSpecies()
