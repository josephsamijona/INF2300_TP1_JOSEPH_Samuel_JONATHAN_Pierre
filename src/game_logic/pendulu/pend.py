import pygame
import math
import random
from src.navigation import return_to_menu  # Assurez-vous d'importer la fonction

class DoublePendulum:
    def __init__(self, L1, L2, M1, M2, G, theta1, theta2, omega1, omega2):
        self.L1 = L1
        self.L2 = L2
        self.M1 = M1
        self.M2 = M2
        self.G = G
        self.theta1 = theta1
        self.theta2 = theta2
        self.omega1 = omega1
        self.omega2 = omega2
        self.trace = []

    def update(self, dt):
        num1 = -self.G * (2 * self.M1 + self.M2) * math.sin(self.theta1)
        num2 = -self.M2 * self.G * math.sin(self.theta1 - 2 * self.theta2)
        num3 = -2 * math.sin(self.theta1 - self.theta2) * self.M2
        num4 = self.omega2 ** 2 * self.L2 + self.omega1 ** 2 * self.L1 * math.cos(self.theta1 - self.theta2)
        denom = self.L1 * (2 * self.M1 + self.M2 - self.M2 * math.cos(2 * self.theta1 - 2 * self.theta2))
        a1 = (num1 + num2 + num3 * num4) / denom

        num1 = 2 * math.sin(self.theta1 - self.theta2)
        num2 = self.omega1 ** 2 * self.L1 * (self.M1 + self.M2)
        num3 = self.G * (self.M1 + self.M2) * math.cos(self.theta1)
        num4 = self.omega2 ** 2 * self.L2 * self.M2 * math.cos(self.theta1 - self.theta2)
        denom = self.L2 * (2 * self.M1 + self.M2 - self.M2 * math.cos(2 * self.theta1 - 2 * self.theta2))
        a2 = num1 * (num2 + num3 + num4) / denom

        self.omega1 += a1 * dt
        self.omega2 += a2 * dt
        self.theta1 += self.omega1 * dt
        self.theta2 += self.omega2 * dt

        self.trace.append(self.get_positions()[1])
        if len(self.trace) > 500:  # Limite la longueur de la trace
            self.trace.pop(0)

    def get_positions(self):
        x1 = 400 + self.L1 * math.sin(self.theta1)
        y1 = 300 + self.L1 * math.cos(self.theta1)
        x2 = x1 + self.L2 * math.sin(self.theta2)
        y2 = y1 + self.L2 * math.cos(self.theta2)
        return (x1, y1), (x2, y2)

    def draw(self, screen):
        (x1, y1), (x2, y2) = self.get_positions()
        for pos in self.trace:
            pygame.draw.circle(screen, (0, 0, 255), (int(pos[0]), int(pos[1])), 2)
        pygame.draw.line(screen, (0, 0, 0), (400, 300), (x1, y1), 2)
        pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 2)
        pygame.draw.circle(screen, (0, 0, 0), (int(x1), int(y1)), 10)
        pygame.draw.circle(screen, (0, 0, 0), (int(x2), int(y2)), 10)

class Particle:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color

    def update(self, width, height):
        self.x += self.vx
        self.y += self.vy

        if self.x <= 0 or self.x >= width:
            self.vx = -self.vx
        if self.y <= 0 or self.y >= height:
            self.vy = -self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

class GamePendulum:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.running = True

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Double Pendulum with Particles")
        clock = pygame.time.Clock()

        pendulum = DoublePendulum(
            L1=200, L2=200, M1=10, M2=10, G=9.81,
            theta1=math.pi / 2, theta2=math.pi / 2,
            omega1=0.0, omega2=0.0
        )

        particles = [Particle(random.randint(0, 800), random.randint(0, 600), random.uniform(-2, 2), random.uniform(-2, 2), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))) for _ in range(20)]

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.running = False
                        return_to_menu(screen, self.root_dir)

            screen.fill((255, 255, 255))

            pendulum.update(0.05)
            pendulum.draw(screen)

            for particle in particles:
                particle.update(1200, 500)
                particle.draw(screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

