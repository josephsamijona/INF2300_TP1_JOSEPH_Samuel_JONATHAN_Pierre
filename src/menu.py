import pygame
import os
from src.settings import show_settings
from src.credits import show_credits
from src.game_modes import show_game_modes

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


def show_menu(screen):
    # Obtenir le chemin absolu du fichier image de fond et du fichier son
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, "../game/assets/backgrounds/menu_background.png")
    sound_path = os.path.join(current_dir, "../game/assets/music/LEMMiNO - Cipher (BGM).mp3")

    # Charger l'image de fond
    background = pygame.image.load(background_path)

    # Initialiser Pygame Mixer pour le son de fond
    pygame.mixer.init()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)  # Jouer en boucle

    # Définir les options du menu
    menu_items = ["Jouer", "Paramètres", "Crédits", "Quitter"]
    selected_item = 0

    # Définir la police et la taille
    font_path = os.path.join(current_dir, "../game/assets/fonts/Seagram tfb.ttf")
    font = pygame.font.Font(font_path, 50)
    title_font = pygame.font.Font(font_path, 80)

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
                        show_game_modes(screen, show_menu)
                    elif selected_item == 1:
                        show_settings(screen)
                    elif selected_item == 2:
                        show_credits(screen)
                    elif selected_item == 3:
                        pygame.quit()
                        return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.hovered:
                        if i == 0:
                            show_game_modes(screen, show_menu)
                        elif i == 1:
                            show_settings(screen)
                        elif i == 2:
                            show_credits(screen)
                        elif i == 3:
                            pygame.quit()
                            return

        # Redimensionner l'image de fond
        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
        screen.blit(background, (0, 0))

        # Afficher le titre du jeu
        title_text = title_font.render("Blades of Honor: Clash of Cultures", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() / 2, 100))
        screen.blit(title_text, title_rect)

        # Créer et afficher les boutons du menu
        buttons = []
        button_width = screen.get_width() // 3
        button_height = screen.get_height() // 12
        button_x = (screen.get_width() - button_width) // 2
        button_y_start = screen.get_height() // 3
        button_y_padding = screen.get_height() // 10  # Augmenter l'espace entre les boutons

        for i, item in enumerate(menu_items):
            button_y = button_y_start + i * button_y_padding
            button = Button(item, font, (200, 200, 200), button_x, button_y, button_width, button_height)
            button.check_hover(mouse_pos)
            button.draw(screen)
            buttons.append(button)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    show_menu
