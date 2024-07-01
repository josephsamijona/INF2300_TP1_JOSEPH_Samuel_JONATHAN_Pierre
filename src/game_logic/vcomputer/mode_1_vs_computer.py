import pygame
from pygame import mixer
import os
from src.game_logic.vcomputer.logic1vcom import Fighter
from src.game_logic.vcomputer.paralaxus1 import Parallax

class Game1vsc:
    def __init__(self, root_dir):
        # Initialiser le mixeur et Pygame
        mixer.init()
        pygame.init()

        # Créer la fenêtre du jeu
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 400
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Blades of Honor: Clash of Cultures")

        # Définir la fréquence d'images
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Définir les couleurs
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)

        # Définir les variables de jeu
        self.intro_count = 3
        self.last_count_update = pygame.time.get_ticks()
        self.score = [0, 0]  # scores des joueurs [P1, P2]
        self.round_over = False
        self.ROUND_OVER_COOLDOWN = 2000

        # Définir les variables des combattants
        self.WARRIOR_SIZE = 162
        self.WARRIOR_SCALE = 4
        self.WARRIOR_OFFSET = [72, 56]
        self.WARRIOR_DATA = [self.WARRIOR_SIZE, self.WARRIOR_SCALE, self.WARRIOR_OFFSET]
        self.WIZARD_SIZE = 250
        self.WIZARD_SCALE = 3
        self.WIZARD_OFFSET = [112, 107]
        self.WIZARD_DATA = [self.WIZARD_SIZE, self.WIZARD_SCALE, self.WIZARD_OFFSET]

        # Obtenir le répertoire racine du projet
        self.root_dir = root_dir

        # Charger la musique et les sons
        pygame.mixer.music.load(os.path.join(self.root_dir, "..", "game", "assets", "music", "LEMMiNO - Cipher (BGM).mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
        self.sword_fx = pygame.mixer.Sound(os.path.join(self.root_dir, "..", "game", "assets", "audio", "sword.wav"))
        self.sword_fx.set_volume(0.5)
        self.magic_fx = pygame.mixer.Sound(os.path.join(self.root_dir, "..", "game", "assets", "audio", "magic.wav"))
        self.magic_fx.set_volume(0.75)

        # Charger les images de fond pour le parallax
        self.bg_images = [pygame.image.load(os.path.join(self.root_dir, "..", "game", "assets", "backgrounds", f"plx-0.png")).convert_alpha() for i in range(1, 6)]
        self.ground_image = pygame.image.load(os.path.join(self.root_dir, "..", "game", "assets", "backgrounds", "ground.png")).convert_alpha()

        # Initialiser Parallax
        self.parallax = Parallax(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.bg_images, self.ground_image, self.FPS)

        # Charger les feuilles de sprites
        self.warrior_sheet = pygame.image.load(os.path.join(self.root_dir, "..", "game", "assets", "characters", "warrior", "Sprites", "warrior.png")).convert_alpha()
        self.wizard_sheet = pygame.image.load(os.path.join(self.root_dir, "..", "game", "assets", "characters", "wizard", "Sprites", "wizard.png")).convert_alpha()

        # Charger et redimensionner les images de victoire et de défaite
        self.victory_img = pygame.image.load(os.path.join(self.root_dir, "..", "game", "assets", "icons", "defeat.png")).convert_alpha()
        self.victory_img = pygame.transform.scale(self.victory_img, (800, 800))
        self.defeat_img = pygame.image.load(os.path.join(self.root_dir, "..", "game", "assets", "icons", "victory.png")).convert_alpha()
        self.defeat_img = pygame.transform.scale(self.defeat_img, (800, 800))

        # Définir le nombre d'étapes dans chaque animation
        self.WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
        self.WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

        # Définir la police
        self.count_font = pygame.font.Font(os.path.join(self.root_dir, "..", "game", "assets", "fonts", "Seagram tfb.ttf"), 80)
        self.score_font = pygame.font.Font(os.path.join(self.root_dir, "..", "game", "assets", "fonts", "Seagram tfb.ttf"), 30)

        # Créer deux instances de combattants
        self.fighter_1 = Fighter(1, 200, 310, False, self.WARRIOR_DATA, self.warrior_sheet, self.WARRIOR_ANIMATION_STEPS, self.sword_fx)
        self.fighter_2 = Fighter(2, 700, 310, True, self.WIZARD_DATA, self.wizard_sheet, self.WIZARD_ANIMATION_STEPS, self.magic_fx)

    # Fonction pour dessiner le texte
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    # Fonction pour dessiner les barres de santé des combattants
    def draw_health_bar(self, health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, self.WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self.screen, self.RED, (x, y, 400, 30))
        pygame.draw.rect(self.screen, self.YELLOW, (x, y, 400 * ratio, 30))

    # Fonction principale pour lancer le jeu
    def run(self):
        run = True
        while run:
            self.clock.tick(self.FPS)

            # Dessiner le fond avec l'effet parallax
            self.parallax.draw()

            # Afficher les statistiques des joueurs
            self.draw_health_bar(self.fighter_1.health, 20, 20)
            self.draw_health_bar(self.fighter_2.health, 580, 20)
            self.draw_text("P1: " + str(self.score[0]), self.score_font, self.RED, 20, 60)
            self.draw_text("P2: " + str(self.score[1]), self.score_font, self.RED, 580, 60)

            # Mettre à jour le compte à rebours
            if self.intro_count <= 0:
                # Déplacer les combattants
                self.fighter_1.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, self.fighter_2, self.round_over)
                self.fighter_2.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, self.fighter_1, self.round_over)
            else:
                # Afficher le compte à rebours
                self.draw_text(str(self.intro_count), self.count_font, self.RED, self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 3)
                # Mettre à jour le compte à rebours
                if (pygame.time.get_ticks() - self.last_count_update) >= 1000:
                    self.intro_count -= 1
                    self.last_count_update = pygame.time.get_ticks()

            # Mettre à jour les combattants
            self.fighter_1.update()
            self.fighter_2.update()

            # Dessiner les combattants
            self.fighter_1.draw(self.screen)
            self.fighter_2.draw(self.screen)

            # Vérifier la défaite des joueurs
            if self.round_over == False:
                if self.fighter_1.alive == False:
                    self.score[1] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
                elif self.fighter_2.alive == False:
                    self.score[0] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
            else:
                # Afficher l'image de victoire ou de défaite au centre de l'écran
                if self.fighter_1.alive == False:
                    img_to_display = self.victory_img
                else:
                    img_to_display = self.defeat_img

                victory_rect = img_to_display.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
                self.screen.blit(img_to_display, victory_rect.topleft)

                if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                    self.round_over = False
                    self.intro_count = 3
                    self.fighter_1 = Fighter(1, 200, 310, False, self.WARRIOR_DATA, self.warrior_sheet, self.WARRIOR_ANIMATION_STEPS, self.sword_fx)
                    self.fighter_2 = Fighter(2, 700, 310, True, self.WIZARD_DATA, self.wizard_sheet, self.WIZARD_ANIMATION_STEPS, self.magic_fx)

            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Mettre à jour l'affichage
            pygame.display.update()

        # Quitter Pygame
        pygame.quit()

