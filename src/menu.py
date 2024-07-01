#Explication du Code : Menu Principal du Jeu
#Ce code constitue le menu principal du jeu "Blades of Honor: Clash of Cultures". 
#Il utilise la bibliothèque pygame pour la gestion des événements et l'affichage des éléments graphiques. 
#Le menu principal est une interface interactive qui permet aux joueurs de naviguer entre différentes options 
#telles que "Jouer", "Paramètres", "Crédits", et "Quitter".
###############################################################################################




# Importation des bibliothèques nécessaires pour la gestion du jeu
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

def show_menu(screen):
    # Programmation graphique - OpenGL en Python :
    # Ici, nous avons utilisé pygame, une bibliothèque Python pour les jeux vidéo qui simplifie la création de fenêtres et la gestion des événements utilisateur.
    # Bien que ce code ne montre pas directement l'utilisation d'OpenGL, pygame est souvent utilisé conjointement avec PyOpenGL pour les graphismes avancés.

    # Obtenir le chemin absolu du fichier image de fond et du fichier son
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_dir, "../game/assets/video/menu_background.mp4")
    sound_path = os.path.join(current_dir, "../game/assets/music/LEMMiNO - Cipher (BGM).mp3")
    click_sound_path = os.path.join(current_dir, "../game/assets/sfx/click.wav")
    hover_sound_path = os.path.join(current_dir, "../game/assets/sfx/hover.wav")

    # Charger la vidéo avec OpenCV
    cap = cv2.VideoCapture(video_path)

    # Initialiser Pygame Mixer pour le son de fond
    pygame.mixer.init()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)  # Jouer en boucle

    # Charger les sons de clic et de survol
    click_sound = pygame.mixer.Sound(click_sound_path)
    hover_sound = pygame.mixer.Sound(hover_sound_path)

    # Définir les options du menu
    menu_items = ["Jouer", "Paramètres", "Crédits", "Quitter"]
    selected_item = 0

    # Définir la police et la taille
    font_path = os.path.join(current_dir, "../game/assets/fonts/Seagram tfb.ttf")
    font = pygame.font.Font(font_path, 50)
    title_font = pygame.font.Font(font_path, 80)

    clock = pygame.time.Clock()

    # Variables pour suivre l'état du survol des boutons
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
                        show_game_modes(screen, current_dir)
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
                            show_game_modes(screen, current_dir)
                        elif i == 1:
                            show_settings(screen)
                        elif i == 2:
                            show_credits(screen)
                        elif i == 3:
                            pygame.quit()
                            return

        # Pipeline de transformation et pipeline graphique programmable, comme étapes pour l’animation :
        # Le pipeline graphique programmable fait référence aux étapes personnalisables dans le processus de rendu graphique, telles que les vertex et fragment shaders.
        # Dans ce contexte, le code initialise la fenêtre de jeu et appelle les fonctions show_intro et show_menu, qui pourraient inclure des animations et des transformations graphiques.
        # La gestion de la scène et des objets de jeu peut inclure des transformations (comme les déplacements, rotations, et mises à l'échelle) et des animations pour rendre l'intro et le menu interactifs et visuellement attrayants.

        # Lire et afficher la vidéo
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (screen.get_width(), screen.get_height()))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))

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
            if button.hovered and not hover_states[item]:
                hover_sound.play()
                hover_states[item] = True
            elif not button.hovered:
                hover_states[item] = False
            button.draw(screen)
            buttons.append(button)

        # Opérations sur les fragments, illumination et textures :
        # Les opérations sur les fragments concernent les calculs effectués sur les pixels avant l'affichage, incluant l'illumination et les textures.
        # Bien que ce code principal n'inclue pas directement ces opérations, les fonctions show_intro et show_menu peuvent appliquer des textures sur les éléments graphiques et gérer l'éclairage pour améliorer l'esthétique du jeu.
        # Par exemple, les textures peuvent être utilisées pour les arrière-plans et les éléments de l'interface utilisateur, tandis que l'illumination peut créer des effets de lumière réalistes pour améliorer l'immersion.

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    show_menu(screen)
    pygame.quit()
