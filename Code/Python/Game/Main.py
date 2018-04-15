import pygame
import random
import math as m
import numpy as np

# Definição de algumas constantes
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500


class GameSettings:
    def __init__(self):
        self.drag = 0.9
        self.angDrag = 0.9


game = GameSettings


class SpaceShip:
    """
    Classe para a espaço-nave
    """

    def __init__(self):
        self.x_pos = SCREEN_WIDTH / 2
        self.y_pos = SCREEN_HEIGHT / 2
        self.x_vel = 0
        self.y_vel = 0
        self.ang_vel = 0
        self.angle = 0
        self.__side = 25
        self.__innerAngle = m.radians(15)
        self.__acel = 2
        self.__maxVel = 5
        self.__angAcel = 0.05
        self.__maxAngVel = 0.1

    def GetCoords(self):
        x_Coords = [0, -self.__side *
                    m.sin(self.__innerAngle), self.__side * m.sin(self.__innerAngle)]
        y_Coords = [0, self.__side *
                    m.cos(self.__innerAngle), self.__side * m.cos(self.__innerAngle)]
        Coords = []
        for x, y in zip(x_Coords, y_Coords):
            xx = x * m.cos(self.angle) + y * m.sin(self.angle) + self.x_pos
            yy = - x * m.sin(self.angle) + y * m.cos(self.angle) + self.y_pos
            Coords.append((xx, yy))

        return Coords

    def Acelerate(self, direction, sign):
        if direction == "hor":
            if sign == "+":
                self.x_vel += self.__acel
            if sign == "-":
                self.x_vel -= self.__acel
        elif direction == "ver":
            if sign == "+":
                self.y_vel += self.__acel
            if sign == "-":
                self.y_vel -= self.__acel
        else:
            print("Comando errado")

        self.x_vel = Limit(self.x_vel, -self.__maxVel, self.__maxVel)
        self.y_vel = Limit(self.y_vel, -self.__maxVel, self.__maxVel)

    def Rotate(self, sign):
        if sign == "+":
            self.ang_vel += self.__angAcel
        elif sign == "-":
            self.ang_vel -= self.__angAcel
        else:
            print("Comando errado")

        self.ang_vel = Limit(self.ang_vel, -self.__maxAngVel, self.__maxAngVel)

    def update(self):
        self.x_vel *= drag
        self.y_vel *= drag
        self.ang_vel *= drag
        self.x_pos += self.x_vel
        self.x_pos = Limit(self.x_pos, 0, SCREEN_WIDTH)
        self.y_pos += self.y_vel
        self.y_pos = Limit(self.y_pos, 0, SCREEN_HEIGHT)
        self.angle += self.ang_vel


def Limit(value, min, max):
    x = value
    if x < min:
        x = min
    elif x > max:
        x = max
    else:
        pass

    return x


def main():
    pygame.init()

    # Criação da tela
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Asteroids AI")

    # Critério de parada
    done = False

    # Inicialização
    clock = pygame.time.Clock()

    Nave = SpaceShip()

    # -------- Loop principal -----------
    while not done:

        # Analisando teclas pressionadas
        keys = np.array(pygame.key.get_pressed())
        PressedKeys = np.where(keys == 1)[0]
        for key in PressedKeys:
            if key == 119:
                Nave.Acelerate("ver", "-")
            elif key == 115:
                Nave.Acelerate("ver", "+")
            elif key == 97:
                Nave.Acelerate("hor", "-")
            elif key == 100:
                Nave.Acelerate("hor", "+")
            elif key == 275:
                Nave.Rotate("-")
            elif key == 276:
                Nave.Rotate("+")

        # --- Desenhando
        screen.fill(BLACK)

        # Desenha a espaço-nave
        Nave.update()
        pygame.draw.polygon(screen, WHITE, Nave.GetCoords())

        # Definindo FPS
        clock.tick(60)

        # Atualizando a tela
        pygame.display.flip()

    # Encerra tudo
    pygame.quit()


if __name__ == "__main__":
    main()