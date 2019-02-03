from PyNEAT import Genome, NEAT
import copy
import matplotlib.pyplot as plt
import numpy as np
import random


myNEAT = NEAT()
myNEAT.SetInitialTopology(1, 1)
myNEAT.PrintSpecies()
print("\n")
i = 0
for i in range(0, 200):
    i += 1
    print('\nGeração ' + str(i))
    myNEAT.RandomUpdate()
    members = myNEAT.GetAllMembers()
    for member in members:
        # member.SetScore(random.random())
        member.InputData([1])
        member.FeedForward()
        x = member.ReturnOutput()
        member.SetScore(1 / (0.1 + abs(0.75 - x[0])))
        print(x)
    myNEAT.Selection(10)
    myNEAT.PrintSpecies()

