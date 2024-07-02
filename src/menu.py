#Explication du Code : Menu Principal du Jeu
#Ce code constitue le menu principal du jeu "Blades of Honor: Clash of Cultures". 
#Il utilise la bibliothèque pygame pour la gestion des événements et l'affichage des éléments graphiques. 
#Le menu principal est une interface interactive qui permet aux joueurs de naviguer entre différentes options 
#telles que "Jouer", "Paramètres", "Crédits", et "Quitter".
###############################################################################################




import pygame
import os
import cv2
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
        self.original_size = (width, height)

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
        if self.hovered:
            self.rect.size = (self.original_size[0] * 1.1, self.original_size[1] * 1.1)
            self.rect.center = mouse_pos
        else:
            self.rect.size = self.original_size

def show_menu(screen, root_dir=None, cap=None, click_sound=None, hover_sound=None):
    if root_dir is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)  # Aller au niveau supérieur pour accéder à assets
    video_path = os.path.join(root_dir, "game", "assets", "video", "menu_background.mp4")
    sound_path = os.path.join(root_dir, "game", "assets", "music", "LEMMiNO - Cipher (BGM).mp3")
    click_sound_path = os.path.join(root_dir, "game", "assets", "sfx", "click.wav")
    hover_sound_path = os.path.join(root_dir, "game", "assets", "sfx", "hover.wav")

    if cap is None:
        cap = cv2.VideoCapture(video_path)
    if click_sound is None:
        click_sound = pygame.mixer.Sound(click_sound_path)
    if hover_sound is None:
        hover_sound = pygame.mixer.Sound(hover_sound_path)

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)

    menu_items = ["Jouer", "Paramètres", "Crédits", "Quitter"]
    selected_item = 0

    font_path = os.path.join(root_dir, "game", "assets", "fonts", "Seagram tfb.ttf")
    font = pygame.font.Font(font_path, 50)
    title_font = pygame.font.Font(font_path, 80)

    clock = pygame.time.Clock()

    hover_states = {item: False for item in menu_items}

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if selected_item == 0:
                        show_game_modes(screen, root_dir)
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
                        click_sound.play()
                        if i == 0:
                            show_game_modes(screen, root_dir)
                        elif i == 1:
                            show_settings(screen)
                        elif i == 2:
                            show_credits(screen)
                        elif i == 3:
                            pygame.quit()
                            return

        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (screen.get_width(), screen.get_height()))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))

        title_text = title_font.render("Blades of Honor: Clash of Cultures", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() / 2, 100))
        screen.blit(title_text, title_rect)

        buttons = []
        button_width = screen.get_width() // 3
        button_height = screen.get_height() // 12
        button_x = (screen.get_width() - button_width) // 2
        button_y_start = screen.get_height() // 3
        button_y_padding = screen.get_height() // 10

        for i, item in enumerate(menu_items):
            button_y = button_y_start + i * button_y_padding
            button = Button(item, font, (200, 200, 200), button_x, button_y, button_width, button_height)
            button.check_hover(mouse_pos)
            if button.hovered and not hover_states[item]:
                hover_sound.play()
                hover_states[item] = True
            elif not button.hovered:
                hover_states[item] = False
            button.draw(screen)
            buttons.append(button)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    show_menu(screen)
    pygame.quit()
