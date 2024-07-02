import pygame
import time

class Parallax:
    def __init__(self, screen, screen_width, screen_height, bg_images, ground_image, fps=60):
        self.screen = screen
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.bg_images = bg_images
        self.ground_image = ground_image
        self.ground_width = ground_image.get_width()
        self.ground_height = ground_image.get_height()
        self.bg_width = bg_images[0].get_width()

        # Définir les variables du jeu
        self.scroll = 0
        self.scroll_direction = 1  # 1 pour droite, -1 pour gauche
        self.scroll_speed = 2  # Vitesse du défilement automatique
        self.change_direction_time = 5  # Temps en secondes pour changer de direction
        self.last_direction_change = time.time()  # Temps du dernier changement de direction

    def draw_bg(self):
        # Dessiner l'arrière-plan
        for x in range(5):
            speed = 1
            for i in self.bg_images:
                self.screen.blit(i, ((x * self.bg_width) - self.scroll * speed, 0))
                speed += 0.2

    def draw_ground(self):
        # Dessiner le sol
        for x in range(15):
            self.screen.blit(self.ground_image, ((x * self.ground_width) - self.scroll * 2.5, self.SCREEN_HEIGHT - self.ground_height))

    def update_scroll(self):
        # Mettre à jour la position du défilement
        self.scroll += self.scroll_direction * self.scroll_speed

        # Changer de direction en fonction du timer
        if time.time() - self.last_direction_change > self.change_direction_time:
            self.scroll_direction *= -1
            self.last_direction_change = time.time()

    def draw(self):
        # Dessiner l'arrière-plan et le sol, puis mettre à jour le défilement
        self.draw_bg()
        self.draw_ground()
        self.update_scroll()
