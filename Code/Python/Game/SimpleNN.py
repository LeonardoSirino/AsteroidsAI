from AsterGameClasses import Game, GameSettings
import random
import numpy as np


class AGPlayer:
    Neurons = 20 + 1
    NumberInputs = 8 + 1
    NumberOutputs = 5
    Mw1 = 1 / 9
    Dw1 = Mw1 / 2
    Mw2 = 1 / (Neurons + 1)
    Dw2 = Mw2 / 2

    def __init__(self):
        self.name = "random"
        self.w1 = np.zeros((AGPlayer.Neurons - 1, AGPlayer.NumberInputs))
        self.w2 = np.zeros((AGPlayer.NumberOutputs, AGPlayer.Neurons))

    def RandomVariation(self):
        RV1 = - AGPlayer.Dw1 + 2 * AGPlayer.Dw1 * \
            np.random.random_sample(
                (AGPlayer.Neurons - 1, AGPlayer.NumberInputs))
        RV2 = - AGPlayer.Dw2 + 2 * AGPlayer.Dw2 * \
            np.random.random_sample((AGPlayer.NumberOutputs, AGPlayer.Neurons))
        return (RV1, RV2)

    def initializeWeights(self):
        rv = self.RandomVariation()
        self.w1 = AGPlayer.Mw1 + rv[0]
        self.w2 = AGPlayer.Mw2 + rv[1]

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
        return o2

    def ActivateFunction(self, a):
        o = []
        for value in a:
            if value > 0:
                o.append(value)
            else:
                o.append(0)

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

        return input

    def setScore(self, score):
        self.Score = score

    def setWeights(self, w1, w2):
        self.w1 = w1
        self.w2 = w2

    def GenChildren(self, size, alpha):
        children = []
        for i in range(0, size):
            rv = self.RandomVariation()
            child = AGPlayer()
            w1 = self.w1 + alpha * rv[0]
            w2 = self.w2 + alpha * rv[1]
            child.setWeights(w1, w2)
            children.append(child)
        return children


class Info:
    def __init__(self, i, max_i, gen):
        self.i = i
        self.max_i = max_i
        self.gen = gen


def Selection(players, size):
    sorted_players = sorted(players, key=lambda player: player.Score)
    print("Pior score: " + str(sorted_players[0].Score))
    print("Melhor score: " + str(sorted_players[-1].Score))
    alive_players = sorted_players[len(players) - size:]
    print(len(alive_players))
    return alive_players


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
    AsterGame.init_game()
    AsterGame.set_AG_info(str(Info.gen), str(Info.i) + "/" + str(Info.max_i))
    AsterGame.setPlayer(player)
    AsterGame.loopExternalUser()
    if AsterGame.abort:
        AsterGame.end()
        return [True, 0]
    else:
        FinalResult = AsterGame.reset()
        return [False, FinalResult]


Generations = 3
alpha = 0.9
for gen in range(1, Generations + 1):
    print("Iniciando geração: " + str(gen))
    i = 1
    for player in players:
        infoPlayer = Info(i, len(players), gen)
        result = main(player, infoPlayer)
        player.setScore(result[1])
        i += 1
        if result[0]:
            break
    alive_players = Selection(players, 3)
    players = []
    for player in alive_players:
        children = player.GenChildren(5, alpha)
        players += children

    alpha *= 0.9


AsterGame.end()
