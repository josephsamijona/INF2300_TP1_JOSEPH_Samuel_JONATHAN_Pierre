import pygame
import os
import cv2
from src.game_logic.unvdeux.mode_1_vs_2 import Game1vs2
from src.game_logic.vcomputer.mode_1_vs_computer import Game1vsc
from src.game_logic.aivai.mode_ai_vs_ai import Gameaivai
from src.game_logic.trid.mode_3d_adventure import Game

class Button:
    def __init__(self, text, font, color, x, y, width, height):
        self.text = text
        self.font = font
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False
        self.original_size = (width, height)
        self.hovered_size = (int(width * 1.1), int(height * 1.1))

    def draw(self, screen):
        if self.hovered:
            button_rect = pygame.Rect(self.rect.x, self.rect.y, *self.hovered_size)
            button_rect.center = self.rect.center
            pygame.draw.rect(screen, (255, 255, 255), button_rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

def show_game_modes(screen, root_dir):
    # Programmation graphique avec pygame
    # Utilisation de pygame pour gérer les fenêtres et les événements utilisateur, souvent couplé avec PyOpenGL pour les graphismes avancés.

    # Obtenir le chemin absolu du fichier vidéo de fond
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_dir, "../game/assets/video/3_background.mp4")
    click_sound_path = os.path.join(current_dir, "../game/assets/sfx/click.wav")
    hover_sound_path = os.path.join(current_dir, "../game/assets/sfx/hover.wav")

    # Charger la vidéo avec OpenCV
    cap = cv2.VideoCapture(video_path)

    # Initialiser Pygame Mixer pour le son de fond
    sound_path = os.path.join(current_dir, "../game/assets/music/LEMMiNO - Cipher (BGM).mp3")
    pygame.mixer.init()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)  # Jouer en boucle

    # Charger les sons de clic et de survol
    click_sound = pygame.mixer.Sound(click_sound_path)
    hover_sound = pygame.mixer.Sound(hover_sound_path)

    # Définir les options des modes de jeu
    game_mode_items = ["1 vs Computer", "1 vs 2", "AI vs AI", "3D Adventure", "Retour"]
    selected_item = 0

    # Définir la police et la taille
    font_path = os.path.join(current_dir, "../game/assets/fonts/Seagram tfb.ttf")
    font = pygame.font.Font(font_path, 50)
    title_font = pygame.font.Font(font_path, 80)

    clock = pygame.time.Clock()

    # Variables pour suivre l'état du survol des boutons
    hover_states = {item: False for item in game_mode_items}

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
                        # Lancer le mode 1 vs Computer
                    elif selected_item == 1:
                        print("1 vs 2 sélectionné")
                        game = Game1vs2(root_dir)
                        game.run()
                    elif selected_item == 2:
                        print("AI vs AI sélectionné")
                        # Lancer le mode AI vs AI
                    elif selected_item == 3:
                        print("3D Adventure sélectionné")
                        pygame.mixer.music.stop()  # Arrêter la musique avant de lancer le jeu
                        game = Game(root_dir)
                        game.run()
                    elif selected_item == 4:
                        return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.hovered:
                        click_sound.play()
                        if i == 0:
                            print("1 vs Computer sélectionné")
                            game = Game1vsc(root_dir)
                            game.run()
                        elif i == 1:
                            print("1 vs 2 sélectionné")
                            game = Game1vs2(root_dir)
                            game.run()
                        elif i == 2:
                            print("AI vs AI sélectionné")
                            game = Gameaivai(root_dir)
                            game.run()
                        elif i == 3:
                            print("3D Adventure sélectionné")
                            pygame.mixer.music.stop()  # Arrêter la musique avant de lancer le jeu
                            game = Game(root_dir)
                            game.run()
                        elif i == 4:
                            return

        # Pipeline de transformation et pipeline graphique programmable, comme étapes pour l’animation :
        # Ce pipeline fait référence aux étapes personnalisables dans le rendu graphique, telles que les vertex et fragment shaders.
        # Le code initialise la fenêtre de jeu et appelle des fonctions qui pourraient inclure des animations et transformations graphiques.
        # La gestion de la scène peut inclure des transformations (déplacements, rotations, mises à l'échelle) et des animations pour rendre l'interface interactive.

        # Lire et afficher la vidéo
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (screen.get_width(), screen.get_height()))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))

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

        for i, item in enumerate(game_mode_items):
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
        # Les opérations sur les fragments incluent les calculs sur les pixels avant l'affichage, comme l'illumination et les textures.
        # Les fonctions de ce code peuvent appliquer des textures sur les éléments graphiques et gérer l'éclairage pour améliorer l'esthétique.
        # Par exemple, les textures peuvent être utilisées pour les arrière-plans et les éléments de l'interface utilisateur, tandis que l'illumination peut créer des effets de lumière réalistes.

        pygame.display.flip()
        clock.tick(30)

    cap.release()
    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    # Initialiser Pygame Mixer pour le son de fond
    pygame.mixer.init()
    sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../game/assets/music/LEMMiNO - Cipher (BGM).mp3")
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play(-1)  # Jouer en boucle

    show_game_modes(screen, os.path.dirname(os.path.abspath(__file__)))
    pygame.quit()

