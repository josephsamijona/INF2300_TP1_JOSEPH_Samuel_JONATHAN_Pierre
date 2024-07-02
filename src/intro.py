import os
import cv2
import pygame

def show_intro(screen):
    # Initialisation de la Vidéo et de l'Audio :
    # Le code utilise os pour obtenir les chemins absolus des fichiers vidéo et audio.
    # cv2.VideoCapture initialise la capture vidéo avec OpenCV.
    # pygame.mixer.init() initialise le mixer de Pygame pour gérer le son.
    
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

    # Difficulté de Lecture des Vidéos avec Son :
    # La lecture synchronisée de vidéos et de sons est complexe et nécessite souvent des outils comme FFmpeg.
    # FFmpeg ajoute des dépendances et peut compliquer l'installation.
    # OpenCV pour la vidéo et Pygame pour le son simplifient cette gestion tout en restant efficaces.
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Traitement de la Vidéo :
        # La vidéo est lue cadre par cadre avec OpenCV.
        # Chaque cadre est redimensionné pour correspondre à la taille de l'écran.
        # Les couleurs du cadre sont converties de BGR (format OpenCV) à RGB (format Pygame).
        # Le cadre est transformé en surface Pygame, puis tourné et retourné pour un affichage correct.
        
        # Redimensionner le cadre pour qu'il corresponde à la taille de l'écran
        frame = cv2.resize(frame, (screen.get_width(), screen.get_height()))

        # Convertir l'image de OpenCV (BGR) à Pygame (RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.rotate(frame_surface, -90)
        frame_surface = pygame.transform.flip(frame_surface, True, False)

        # Affichage et Synchronisation :
        # Chaque cadre est affiché sur l'écran Pygame.
        # La boucle limite l'affichage à 30 fps pour une synchronisation fluide.
        # Les événements Pygame sont gérés pour permettre la fermeture propre du programme.
        
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

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    show_intro(screen)
    pygame.quit()
