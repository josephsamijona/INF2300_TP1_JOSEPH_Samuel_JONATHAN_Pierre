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

        # Define game variables
        self.scroll = 0
        self.scroll_direction = 1  # 1 for right, -1 for left
        self.scroll_speed = 2  # Speed of the automatic scrolling
        self.change_direction_time = 5  # Time in seconds to change direction
        self.last_direction_change = time.time()  # Time of the last direction change

    def draw_bg(self):
        for x in range(5):
            speed = 1
            for i in self.bg_images:
                self.screen.blit(i, ((x * self.bg_width) - self.scroll * speed, 0))
                speed += 0.2

    def draw_ground(self):
        for x in range(15):
            self.screen.blit(self.ground_image, ((x * self.ground_width) - self.scroll * 2.5, self.SCREEN_HEIGHT - self.ground_height))

    def update_scroll(self):
        # Update scroll position
        self.scroll += self.scroll_direction * self.scroll_speed

        # Change direction based on the timer
        if time.time() - self.last_direction_change > self.change_direction_time:
            self.scroll_direction *= -1
            self.last_direction_change = time.time()

    def draw(self):
        self.draw_bg()
        self.draw_ground()
        self.update_scroll()
