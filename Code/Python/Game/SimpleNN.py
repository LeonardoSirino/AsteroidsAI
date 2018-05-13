from AsterGameClasses import Game, GameSettings
import random
import numpy as np
import matplotlib.pyplot as plt
from DynamicGraphs import Chart

progressChart = plt.subplots()
plt.xlabel("Gerações")
plt.ylabel("Melhor Score")
plt.title("NN for Asteroids Game")

Progress = Chart()
Progress.setPlot(progressChart)


class AGPlayer:
    ID = 0
    NeuronsHL1 = 10 + 1
    NeuronsHL2 = 10 + 1
    NumberInputs = 13 + 1
    NumberOutputs = 5
    Mw1 = 1 / 9
    Dw1 = Mw1 / 1
    Mw2 = 1 / (NeuronsHL1 + 1)
    Dw2 = Mw2 / 1
    Mw3 = 1 / (NeuronsHL2 + 1)
    Dw3 = Mw3 / 1

    def __init__(self):
        self.name = "random"
        self.w1 = np.zeros((AGPlayer.NeuronsHL1 - 1, AGPlayer.NumberInputs))
        self.w2 = np.zeros((AGPlayer.NeuronsHL2 - 1, AGPlayer.NeuronsHL1))
        self.w3 = np.zeros((AGPlayer.NumberOutputs, AGPlayer.NeuronsHL2))
        self.ID = AGPlayer.ID
        AGPlayer.ID += 1

    def RandomVariation(self):
        RV1 = - AGPlayer.Dw1 + 2 * AGPlayer.Dw1 * \
            np.random.random_sample(
                (AGPlayer.NeuronsHL1 - 1, AGPlayer.NumberInputs))
        RV2 = - AGPlayer.Dw2 + 2 * AGPlayer.Dw2 * \
            np.random.random_sample(
                (AGPlayer.NeuronsHL2 - 1, AGPlayer.NeuronsHL1))
        RV3 = - AGPlayer.Dw3 + 2 * AGPlayer.Dw3 * \
            np.random.random_sample(
                (AGPlayer.NumberOutputs, AGPlayer.NeuronsHL2))
        return (RV1, RV2, RV3)

    def MutatedVariation(self, prob):
        Seed = np.random.random_sample(
            (AGPlayer.NeuronsHL1 - 1, AGPlayer.NumberInputs))
        Mutations = []
        for line in Seed:
            MutatedLine = []
            for value in line:
                if value > prob:
                    MutatedLine.append(0)
                else:
                    MutatedLine.append(value)
            Mutations.append(MutatedLine)

        RV1 = (-1)**random.randint(0, 1) * AGPlayer.Dw1 * np.array(Mutations)

        Seed = np.random.random_sample(
            (AGPlayer.NeuronsHL2 - 1, AGPlayer.NeuronsHL1))
        Mutations = []
        for line in Seed:
            MutatedLine = []
            for value in line:
                if value > prob:
                    MutatedLine.append(0)
                else:
                    MutatedLine.append(value)
            Mutations.append(MutatedLine)

        RV2 = (-1)**random.randint(0, 1) * AGPlayer.Dw2 * np.array(Mutations)

        Seed = np.random.random_sample(
            (AGPlayer.NumberOutputs, AGPlayer.NeuronsHL2))
        Mutations = []
        for line in Seed:
            MutatedLine = []
            for value in line:
                if value > prob:
                    MutatedLine.append(0)
                else:
                    MutatedLine.append(value)
            Mutations.append(MutatedLine)

        RV3 = (-1)**random.randint(0, 1) * AGPlayer.Dw3 * np.array(Mutations)

        return (RV1, RV2, RV3)

    def initializeWeights(self):
        rv = self.RandomVariation()
        self.w1 = rv[0]
        self.w2 = rv[1]
        self.w3 = rv[2]

    def init(self):
        import random

    def CalcResult(self, NN_input):
        input = np.array(NN_input + [1])
        input = [input]
        input = np.transpose(input)
        a1 = np.matmul(self.w1, input)
        o1 = self.ActivateFunction(a1)
        o1.append(1)
        a2 = np.matmul(self.w2, o1)
        o2 = self.ActivateFunction(a2)
        o2.append(1)
        a3 = np.matmul(self.w3, o2)
        o3 = self.ActivateFunction(a3)
        return o3

    def ActivateFunction(self, a):
        o = []
        for value in a:
            sigmoid = 1 / (1 + np.exp(-value))
            o.append(sigmoid)

        return o

    def move(self, output):
        """Move:
        0 - Rotate -
        1 - Rotate +
        2 - Shoot
        3 - Push
        4 - Break
        """
        input = self.CalcResult(output)
        # print(input)

        return input

    def setScore(self, score):
        self.Score = score

    def setWeights(self, w1, w2, w3):
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3

    def GenChildren(self, size, alpha):
        children = []
        for i in range(0, size):
            rv = self.RandomVariation()
            child = AGPlayer()
            w1 = self.w1 + alpha * rv[0]
            w2 = self.w2 + alpha * rv[1]
            w3 = self.w3 + alpha * rv[2]
            child.setWeights(w1, w2, w3)
            children.append(child)
        return children

    def Mutate(self, prob):
        if random.random() < prob:
            MV = self.MutatedVariation(prob)
            mutation = AGPlayer()
            w1 = self.w1 + alpha * MV[0]
            w2 = self.w2 + alpha * MV[1]
            w3 = self.w3 + alpha * MV[2]
            mutation.setWeights(w1, w2, w3)
            return [True, mutation]
        else:
            return [False, None]


class Info:
    def __init__(self, i, max_i, gen, tries):
        self.i = i
        self.max_i = max_i
        self.gen = gen
        self.tries = tries


def Selection(players, size):
    sorted_players = sorted(players, key=lambda player: player.Score)
    print("Pior player -- " + PlayerLog(sorted_players[0]))
    print("Melhor player -- " + PlayerLog(sorted_players[-1]))
    alive_players = sorted_players[len(players) - size:]
    return alive_players


def PlayerLog(player):
    score = round(player.Score, 2)
    W1m = round(np.mean(player.w1), 2)
    W1max = round(np.max(player.w1), 2)
    W1min = round(np.min(player.w1), 2)
    W2m = round(np.mean(player.w2), 2)
    W2max = round(np.max(player.w2), 2)
    W2min = round(np.min(player.w2), 2)
    W3m = round(np.mean(player.w3), 2)
    W3max = round(np.max(player.w3), 2)
    W3min = round(np.min(player.w3), 2)
    log = "ID " + str(player.ID) + "  Score: " + str(score) + "  W1m: " + str(W1m) + "  W2m: " + str(W2m) + "  W3m: " + str(W3m) + "  W1max: " + str(W1max) + "  W2max: " + str(W2max) + "  W3max: " + str(W3max) + \
        "  W1min: " + str(W1min) + "  W2min: " + \
        str(W2min) + "  W3min: " + str(W3min)
    return log


config = GameSettings()
config.GameOverMode = "GameOverExternal"
config.FPS = 60
player = AGPlayer()
player.initializeWeights()
players = player.GenChildren(5, 0.8)

AsterGame = Game()
AsterGame.init_classes()
AsterGame.setConfig(config)


def main(player, Info):
    results = []
    for i in range(0, Info.tries):
        AsterGame.init_game()
        AsterGame.set_AG_info(str(Info.gen), str(
            Info.i) + "/" + str(Info.max_i), str(i + 1) + "/" + str(Info.tries))
        AsterGame.setPlayer(player)
        AsterGame.loopExternalUser()
        if AsterGame.abort:
            AsterGame.end()
            return [True, 0]
        else:
            results.append(AsterGame.reset())

    FinalResult = np.mean(results)
    return [False, FinalResult]


Generations = 5000
tries = 3
alpha = 1

file = open("data.txt", mode="w")
for gen in range(1, Generations + 1):
    print("Iniciando geração: " + str(gen))
    i = 1
    for player in players:
        infoPlayer = Info(i, len(players), gen, tries)
        result = main(player, infoPlayer)
        player.setScore(result[1])
        i += 1
        if result[0]:
            break
    alive_players = Selection(players, 3)
    file.write("Melhor elemento da geração " + str(gen) + "\n--- W1\n")
    file.write(np.array_str(alive_players[-1].w1))
    file.write("\n\n --- W2\n")
    file.write(np.array_str(alive_players[-1].w2))
    file.write("\n\n --- W3\n")
    file.write(np.array_str(alive_players[-1].w3))
    file.write("\n\n\n")
    players = alive_players[:]
    for player in alive_players:
        children = player.GenChildren(3, alpha)
        players += children
        mutation = player.Mutate(0.8)
        if mutation[0]:
            players.append(mutation[1])

    base_player = AGPlayer()
    base_player.initializeWeights()
    mutated = base_player.GenChildren(2, 0.8)
    players += mutated

    alpha *= 0.98

    Progress.appendData(alive_players[-1].Score)
    Progress.plot()

file.close()
AsterGame.end()
