from AsterGameClasses import Game, GameSettings
import random


class RandomPlayer:
    def __init__(self):
        self.name = "random"

    def init(self):
        import random

    def move(self, output):
        """Move:
        0 - Rotate -
        1 - Rotate +
        2 - Shoot
        3 - Push
        4 - Break
        """
        # print(output)
        input = [0] * 5
        k = 0
        for i in input:
            input[k] = random.random()
            k += 1

        return input


config = GameSettings()
config.GameOverMode = "GameOverExternal"
config.FPS = 60
player = RandomPlayer()
AsterGame = Game()
AsterGame.init_classes()
AsterGame.setConfig(config)

for i in range(1, 10):
    def main():
        AsterGame.init_game()
        AsterGame.setPlayer(player)
        AsterGame.loopExternalUser()
        AsterGame.reset()

    if __name__ == "__main__":
        main()

AsterGame.end()
