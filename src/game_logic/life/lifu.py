import pygame
import numpy as np

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
                # Compter les voisins vivants
                neighbors = (
                    grid[(x-1) % cols, (y-1) % rows] + grid[(x) % cols, (y-1) % rows] + grid[(x+1) % cols, (y-1) % rows] +
                    grid[(x-1) % cols, (y) % rows] + grid[(x+1) % cols, (y) % rows] +
                    grid[(x-1) % cols, (y+1) % rows] + grid[(x) % cols, (y+1) % rows] + grid[(x+1) % cols, (y+1) % rows]
                )

                # Appliquer les règles du jeu de la vie
                if grid[x, y] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[x, y] = 0
                else:
                    if neighbors == 3:
                        new_grid[x, y] = 1
        return new_grid

    def run(self):
        pygame.init()
        width, height = 800, 600
        cell_size = 10
        cols, rows = width // cell_size, height // cell_size

        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Jeu de la Vie de Conway")
        clock = pygame.time.Clock()

        # Initialisation de la grille
        grid = np.zeros((cols, rows), dtype=int)
        grid = self.random_grid(cols, rows)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            screen.fill((0, 0, 0))

            for x in range(cols):
                for y in range(rows):
                    if grid[x, y] == 1:
                        pygame.draw.rect(screen, (255, 255, 255), (x * cell_size, y * cell_size, cell_size - 1, cell_size - 1))

            pygame.display.flip()
            grid = self.update_grid(grid, cols, rows)
            clock.tick(10)

        pygame.quit()
