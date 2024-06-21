import os
import cv2
import pygame

def show_intro(screen):
    # Obtenir le chemin absolu du fichier vidéo et audio
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_dir, "../game/assets/video/intro.mp4")
    audio_path = os.path.join(current_dir, "../game/assets/music/intro.mp3")
    
    # Initialiser OpenCV pour la vidéo
    cap = cv2.VideoCapture(video_path)

    # Initialiser Pygame Mixer pour le son
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    clock = pygame.time.Clock()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir l'image de OpenCV (BGR) à Pygame (RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.rotate(frame_surface, -90)
        frame_surface = pygame.transform.flip(frame_surface, True, False)

        # Afficher l'image sur l'écran
        screen.blit(frame_surface, (0, 0))
        pygame.display.flip()

        # Limiter la vitesse d'affichage à 30 fps
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                return

    cap.release()
    pygame.mixer.music.stop()

