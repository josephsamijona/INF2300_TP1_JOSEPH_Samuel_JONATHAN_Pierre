import pygame
import os

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

def show_game_modes(screen, show_menu):
    # Obtenir le chemin absolu du fichier image de fond
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, "../game/assets/backgrounds/menu_background.png")

    # Charger l'image de fond
    background = pygame.image.load(background_path)

    # Définir les options des modes de jeu
    game_modes = ["1 vs Computer", "3D Adventure", "1 vs 2", "AI vs AI", "Retour"]
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
                        print("1 vs Computer sélectionné")
                        # show_1_vs_computer(screen)  # À implémenter
                    elif selected_item == 1:
                        print("3D Adventure sélectionné")
                        # show_3d_adventure(screen)  # À implémenter
                    elif selected_item == 2:
                        print("1 vs 2 sélectionné")
                        # show_1_vs_2(screen)  # À implémenter
                    elif selected_item == 3:
                        print("AI vs AI sélectionné")
                        # show_ai_vs_ai(screen)  # À implémenter
                    elif selected_item == 4:
                        return show_menu(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.hovered:
                        if i == 0:
                            print("1 vs Computer sélectionné")
                            # show_1_vs_computer(screen)  # À implémenter
                        elif i == 1:
                            print("3D Adventure sélectionné")
                            # show_3d_adventure(screen)  # À implémenter
                        elif i == 2:
                            print("1 vs 2 sélectionné")
                            # show_1_vs_2(screen)  # À implémenter
                        elif i == 3:
                            print("AI vs AI sélectionné")
                            # show_ai_vs_ai(screen)  # À implémenter
                        elif i == 4:
                            return show_menu(screen)

        # Redimensionner l'image de fond
        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
        screen.blit(background, (0, 0))

        # Afficher le titre des modes de jeu
        title_text = title_font.render("Modes de Jeu", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() / 2, 100))
        screen.blit(title_text, title_rect)

        # Créer et afficher les boutons des modes de jeu
        buttons = []
        button_width = screen.get_width() // 3
        button_height = screen.get_height() // 12
        button_x = (screen.get_width() - button_width) // 2
        button_y_start = screen.get_height() // 3
        button_y_padding = screen.get_height() // 10  # Augmenter l'espace entre les boutons

        for i, item in enumerate(game_modes):
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
    show_game_modes(screen, lambda scr: None)  # Fonction placeholder pour éviter les erreurs lors de l'exécution directe
    pygame.quit()

