import pygame
import numpy as np
from src.navigation import return_to_menu

class GameLife:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.running = True

    def random_grid(self, cols, rows):
        return np.random.choice([0, 1], size=(cols, rows), p=[0.8, 0.2])

    def update_grid(self, grid, cols, rows):
        new_grid = grid.copy()
        for x in range(cols):
            for y in range(rows):
                neighbors = (
                    grid[(x-1) % cols, (y-1) % rows] + grid[(x) % cols, (y-1) % rows] + grid[(x+1) % cols, (y-1) % rows] +
                    grid[(x-1) % cols, (y) % rows] + grid[(x+1) % cols, (y) % rows] +
                    grid[(x-1) % cols, (y+1) % rows] + grid[(x) % cols, (y+1) % rows] + grid[(x+1) % cols, (y+1) % rows]
                )
                if grid[x, y] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[x, y] = 0
                else:
                    if neighbors == 3:
                        new_grid[x, y] = 1
        return new_grid

    def run(self):
        pygame.init()
        width, height = 1200, 800
        cell_size = 10
        cols, rows = width // cell_size, height // cell_size

        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Jeu de la Vie de Conway")
        clock = pygame.time.Clock()

        grid = np.zeros((cols, rows), dtype=int)
        grid = self.random_grid(cols, rows)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Retour au menu principal avec la touche p
                        return_to_menu(screen, self.root_dir)
                        return

            screen.fill((0, 0, 0))

            for x in range(cols):
                for y in range(rows):
                    if grid[x, y] == 1:
                        pygame.draw.rect(screen, (255, 255, 255), (x * cell_size, y * cell_size, cell_size - 1, cell_size - 1))

            pygame.display.flip()
            grid = self.update_grid(grid, cols, rows)
            clock.tick(10)

        pygame.quit()
