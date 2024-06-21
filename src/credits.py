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
    # Obtenir le chemin absolu du fichier image de fond
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, "../game/assets/backgrounds/menu_background.png")
    photo1_path = os.path.join(current_dir, "../game/assets/characters/samuel.png")
    photo2_path = os.path.join(current_dir, "../game/assets/characters/jonathan.png")

    # Charger l'image de fond et les photos des créateurs
    background = pygame.image.load(background_path)
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

    # Définir la police et la taille
    font_path = os.path.join(current_dir, "../game/assets/fonts/Seagram tfb.ttf")
    font = pygame.font.Font(font_path, screen.get_height() // 40)
    title_font = pygame.font.Font(font_path, screen.get_height() // 20)

    # Définir le texte des crédits
    credits_text = """
    🥋 Jeu de Combat - INF2300 Infographie 🥋

    Introduction
    Bienvenue dans notre projet de jeu de combat ! Ce projet a été créé avec une passion débordante pour l'apprentissage et l'excellence en programmation. Inspiré par les géants du code, Coder Space et Coding With Russ, nous avons mis tout notre cœur (et un peu de sueur) dans ce jeu. Préparez-vous à découvrir un univers où chaque ligne de code compte et où les combats sont épiques ! 🎮

    Inspiration
    Ce projet n'aurait pas été possible sans l'inspiration tirée des travaux exceptionnels de :
    - Coder Space
      - YouTube : Coder Space Channel
      - GitHub : Stanislav Petrov

    - Coding With Russ
      - YouTube : Coding With Russ
      - GitHub : Russ

    Merci à eux pour leur partage de connaissances et leurs tutos incroyables. Vous êtes des rock stars du code ! 🤘

    Utilisation des Assets
    Tous les assets utilisés dans ce projet proviennent de itch.io et ont été fournis gratuitement. Nous respectons pleinement les droits d'auteur des créateurs. Un grand merci à la communauté d'itch.io pour rendre ce projet encore plus visuellement attrayant ! 🎨

    Licence
    Ce projet est sous licence MIT. Cela signifie que vous êtes libre de l'utiliser, de le modifier et de le partager. Nous vous encourageons à le faire pour promouvoir le partage de la connaissance libre. Après tout, le savoir est fait pour être partagé, pas pour rester caché dans un tiroir poussiéreux ! 📚✨

    Contact
    Nous sommes toujours ouverts aux questions, suggestions et messages d'encouragement (ou même de défis !) :
    - 📧 isteah.josephsamuel@gmail.com – JOSEPH Samuel Jonathan
    - 📧 isteah.jpierrelouis03@gmail.com – JONATHAN Pierre Louis

    Informations du Cours
    - Cours : INF2300 Infographie
    - Session : Été 2024
    - Travail No. : 2
    - Groupe :
      - JOSEPH Samuel Jonathan
      - JONATHAN Pierre Louis
    - Soumis au : Dre. Franjieh El Khoury
    - Date : 20 juin 2024

    Fonctionnalités du Jeu
    - 🎬 Introduction Vidéo : Une vidéo d'introduction captivante pour plonger les joueurs dans l'ambiance du jeu.
    - 🕹️ Menu Principal : Avec un fond animé et des options claires (Play, Settings, Credits, Exit).
    - 🥊 Modes de Combat : Choisissez entre 1 vs 2, 1 vs Computer, ou Computer vs Computer. Peu importe le mode, le choix du personnage est à vous !
    - 🎶 Paramètres : Ajustez le son, la musique et les effets pour une expérience de jeu optimale.
    - 👨‍💻 Crédits : Découvrez les cerveaux derrière ce projet incroyable.

    Remerciements
    Un immense merci à nos professeurs, collègues, amis, et bien sûr, à vous, pour votre intérêt et votre soutien. Et souvenez-vous : coder, c'est comme combattre – il faut de la stratégie, de la détermination, et parfois, un bon café ! ☕👨‍💻👩‍💻
    """

    scrolling_text = ScrollingText(credits_text, font, (255, 0, 0), screen.get_width() // 2, screen.get_height(), screen.get_width() - 40)

    # Créer le bouton "Retour"
    button_font = pygame.font.Font(font_path, screen.get_height() // 30)
    return_button = Button("Retour", button_font, (200, 200, 200), screen.get_width() // 2 - 100, screen.get_height() - 100, 200, 50)

    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.hovered:
                    return

        # Redimensionner l'image de fond
        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
        screen.blit(background, (0, 0))

        # Afficher les photos des créateurs
        screen.blit(photo1, (screen.get_width() // 4 - photo1.get_width() // 2, 50))
        screen.blit(photo2, (3 * screen.get_width() // 4 - photo2.get_width() // 2, 50))

        # Afficher le texte défilant
        scrolling_text.draw(screen, 1)

        # Afficher le bouton "Retour"
        return_button.check_hover(mouse_pos)
        return_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    show_credits(screen)
    pygame.quit()
