import pygame
import os
import cv2

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

class ScrollingText:
    def __init__(self, text, font, color, x, y, width):
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.lines = [line.strip() for line in text.split('\n')]

    def draw(self, screen, speed):
        for i, line in enumerate(self.lines):
            text_surface = self.font.render(line, True, self.color)
            text_rect = text_surface.get_rect(center=(self.x, self.y + i * text_surface.get_height()))
            screen.blit(text_surface, text_rect)
        self.y -= speed

def show_credits(screen):
    # Obtenir le chemin absolu des fichiers nécessaires
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_dir, "../game/assets/video/Sunrise_animation.mp4")
    photo1_path = os.path.join(current_dir, "../game/assets/characters/samuel.png")
    photo2_path = os.path.join(current_dir, "../game/assets/characters/jonathan.png")
    click_sound_path = os.path.join(current_dir, "../game/assets/sfx/click.wav")
    hover_sound_path = os.path.join(current_dir, "../game/assets/sfx/hover.wav")

    # Charger la vidéo avec OpenCV
    cap = cv2.VideoCapture(video_path)

    # Charger les photos des créateurs
    photo1 = pygame.image.load(photo1_path)
    photo2 = pygame.image.load(photo2_path)

    # Redimensionner les photos des créateurs
    photo1 = pygame.transform.scale(photo1, (screen.get_width() // 4, screen.get_height() // 4))
    photo2 = pygame.transform.scale(photo2, (screen.get_width() // 4, screen.get_height() // 4))

    # Initialiser Pygame Mixer pour le son de fond
    sound_path = os.path.join(current_dir, "../game/assets/music/LEMMiNO - Cipher (BGM).mp3")
    pygame.mixer.init()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)  # Jouer en boucle

    # Charger les sons de clic et de survol
    click_sound = pygame.mixer.Sound(click_sound_path)
    hover_sound = pygame.mixer.Sound(hover_sound_path)

    # Définir la police et la taille
    font_path = os.path.join(current_dir, "../game/assets/fonts/Seagram tfb.ttf")
    font = pygame.font.Font(font_path, screen.get_height() // 40)
    title_font = pygame.font.Font(font_path, screen.get_height() // 20)

    # Définir le texte des crédits
    credits_text = """
    🥋 Jeu de Combat - INF2300 Infographie 🥋

    Introduction
    Bienvenue dans notre projet de jeu de combat, créé avec passion pour l'apprentissage et l'excellence. 
    Inspiré par Coder Space et Coding With Russ, nous avons mis tout notre cœur dans ce jeu. 
    Préparez-vous à des combats épiques ! 🎮

    Inspiration
    Inspiré par :
    - Coder Space (YouTube : Coder Space, GitHub : Stanislav Petrov)
    - Coding With Russ (YouTube : Coding With Russ, GitHub : Russ)

    Merci pour le partage de connaissances. Vous êtes des rock stars du code ! 🤘

    Utilisation des Assets
    Tous les assets proviennent de itch.io et sont gratuits. Merci à la communauté d'itch.io ! 🎨

    Licence
    Projet sous licence MIT. Utilisez, modifiez et partagez librement. Partagez la connaissance libre ! 📚✨

    Contact
    Pour questions et suggestions :
    - 📧 isteah.josephsamuel@gmail.com – JOSEPH Samuel Jonathan
    - 📧 isteah.jpierrelouis03@gmail.com – JONATHAN Pierre Louis

    Informations du Cours
    - Cours : INF2300 Infographie
    - Session : Été 2024
    - Travail No. : 2
    - Groupe : JOSEPH Samuel Jonathan, JONATHAN Pierre Louis
    - Soumis à : Dre. Franjieh El Khoury
    - Date : 20 juin 2024

    Fonctionnalités du Jeu
    - 🎬 Introduction Vidéo captivante
    - 🕹️ Menu Principal animé
    - 🥊 Modes de Combat variés
    - 🎶 Paramètres ajustables
    - 👨‍💻 Crédits du projet

    Remerciements
    Merci à nos professeurs, collègues, amis, et à vous pour votre soutien. Coder, c'est comme combattre – stratégie, détermination, et café ! ☕👨‍💻👩‍💻
    """

    scrolling_text = ScrollingText(credits_text, font, (255, 0, 0), screen.get_width() // 2, screen.get_height(), screen.get_width() - 40)

    # Créer le bouton "Retour"
    button_font = pygame.font.Font(font_path, screen.get_height() // 30)
    return_button = Button("Retour", button_font, (200, 200, 200), screen.get_width() // 2 - 100, screen.get_height() - 100, 200, 50)

    clock = pygame.time.Clock()

    hover_state_return_button = False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.hovered:
                    click_sound.play()
                    return

        # Lire et afficher la vidéo
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (screen.get_width(), screen.get_height()))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))

        # Afficher les photos des créateurs
        screen.blit(photo1, (screen.get_width() // 4 - photo1.get_width() // 2, 50))
        screen.blit(photo2, (3 * screen.get_width() // 4 - photo2.get_width() // 2, 50))

        # Afficher le texte défilant
        scrolling_text.draw(screen, 1)

        # Afficher le bouton "Retour"
        return_button.check_hover(mouse_pos)
        if return_button.hovered and not hover_state_return_button:
            hover_sound.play()
            hover_state_return_button = True
        elif not return_button.hovered:
            hover_state_return_button = False
        return_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    cap.release()
    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    show_credits(screen)
    pygame.quit()
