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

def show_controls_settings(screen):
    # Obtenir le chemin absolu du fichier image de fond
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, "../game/assets/backgrounds/menu_background.png")

    # Charger l'image de fond
    background = pygame.image.load(background_path)

    # Définir les touches de contrôle
    controls_items = ["Déplacer gauche", "Déplacer droite", "Sauter", "Attaquer", "Retour"]
    controls = {"Déplacer gauche": "LEFT", "Déplacer droite": "RIGHT", "Sauter": "UP", "Attaquer": "SPACE"}
    selected_item = 0

    # Définir la police et la taille
    font_path = os.path.join(current_dir, "../game/assets/fonts/Seagram tfb.ttf")
    font = pygame.font.Font(font_path, 50)
    title_font = pygame.font.Font(font_path, 80)

    # Créer les boutons des contrôles
    buttons = []
    button_width = 400
    button_height = 60
    button_x = (screen.get_width() - button_width) // 2
    button_y_start = 200
    button_y_padding = 80

    for i, item in enumerate(controls_items):
        button_y = button_y_start + i * button_y_padding
        button_text = f"{item}: {controls[item]}" if item in controls else item
        button = Button(button_text, font, (200, 200, 200), button_x, button_y, button_width, button_height)
        buttons.append(button)

    clock = pygame.time.Clock()
    waiting_for_key = False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if waiting_for_key:
                    key_name = pygame.key.name(event.key).upper()
                    controls[controls_items[selected_item]] = key_name
                    buttons[selected_item].text = f"{controls_items[selected_item]}: {key_name}"
                    waiting_for_key = False
                elif event.key == pygame.K_RETURN:
                    if selected_item == len(controls_items) - 1:  # "Retour" is the last item
                        return
                    else:
                        waiting_for_key = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.hovered:
                        if controls_items[i] == "Retour":
                            return
                        else:
                            waiting_for_key = True
                            selected_item = i

        # Afficher l'image de fond
        screen.blit(background, (0, 0))

        # Afficher le titre des paramètres de contrôle
        title_text = title_font.render("Touches de contrôle", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() / 2, 100))
        screen.blit(title_text, title_rect)

        # Afficher les boutons des contrôles
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    show_controls_settings(screen)
    pygame.quit()
