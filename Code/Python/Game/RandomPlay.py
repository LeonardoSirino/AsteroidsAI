from AsterGameClasses import Game
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

        input = [0] * 5
        k = 0
        for i in input:
            input[k] = random.random()
            k += 1

        return input


player = RandomPlayer()

AsterGame = Game()
AsterGame.init_classes()


def main():
    AsterGame.init_game()
    AsterGame.setPlayer(player)
    AsterGame.loopExternalUser()
    AsterGame.end()


if __name__ == "__main__":
    main()
