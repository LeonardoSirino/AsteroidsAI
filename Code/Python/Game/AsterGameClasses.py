import pygame
import random
import math as m
import numpy as np
import time
import copy


class GameSettings:
    def __init__(self):
        self.drag = 0.99
        self.angDrag = 0.95
        self.SCREEN_WIDTH = 700
        self.SCREEN_HEIGHT = 500
        self.colors = {"black": (0, 0, 0), "white": (
            255, 255, 255), "red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0)}
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        self.FPS = 60
        self.MaxShipVel = 5
        self.MaxShipAngVel = 0.1
        self.GameOverMode = "NoGameOver"
        """Game over modes:
        NoGameOver - Apenas se desconta pontos do score
        GameOverUser - Game Over para o usuário, espera de alguns segundos
        GameOverExternal - Game Over para controle externo, sem espera
        """


class AsterManage:
    def __init__(self):
        self.__maxAsters = 20
        self.__minVel = 1
        self.__maxVel = 4
        self.maxSize = 30
        self.maxDivs = 2
        self.asters = []

    def clear(self):
        self.asters = []
        Aster.class_ID = 0

    def SetConfig(self, config):
        self.settings = config

    def AsterCreation(self, x_pos, y_pos, veloc, direction, size):
        aster = Aster(x_pos, y_pos, veloc, direction, size, self)
        self.asters.append(aster)

    def RandomCreation(self):
        if len(self.asters) < self.__maxAsters:
            vel = random.uniform(self.__minVel, self.__maxVel)
            direction = random.uniform(0, 2 * m.pi)
            size = random.randint(1, self.maxDivs)
            a = random.randint(1, 4)

            if a == 1:
                x_pos = -self.maxSize
                y_pos = random.randint(-self.maxSize,
                                       self.settings.SCREEN_HEIGHT + self.maxSize)
            elif a == 2:
                x_pos = self.settings.SCREEN_WIDTH + self.maxSize
                y_pos = random.randint(-self.maxSize,
                                       self.settings.SCREEN_HEIGHT + self.maxSize)
            elif a == 3:
                x_pos = random.randint(-self.maxSize,
                                       self.settings.SCREEN_WIDTH + self.maxSize)
                y_pos = -self.maxSize
            elif a == 4:
                x_pos = random.randint(-self.maxSize,
                                       self.settings.SCREEN_WIDTH + self.maxSize)
                y_pos = self.maxSize + self.settings.SCREEN_WIDTH
            else:
                pass

            NewAster = Aster(x_pos, y_pos, vel, direction,
                             size, self)
            self.asters.append(NewAster)

    def updateAll(self):
        for aster in self.asters:
            aster.update()

    def drawAll(self, screen):
        for aster in self.asters:
            aster.draw(screen)

    def DeleteAster(self, ID):
        i = 0
        for aster in self.asters:
            if aster.ID == ID:
                index = i
            i += 1

        del self.asters[index]

    def CheckForColision(self, Shoots):
        destroyed = False
        for aster in self.asters:
            for shoot in Shoots:
                distance = m.sqrt((shoot.x_pos - aster.x_pos)
                                  ** 2 + (shoot.y_pos - aster.y_pos)**2)
                if distance <= aster.GetSize():
                    shoot.delete()
                    aster.split()
                    destroyed = True
                    break

        return destroyed

    def CheckForShipColision(self, coords):
        colision = False
        for aster in self.asters:
            for coord in coords:
                distance = m.sqrt(
                    (aster.x_pos - coord[0])**2 + (aster.y_pos - coord[1])**2)
                if distance <= aster.GetSize():
                    colision = True
                    break

        return colision

    def RefreshAll(self):
        for aster in self.asters:
            aster.InTheWay = False

    def MarkInTarget(self, IDs):
        for aster in self.asters:
            for ID in IDs:
                if ID == aster.ID:
                    aster.InTheWay = True


class Aster:
    class_ID = 0

    def __init__(self, x_pos, y_pos, vel, direction, size, manager):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.vel = vel
        self.direction = direction
        self.size = size
        self.ID = self.class_ID
        self.manager = manager
        self.InTheWay = False

        Aster.class_ID += 1

    def update(self):
        self.x_pos += self.vel * m.sin(self.direction)
        self.y_pos += self.vel * m.cos(self.direction)

        Cond_a = self.x_pos < -2 * \
            self.manager.maxSize or self.x_pos > (
                self.manager.settings.SCREEN_WIDTH + 2 * self.manager.maxSize)
        Cond_b = self.y_pos < -2 * \
            self.manager.maxSize or self.y_pos > (
                self.manager.settings.SCREEN_HEIGHT + 2 * self.manager.maxSize)

        if Cond_a or Cond_b:
            self.manager.DeleteAster(ID=self.ID)

    def draw(self, screen):
        size = self.GetSize()
        if self.InTheWay:
            color = "green"
        else:
            color = "white"
        pygame.draw.circle(screen, self.manager.settings.colors.get(color), (int(self.x_pos),
                                                                             int(self.y_pos)), int(size))
        """
        print("Desenhado asteroide de ID " + str(self.ID) + " coordenadas: x = " +
              str(self.x_pos) + "; y = " + str(self.y_pos) + " -- tam: " + str(self.size))
        """

    def GetSize(self):
        size = self.manager.maxSize / 2**(self.manager.maxDivs - self.size)
        return size

    def delete(self):
        self.manager.DeleteAster(self.ID)

    def split(self):
        if self.size == 0:
            self.delete()
        else:
            self.manager.AsterCreation(
                self.x_pos, self.y_pos, self.vel, self.direction + m.radians(15), self.size - 1)
            self.manager.AsterCreation(
                self.x_pos, self.y_pos, self.vel, self.direction - m.radians(15), self.size - 1)
            self.delete()

    def ChangeToShipPersp(self, nave):
        self.old_x = self.x_pos
        self.old_y = self.y_pos
        x = self.x_pos - nave.x_pos
        y = self.y_pos - nave.y_pos
        xx = x * m.cos(-nave.angle) + y * m.sin(-nave.angle)
        yy = - x * m.sin(-nave.angle) + y * m.cos(-nave.angle)
        self.x_pos = xx
        self.y_pos = yy

    def ReturnPersp(self):
        self.x_pos = self.old_x
        self.y_pos = self.old_y


class ShootManage:
    def __init__(self):
        self.__minTimeShoots = 0.05
        self.ShootVeloc = 20
        self.shootSize = 4
        self.shoots = []
        self.lastTime = time.time() - self.__minTimeShoots

    def clear(self):
        self.shoots = []
        Shoot.class_ID = 0

    def SetConfig(self, config):
        self.settings = config

    def shoot(self, Nave):
        shooted = False
        CurrentTime = time.time()
        if (CurrentTime - self.lastTime) > self.__minTimeShoots:
            NewShoot = Shoot(Nave, self)
            self.shoots.append(NewShoot)
            self.lastTime = CurrentTime
            shooted = True

        return shooted

    def updateAll(self):
        for shoot in self.shoots:
            shoot.update()

    def drawAll(self, screen):
        for shoot in self.shoots:
            shoot.draw(screen)

    def deleteShoot(self, ID):
        i = 0
        for shoot in self.shoots:
            if shoot.ID == ID:
                index = i
            i += 1

        del self.shoots[index]

    def GetAllShoots(self):
        return self.shoots


class Shoot:

    class_ID = 0

    def __init__(self, Nave, manager):
        self.direction = Nave.angle + m.pi
        self.x_pos = Nave.x_pos
        self.y_pos = Nave.y_pos
        self.ID = self.class_ID
        self.manager = manager
        self.vel = self.manager.ShootVeloc

        Shoot.class_ID += 1

    def update(self):
        self.x_pos += self.vel * m.sin(self.direction)
        self.y_pos += self.vel * m.cos(self.direction)

        Cond_a = self.x_pos < -2 * \
            self.manager.shootSize or self.x_pos > (
                self.manager.settings.SCREEN_WIDTH + 2 * self.manager.shootSize)
        Cond_b = self.y_pos < -2 * \
            self.manager.shootSize or self.y_pos > (
                self.manager.settings.SCREEN_HEIGHT + 2 * self.manager.shootSize)

        if Cond_a or Cond_b:
            self.manager.deleteShoot(ID=self.ID)

    def draw(self, screen):
        size = self.manager.shootSize
        pygame.draw.circle(screen, self.manager.settings.colors.get("red"), (int(self.x_pos),
                                                                             int(self.y_pos)), int(size))

    def delete(self):
        self.manager.deleteShoot(self.ID)


class SpaceShip:
    """
    Classe para a espaço-nave
    """

    def __init__(self):
        self.x_vel = 0
        self.y_vel = 0
        self.veloc = 0
        self.ang_vel = 0
        self.angle = 0
        self.__side = 25
        self.__innerAngle = m.radians(15)
        self.__acel = 2
        self.__angAcel = 0.05

    def SetConfig(self, config):
        self.settings = config
        self.x_pos = self.settings.SCREEN_WIDTH / 2
        self.y_pos = self.settings.SCREEN_HEIGHT / 2
        self.__maxVel = self.settings.MaxShipVel
        self.__maxAngVel = self.settings.MaxShipAngVel

    def clear(self):
        self.x_pos = self.settings.SCREEN_WIDTH / 2
        self.y_pos = self.settings.SCREEN_HEIGHT / 2

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
        self.x_vel *= self.settings.drag
        self.y_vel *= self.settings.drag
        self.veloc *= self.settings.drag
        self.ang_vel *= self.settings.angDrag
        self.x_pos += self.x_vel
        self.x_pos = Limit(self.x_pos, 0, self.settings.SCREEN_WIDTH)
        self.y_pos += self.y_vel
        self.y_pos = Limit(self.y_pos, 0, self.settings.SCREEN_HEIGHT)
        self.angle += self.ang_vel
        if self.angle > 2 * m.pi:
            self.angle -= 2 * m.pi
        elif self.angle < - 2 * m.pi:
            self.angle += 2 * m.pi

    def draw(self, screen):
        pygame.draw.polygon(screen, self.settings.colors.get(
            "white"), self.GetCoords())

    def push(self):
        self.veloc += self.__acel
        self.veloc = Limit(self.veloc, -self.__maxVel, self.__maxVel)
        self.x_vel = -self.veloc * m.sin(self.angle)
        self.y_vel = -self.veloc * m.cos(self.angle)

    def breaking(self):
        self.veloc *= 0.8
        self.x_vel = -self.veloc * m.sin(self.angle)
        self.y_vel = -self.veloc * m.cos(self.angle)

    def DrawAuxiliaryLines(self, screen):
        lenght = 500
        n1_x = self.x_pos + lenght * m.sin(self.angle)
        n1_y = self.y_pos + lenght * m.cos(self.angle)
        n2_x = self.x_pos - lenght * m.sin(self.angle)
        n2_y = self.y_pos - lenght * m.cos(self.angle)
        t1_x = self.x_pos + lenght * m.sin(self.angle - m.pi / 2)
        t1_y = self.y_pos + lenght * m.cos(self.angle - m.pi / 2)
        t2_x = self.x_pos - lenght * m.sin(self.angle - m.pi / 2)
        t2_y = self.y_pos - lenght * m.cos(self.angle - m.pi / 2)

        pygame.draw.line(screen, (255, 255, 0), (n1_x, n1_y), (n2_x, n2_y))
        pygame.draw.line(screen, (255, 255, 0), (t1_x, t1_y), (t2_x, t2_y))


class FPS:
    def __init__(self, color):
        self.t1 = time.time()
        self.i = 0
        self.sumFPS = 0
        self.lastFPS = 0
        pygame.font.init()
        self.font = pygame.font.SysFont('Calibri', 20, bold=1)
        self.color = color

    def __call__(self, screen):
        t2 = time.time()

        try:
            FPS = 1 / (t2 - self.t1)
        except ZeroDivisionError:
            FPS = 0

        self.t1 = t2
        self.i += 1
        self.sumFPS += FPS

        text = self.font.render(
            str(round(self.lastFPS, 2)) + " FPS", False, self.color)
        screen.blit(text, (0, 0))

        if self.i == 60:
            self.lastFPS = self.sumFPS / self.i

            self.i = 0
            self.sumFPS = 0


class score:
    def __init__(self, color):
        self.TimeScore = 0.01
        self.ShootScore = -1
        self.DestroyScore = 5
        self.ShipColisionScore = -50
        self.value_to_show = 0
        self.value = 0
        self.i = 0
        pygame.font.init()
        self.font = pygame.font.SysFont('Calibri', 20, bold=1)
        self.color = color

    def clear(self):
        self.value = 0
        self.value_to_show = 0

    def __call__(self, screen):
        self.value += self.TimeScore
        self.i += 1

        text = self.font.render("SCORE: " +
                                str(round(self.value_to_show, 2)), False, self.color)
        screen.blit(text, (0, 30))

        if self.i == 6:
            self.i = 0
            self.value_to_show = self.value

    def shoot(self):
        self.value += self.ShootScore

    def destroy(self):
        self.value += self.DestroyScore

    def colision(self):
        self.value += self.ShipColisionScore


class NEAT_input:
    def __init__(self, settings):
        self.input = [0] * 8
        """Input:
        0 - Distância a frente
        1 - Distância atrás
        3 - Distância a direita
        4 - Distância a esquerda
        5 - Ângulo da nave
        6 - Velocidade da nave
        7 - Rotação da nave
        """
        self.settings = settings

    def calcInput(self, nave, asters):
        self.input[5] = nave.angle / (2 * m.pi)
        self.input[6] = nave.veloc / self.settings.MaxShipVel
        self.input[7] = nave.ang_vel / self.settings.MaxShipAngVel
        NormalizerLenght = m.sqrt(
            self.settings.SCREEN_HEIGHT**2 + self.settings.SCREEN_WIDTH**2)
        self.Asters = asters
        self.nave = nave
        IDs_inTheWay = []

        asters_posXline = []
        asters_negXline = []
        asters_posYline = []
        asters_negYline = []
        for aster in self.Asters:
            aster.ChangeToShipPersp(nave)
            size = aster.GetSize()
            x = aster.x_pos
            y = aster.y_pos
            if abs(x) < size and y > 0:
                asters_posYline.append(aster)
            if abs(x) < size and y <= 0:
                asters_negYline.append(aster)
            if abs(y) < size and x > 0:
                asters_posXline.append(aster)
            if abs(y) < size and x <= 0:
                asters_negXline.append(aster)
            aster.ReturnPersp()

        asters_lists = [asters_posYline, asters_negYline,
                        asters_posXline, asters_negXline]
        i = 0
        for asters in asters_lists:
            if len(asters) != 0:
                distances = []
                for aster in asters:
                    distance = m.sqrt((aster.x_pos - nave.x_pos)
                                      ** 2 + (aster.y_pos - nave.y_pos)**2)
                    distances.append(distance)

                index = np.argmin(distances)
                IDs_inTheWay.append(asters[index].ID)
                self.input[i] = np.min(distances) / NormalizerLenght
            else:
                self.input[i] = 1

            i += 1

        return (IDs_inTheWay, self.input)


def Limit(value, min, max):
    x = value
    if x < min:
        x = min
    elif x > max:
        x = max
    else:
        pass

    return x


class Game:
    def __init__(self):
        print("Iniciando ambiente")
        self.done = False
        self.GameOver = "NoGameOver"
        self.generation = ""
        self.specimen = ""
        self.abort = False
        pygame.font.init()
        self.font = pygame.font.SysFont('Calibri', 20, bold=1)

    def init_classes(self):
        self.settings = GameSettings()
        self.ManagerAsters = AsterManage()
        self.ManagerAsters.SetConfig(self.settings)
        self.ManagerShoots = ShootManage()
        self.ManagerShoots.SetConfig(self.settings)
        self.Nave = SpaceShip()
        self.Nave.SetConfig(self.settings)
        self.FPS = FPS(self.settings.colors.get("blue"))
        self.score = score(self.settings.colors.get("blue"))
        self.NEAT_input = NEAT_input(self.settings)

    def setConfig(self, config):
        self.settings = config

    def set_AG_info(self, gen, spec):
        self.generation = gen
        self.specimen = spec

    def init_game(self):
        pygame.init()
        self.score.clear()

        # Criação da tela
        size = [self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT]
        self.screen = pygame.display.set_mode(size)

        pygame.display.set_caption("Asteroids AI")

        from ctypes import windll
        SetWindowPos = windll.user32.SetWindowPos

        NOSIZE = 1
        NOMOVE = 2
        zorder = -1
        hwnd = pygame.display.get_wm_info()['window']
        SetWindowPos(hwnd, zorder, 0, 0, 0, 0, NOMOVE | NOSIZE)

        # Critério de parada
        self.done = False

        # Inicialização
        self.clock = pygame.time.Clock()

    def setPlayer(self, Player):
        self.player = Player
        self.player.init()

    def events(self):
        # Analisando os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

        # Analisando teclas pressionadas
        keys = np.array(pygame.key.get_pressed())
        PressedKeys = np.where(keys == 1)[0]
        # print(PressedKeys)
        for key in PressedKeys:
            if key == 119:
                self.Nave.Acelerate("ver", "-")
            elif key == 115:
                self.Nave.Acelerate("ver", "+")
            elif key == 97:
                self.Nave.Acelerate("hor", "-")
            elif key == 100:
                self.Nave.Acelerate("hor", "+")
            elif key == 275:
                self.Nave.Rotate("-")
            elif key == 276:
                self.Nave.Rotate("+")
            elif key == 273:
                shooted = self.ManagerShoots.shoot(self.Nave)
                if shooted:
                    self.score.shoot()
            elif key == 120:
                self.Nave.push()
            elif key == 122:
                self.Nave.breaking()

    def ExternalControl(self):
        input = self.player.move(self.lastOutput)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.abort = True
                    self.done = True
                    self.GameOver = "GameOverExternal"
                elif event.key == pygame.K_s:
                    self.settings.FPS = 60
                elif event.key == pygame.K_f:
                    self.settings.FPS = 2000

        if input[0] > 0.5:
            self.Nave.Rotate("-")
        if input[1] > 0.5:
            self.Nave.Rotate("+")
        if input[2] > 0.5:
            shooted = self.ManagerShoots.shoot(self.Nave)
            if shooted:
                self.score.shoot()
        if input[3] > 0.5:
            self.Nave.push()
        if input[4] > 0.5:
            self.Nave.breaking()

    def update(self):
        # Tratando colisões
        shoots = self.ManagerShoots.shoots
        destroyed = self.ManagerAsters.CheckForColision(shoots)
        if destroyed:
            self.score.destroy()
        colision = self.ManagerAsters.CheckForShipColision(
            self.Nave.GetCoords())
        if colision:
            if self.settings.GameOverMode == "NoGameOver":
                self.score.colision()
            else:
                self.GameOver = self.settings.GameOverMode

        self.Nave.update()
        self.ManagerShoots.updateAll()

        self.ManagerAsters.RandomCreation()
        self.ManagerAsters.updateAll()

    def generateOutput(self):

        output = self.NEAT_input.calcInput(
            self.Nave, self.ManagerAsters.asters)
        self.ManagerAsters.MarkInTarget(output[0])
        self.lastOutput = output[1]

    def draw(self):
        self.screen.fill(self.settings.colors.get("black"))
        self.ManagerAsters.drawAll(self.screen)
        self.Nave.draw(self.screen)
        # self.Nave.DrawAuxiliaryLines(self.screen)
        self.ManagerShoots.drawAll(self.screen)

        self.clock.tick(self.settings.FPS)
        self.FPS(self.screen)
        self.score(self.screen)

    def ShowInfo(self):
        text1 = self.font.render("Geração: " + self.generation, False, self.settings.colors.get("blue"))
        text2 = self.font.render("Ser: " + self.specimen, False, self.settings.colors.get("blue"))
        self.screen.blit(text1, (0, 60))
        self.screen.blit(text2, (0, 90))

    def loop(self):
        while not self.done:
            if self.GameOver == "GameOverUser":
                print("Game over do usuário")
                self.screen.fill(self.settings.colors.get("black"))
                text = self.settings.font.render(
                    "GAME OVER", False, self.settings.colors.get("white"))
                self.screen.blit(
                    text, (self.settings.SCREEN_WIDTH / 2, self.settings.SCREEN_HEIGHT / 2))
                pygame.display.flip()
                time.sleep(2)
                break

            elif self.GameOver == "GameOverExternal":
                print("Game over externo")
                self.screen.fill(self.settings.colors.get("black"))
                text = self.settings.font.render(
                    "GAME OVER", False, self.settings.colors.get("white"))
                self.screen.blit()
                break

            else:
                self.events()
                self.update()
                self.draw()
                pygame.display.flip()

    def loopExternalUser(self):
        while not self.done:
            if self.GameOver == "GameOverUser":
                self.screen.fill(self.settings.colors.get("black"))
                text = self.settings.font.render(
                    "GAME OVER", False, self.settings.colors.get("white"))
                self.screen.blit(
                    text, (self.settings.SCREEN_WIDTH / 2, self.settings.SCREEN_HEIGHT / 2))
                pygame.display.flip()
                time.sleep(2)
                break

            elif self.GameOver == "GameOverExternal":
                self.screen.fill(self.settings.colors.get("black"))
                text = self.settings.font.render(
                    "GAME OVER", False, self.settings.colors.get("white"))
                break

            else:
                self.ManagerAsters.RefreshAll()
                self.generateOutput()
                self.ExternalControl()
                self.update()
                self.draw()
                self.ShowInfo()
                # self.Nave.DrawAuxiliaryLines(self.screen)
                pygame.display.flip()

    def end(self):
        pygame.quit()

    def reset(self):
        FinalResult = self.score.value
        self.Nave.clear()
        self.ManagerAsters.clear()
        self.ManagerShoots.clear()
        self.score.clear()
        self.GameOver = "NoGameOver"
        self.done = False
        return FinalResult
