from PyNEAT import Genome, NEAT
import copy


player = Genome()
player.InitGenome(2, 3)
player.RandomNode()
for i in range(0, 5):
    player.RandomNode()

for i in range(0, 10):
    player.RandomConnection()

player.GenomeRepresentation()

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
"""
for i in range(0, 10):
    player.InputData([2.5, 3.6])
    player.FeedForward()
    result = player.ReturnOutput()
    print(result)

    player.ClearNet()
"""