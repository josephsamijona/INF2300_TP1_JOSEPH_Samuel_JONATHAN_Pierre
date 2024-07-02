import pygame as pg
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
from src.navigation import return_to_menu

vec2, vec3 = pg.math.Vector2, pg.math.Vector3

RES = WIDTH, HEIGHT = 1200, 800
NUM_STARS = 1500
CENTER = vec2(WIDTH // 2, HEIGHT // 2)
COLORS = 'red green blue orange purple cyan'.split()
Z_DISTANCE = 40
ALPHA = 120

class Star:
    def __init__(self, screen):
        self.screen = screen
        self.pos3d = self.get_pos3d()
        self.vel = random.uniform(0.05, 0.25)
        self.color = random.choice(COLORS)
        self.screen_pos = vec2(0, 0)
        self.size = 10

    def get_pos3d(self, scale_pos=35):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // scale_pos, HEIGHT) * scale_pos
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        return vec3(x, y, Z_DISTANCE)

    def update(self):
        self.pos3d.z -= self.vel
        self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (Z_DISTANCE - self.pos3d.z) / (0.2 * self.pos3d.z)
        self.pos3d.xy = self.pos3d.xy.rotate(0.2)

    def draw(self):
        s = self.size
        if (-s < self.screen_pos.x < WIDTH + s) and (-s < self.screen_pos.y < HEIGHT + s):
            pg.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))

class Starfield:
    def __init__(self, screen):
        self.stars = [Star(screen) for _ in range(NUM_STARS)]

    def run(self):
        for star in self.stars:
            star.update()
        self.stars.sort(key=lambda star: star.pos3d.z, reverse=True)
        for star in self.stars:
            star.draw()

class Cube:
    def __init__(self):
        self.angle = 0

    def draw(self):
        glBegin(GL_QUADS)
        # Front face
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-1.0, -1.0, 1.0)
        glVertex3f(1.0, -1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        # Back face
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(1.0, -1.0, -1.0)
        # Top face
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)
        glVertex3f(1.0, 1.0, -1.0)
        # Bottom face
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(1.0, -1.0, -1.0)
        glVertex3f(1.0, -1.0, 1.0)
        glVertex3f(-1.0, -1.0, 1.0)
        # Right face
        glColor3f(0.0, 1.0, 1.0)
        glVertex3f(1.0, -1.0, -1.0)
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(1.0, 1.0, 1.0)
        glVertex3f(1.0, -1.0, 1.0)
        # Left face
        glColor3f(1.0, 0.0, 1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glEnd()

    def update(self):
        self.angle += 1
        glRotatef(self.angle, 3, 1, 1)

class GameCube3D:
    def __init__(self, root_dir):
        pg.init()
        pg.display.set_mode(RES, pg.OPENGL | pg.DOUBLEBUF)
        self.screen = pg.display.get_surface()
        glEnable(GL_DEPTH_TEST)
        self.clock = pg.time.Clock()
        self.starfield = Starfield(self.screen)
        self.cube = Cube()
        self.running = True

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.running = False
                        return_to_menu(self.screen, os.path.dirname(os.path.abspath(__file__)))

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
            glTranslatef(0.0, 0.0, -5)

            self.cube.update()
            self.cube.draw()

            self.screen.fill((0, 0, 0, 0))
            self.starfield.run()
            pg.display.flip()

            self.clock.tick(60)

        pg.quit()

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.abspath(__file__))
    game = GameCube3D(root_dir)
    game.run()
