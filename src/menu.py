import pygame
import os
from src.settings import show_settings

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

    # Créer les boutons du menu
    buttons = []
    button_width = 300
    button_height = 60
    button_x = (screen.get_width() - button_width) // 2
    button_y_start = 300
    button_y_padding = 100

    for i, item in enumerate(menu_items):
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
                        print("Jouer sélectionné")
                        # show_game_modes(screen)  # À implémenter
                    elif selected_item == 1:
                        print("Paramètres sélectionné")
                        show_settings(screen)
                    elif selected_item == 2:
                        print("Crédits sélectionné")
                        # show_credits(screen)  # À implémenter
                    elif selected_item == 3:
                        pygame.quit()
                        return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.hovered:
                        if i == 0:
                            print("Jouer sélectionné")
                            # show_game_modes(screen)  # À implémenter
                        elif i == 1:
                            print("Paramètres sélectionné")
                            show_settings(screen)
                        elif i == 2:
                            print("Crédits sélectionné")
                            # show_credits(screen)  # À implémenter
                        elif i == 3:
                            pygame.quit()
                            return

        # Afficher l'image de fond
        screen.blit(background, (0, 0))

        # Afficher le titre du jeu
        title_text = title_font.render("Blades of Honor: Clash of Cultures", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() / 2, 100))
        screen.blit(title_text, title_rect)

        # Afficher les boutons du menu
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    show_menu(screen)
    pygame.quit()

