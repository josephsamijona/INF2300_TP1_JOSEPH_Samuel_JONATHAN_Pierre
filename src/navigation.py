import pygame
import os
import cv2

def return_to_menu(screen, root_dir):
    from src.game_modes import show_game_modes  # Importation locale pour éviter les imports circulaires

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)  # Aller au niveau supérieur pour accéder à assets
    video_path = os.path.join(project_root, "game", "assets", "video", "3_background.mp4")
    click_sound_path = os.path.join(project_root, "game", "assets", "sfx", "click.wav")
    hover_sound_path = os.path.join(project_root, "game", "assets", "sfx", "hover.wav")

    cap = cv2.VideoCapture(video_path)

    sound_path = os.path.join(project_root, "game", "assets", "music", "LEMMiNO - Cipher (BGM).mp3")
    pygame.mixer.init()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)

    click_sound = pygame.mixer.Sound(click_sound_path)
    hover_sound = pygame.mixer.Sound(hover_sound_path)

    show_game_modes(screen, root_dir)
