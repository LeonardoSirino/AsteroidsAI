from AsterGameClasses import Game

AsterGame = Game()
AsterGame.init_classes()


def main():
    AsterGame.init_game()
    AsterGame.loop()
    AsterGame.end()


if __name__ == "__main__":
    main()
