import pygame
import os

def show_menu(screen):
    # Obtenir le chemin absolu du fichier image de fond et du fichier son
    current_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(current_dir, "../game/assets/backgrounds/menu_background.png")
    sound_path = os.path.join(current_dir, "../game/assets/music/LEMMiNO - Cipher (BGM).mp3")

    # Charger l'image de fond
    background = pygame.image.load(background_path)

    # Initialiser Pygame Mixer pour le son de fond
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play(-1)  # Jouer en boucle

    # Définir les options du menu
    menu_items = ["Jouer", "Paramètres", "Crédits", "Quitter"]
    selected_item = 0

    # Définir la police et la taille
    font = pygame.font.Font(None, 74)
    title_font = pygame.font.Font(None, 100)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected_item == 0:
                        print("Jouer sélectionné")
                        # show_game_modes(screen)  # À implémenter
                    elif selected_item == 1:
                        print("Paramètres sélectionné")
                        # show_settings(screen)  # À implémenter
                    elif selected_item == 2:
                        print("Crédits sélectionné")
                        # show_credits(screen)  # À implémenter
                    elif selected_item == 3:
                        pygame.quit()
                        return
        
        # Afficher l'image de fond
        screen.blit(background, (0, 0))

        # Afficher le titre du jeu
        title_text = title_font.render("Blades of Honor: Clash of Cultures", True, (255, 255, 255))
        screen.blit(title_text, (100, 50))

        # Afficher les options du menu
        for i, item in enumerate(menu_items):
            color = (255, 0, 0) if i == selected_item else (255, 255, 255)
            text = font.render(item, True, color)
            screen.blit(text, (350, 200 + i * 100))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    show_menu(screen)
    pygame.quit()
