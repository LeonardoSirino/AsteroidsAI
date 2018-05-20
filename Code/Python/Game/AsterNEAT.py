from PyNEAT import Genome, NEAT
import copy
import matplotlib.pyplot as plt
import numpy as np


player = Genome()
player.InitGenome(2, 3)
player.RandomNode()
for i in range(0, 10):
    player.RandomNode()

for i in range(0, 100):
    player.RandomConnection()

#player.GenomeRepresentation()

"""
copyPlayer = copy.deepcopy(player)
for i in range(0, 10):
    player.RandomNode()

player.RandomConnection()
copyPlayer.RandomNode()
copyPlayer.RandomConnection()

myNEAT = NEAT()
distance = myNEAT.CalcDistance(
    player.ReturnLinearizedGenome(), copyPlayer.ReturnLinearizedGenome())
print(distance)
"""


"""
print(player)

nodes = 5
for i in range(0, nodes):
    player.RandomNode()

connections = 5
for i in range(0, connections):
    player.RandomConnection()

print(player)
"""
range = 5
positive = np.linspace(-range, range, num = 50)
negative = np.linspace(range, -range, num = 50)
inputData = np.concatenate((positive, negative))
outputData = [[], [], []]

for data in inputData:
    player.InputData([data, 2 * data])
    player.FeedForward()
    result = player.ReturnOutput()
    i = 0
    for value in result:
        outputData[i].append(value)
        i += 1

    player.ClearNet()

plt.plot(inputData, outputData[0], inputData, outputData[1], inputData, outputData[2])
plt.show()