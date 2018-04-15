import pygame
import random
import math as m
import numpy as np

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BALL_SIZE = 25

drag = 0.9
AngDrag = 0.9


class Ball:
    """
    Class to keep track of a ball's location and vector.
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.float_x = 0
        self.float_y = 0
        self.change_x = 0
        self.change_y = 0


class SpaceShip:
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


def make_ball():
    """
    Function to make a new, random ball.
    """
    ball = Ball()
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
    ball.x = random.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)
    ball.float_x = float(ball.x)
    ball.y = random.randrange(BALL_SIZE, SCREEN_HEIGHT - BALL_SIZE)
    ball.float_y = float(ball.y)

    # Speed and direction of rectangle
    ball.change_x = random.randrange(-10, 10)
    ball.change_y = random.randrange(-10, 10)

    return ball


def main():
    """
    This is our main program.
    """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Bouncing Balls")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    ball_list = []

    Nave = SpaceShip()

    ball = make_ball()
    ball_list.append(ball)

    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # Space bar! Spawn a new ball.
                if event.key == pygame.K_SPACE:
                    ball = make_ball()
                    ball_list.append(ball)

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

        # --- Logic
        for ball in ball_list:
            # Arrasto
            ball.change_x *= drag
            ball.change_y *= drag

            # Move the ball's center
            ball.float_x += ball.change_x
            ball.float_y += ball.change_y

            ball.x = int(ball.float_x)
            ball.y = int(ball.float_y)

            # Bounce the ball if needed
            if ball.y > SCREEN_HEIGHT - BALL_SIZE or ball.y < BALL_SIZE:
                ball.change_y *= -1
            if ball.x > SCREEN_WIDTH - BALL_SIZE or ball.x < BALL_SIZE:
                ball.change_x *= -1

        # --- Drawing
        # Set the screen background
        screen.fill(BLACK)

        # Draw the balls
        for ball in ball_list:
            pygame.draw.circle(screen, WHITE, [ball.x, ball.y], BALL_SIZE)

        # Desenha a espaço-nave
        Nave.update()
        pygame.draw.polygon(screen, WHITE, Nave.GetCoords())

        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Close everything down
    pygame.quit()


if __name__ == "__main__":
    main()
