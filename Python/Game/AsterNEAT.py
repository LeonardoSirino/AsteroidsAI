from PyNEAT import Genome, NEAT
import copy
import matplotlib.pyplot as plt
import numpy as np
import random


myNEAT = NEAT()
myNEAT.SetInitialTopology(2, 4)
myNEAT.PrintSpecies()
print("\n")
i = 0
for i in range(0, 40):
    i += 1
    print("Geração " + str(i))
    myNEAT.RandomUpdate()
    members = myNEAT.GetAllMembers()
    for member in members:
        member.SetScore(random.random())
    myNEAT.Selection(10)
    myNEAT.PrintSpecies()

