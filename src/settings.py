import pygame
import os
from src.controls_settings import show_controls_settings

class Button:
    def __init__(self, text, font, color, x, y, width, height):
        self.text = text
        self.font = font
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False

    def draw(self, screen):
        if self.hovered:
            pygame.draw.rect(screen, (255, 255, 255), self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)


def show_settings(screen):
    # Obtenir le chemin absolu du fichier image de fond
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, "../game/assets/backgrounds/menu_background.png")

    # Charger l'image de fond
    background = pygame.image.load(background_path)

    # Définir les options de paramètres
    settings_items = ["Touches de contrôle", "Volume", "Retour"]
    selected_item = 0

    # Définir la police et la taille
    font_path = os.path.join(current_dir, "../game/assets/fonts/Seagram tfb.ttf")
    font = pygame.font.Font(font_path, 50)
    title_font = pygame.font.Font(font_path, 80)

    # Créer les boutons des paramètres
    buttons = []
    button_width = 400
    button_height = 60
    button_x = (screen.get_width() - button_width) // 2
    button_y_start = 300
    button_y_padding = 100

    for i, item in enumerate(settings_items):
        button_y = button_y_start + i * button_y_padding
        button = Button(item, font, (200, 200, 200), button_x, button_y, button_width, button_height)
        buttons.append(button)

    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if selected_item == 0:
                        show_controls_settings(screen)
                    elif selected_item == 1:
                        show_volume_settings(screen)
                    elif selected_item == 2:
                        return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.hovered:
                        if i == 0:
                            show_controls_settings(screen)
                        elif i == 1:
                            show_volume_settings(screen)
                        elif i == 2:
                            return

        # Afficher l'image de fond
        screen.blit(background, (0, 0))

        # Afficher le titre des paramètres
        title_text = title_font.render("Paramètres", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() / 2, 100))
        screen.blit(title_text, title_rect)

        # Afficher les boutons des paramètres
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()
        clock.tick(30)


def show_volume_settings(screen):
    current_volume = pygame.mixer.music.get_volume()
    
    # Obtenir le chemin absolu du fichier image de fond
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, "../game/assets/backgrounds/menu_background.png")

    # Charger l'image de fond
    background = pygame.image.load(background_path)

    # Définir les boutons de volume
    volume_items = ["Augmenter Volume", "Diminuer Volume", "Retour"]
    selected_item = 0

    # Définir la police et la taille
    font_path = os.path.join(current_dir, "../game/assets/fonts/Seagram tfb.ttf")
    font = pygame.font.Font(font_path, 50)
    title_font = pygame.font.Font(font_path, 80)

    # Créer les boutons de volume
    buttons = []
    button_width = 400
    button_height = 60
    button_x = (screen.get_width() - button_width) // 2
    button_y_start = 300
    button_y_padding = 100

    for i, item in enumerate(volume_items):
        button_y = button_y_start + i * button_y_padding
        button = Button(item, font, (200, 200, 200), button_x, button_y, button_width, button_height)
        buttons.append(button)

    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if selected_item == 0:
                        current_volume = min(1.0, current_volume + 0.1)
                        pygame.mixer.music.set_volume(current_volume)
                    elif selected_item == 1:
                        current_volume = max(0.0, current_volume - 0.1)
                        pygame.mixer.music.set_volume(current_volume)
                    elif selected_item == 2:
                        return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.hovered:
                        if i == 0:
                            current_volume = min(1.0, current_volume + 0.1)
                            pygame.mixer.music.set_volume(current_volume)
                        elif i == 1:
                            current_volume = max(0.0, current_volume - 0.1)
                            pygame.mixer.music.set_volume(current_volume)
                        elif i == 2:
                            return

        # Afficher l'image de fond
        screen.blit(background, (0, 0))

        # Afficher le titre des paramètres de volume
        title_text = title_font.render("Volume", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() / 2, 100))
        screen.blit(title_text, title_rect)

        # Afficher le niveau de volume actuel
        volume_text = font.render(f"Volume: {int(current_volume * 100)}%", True, (255, 255, 255))
        volume_rect = volume_text.get_rect(center=(screen.get_width() / 2, 200))
        screen.blit(volume_text, volume_rect)

        # Afficher les boutons de volume
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    show_settings(screen)
    pygame.quit()
