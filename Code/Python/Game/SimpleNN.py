from AsterGameClasses import Game, GameSettings
import random
import numpy as np
import matplotlib.pyplot as plt

plt.ion()


class DynamicUpdate():
    def on_launch(self):
        # Set up plot
        self.figure, self.ax = plt.subplots()
        self.lines, = self.ax.plot([], [], '-')
        # Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        #self.ax.set_xlim(self.min_x, self.max_x)
        plt.xlabel("Gerações")
        plt.ylabel("Melhor Score")
        plt.title("NN for Asteroids Game")

    def on_running(self, xdata, ydata):
        # Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)
        # Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        # We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()


class AGPlayer:
    ID = 0
    Neurons = 20 + 1
    NumberInputs = 10 + 1
    NumberOutputs = 5
    Mw1 = 1 / 9
    Dw1 = Mw1 / 1
    Mw2 = 1 / (Neurons + 1)
    Dw2 = Mw2 / 1

    def __init__(self):
        self.name = "random"
        self.w1 = np.zeros((AGPlayer.Neurons - 1, AGPlayer.NumberInputs))
        self.w2 = np.zeros((AGPlayer.NumberOutputs, AGPlayer.Neurons))
        self.ID = AGPlayer.ID
        AGPlayer.ID += 1

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
        # print(input)

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
    W2m = round(np.mean(player.w2), 2)
    W2max = round(np.max(player.w2), 2)
    log = "ID " + str(player.ID) + "  Score: " + str(score) + "  W1m: " + str(W1m) + "  W2m: " + \
        str(W2m) + "  W1max: " + str(W1max) + "  W2max: " + str(W2max)
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

ScoreGraph = DynamicUpdate()
ScoreGraph.on_launch()


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

    FinalResult = np.min(results)
    return [False, FinalResult]


Generations = 5000
tries = 5
alpha = 0.90

gens = []
scores = []

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
    file.write("\n\n\n")
    players = alive_players[:]
    for player in alive_players:
        children = player.GenChildren(5, alpha)
        players += children

    base_player = AGPlayer()
    base_player.initializeWeights()
    mutated = base_player.GenChildren(3, 0.8)
    players += mutated

    alpha *= 0.95

    gens.append(gen)
    scores.append(alive_players[-1].Score)

    ScoreGraph.on_running(gens, scores)

file.close()
AsterGame.end()
