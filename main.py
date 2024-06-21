# INF2300 Infographie
# ÉTÉ 2024
# 
# Travail No. [1]
# 
# Groupe
# [isteah.josephsamuel@gmail.com] – [JOSEPH Samuel Jonathan]
# [isteah.jpierrelouis03@gmail.com] – [JONATHAN Pierre Louis]
# 
# Soumis au : Dre. Franjieh El Khoury
# 
# [6/20/2024]

"""
Ce fichier main.py sert de point d'entrée principal pour le jeu de combat en 2D.
Il initialise les bibliothèques Pygame et OpenGL, configure la fenêtre principale,
et définit les paramètres de base pour OpenGL.

Les étapes principales du script sont les suivantes :
1. Initialisation de Pygame pour gérer la fenêtre et les événements.
2. Configuration de la fenêtre principale avec une taille de 800x600 pixels,
   utilisant OpenGL pour le rendu graphique et le double buffering pour éviter
   le scintillement.
3. Initialisation des paramètres OpenGL, y compris l'activation du mélange pour
   gérer la transparence et la définition de la couleur de fond de la fenêtre.
4. Affichage de l'intro vidéo du jeu en appelant la fonction show_intro.
5. Affichage du menu principal du jeu en appelant la fonction show_menu.
6. Nettoyage et fermeture de Pygame lors de la sortie du jeu.

Ce script constitue la base du jeu, et les fonctionnalités supplémentaires telles
que les modes de jeu, la sélection des personnages, les paramètres et les crédits
seront développées dans des modules séparés et intégrées via les appels de fonction
dans ce fichier principal.
"""
import pygame
from src.intro import show_intro
from src.menu import show_menu

def main():
    # Initialisation de Pygame
    pygame.init()
    
    # Configuration de la fenêtre principale avec Pygame
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("Blades of Honor: Clash of Cultures")
    
    # Afficher l'intro
    print("Lancement de l'intro")
    show_intro(screen)
    
    # Afficher le menu principal
    print("Affichage du menu principal")
    show_menu(screen)

    pygame.quit()

if __name__ == "__main__":
    main()
