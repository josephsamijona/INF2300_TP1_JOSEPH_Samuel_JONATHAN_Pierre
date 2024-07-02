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

# Importation de la bibliothèque Pygame pour la gestion de la fenêtre et des événements
import pygame
from src.intro import show_intro
from src.menu import show_menu

def main():
    # Initialisation de Pygame
    pygame.init()
    
    # Programmation graphique - OpenGL en Python :
    # Ici, nous avons utilisé pygame, une bibliothèque Python pour les jeux vidéo qui simplifie la création de fenêtres et la gestion des événements utilisateur.
    # Bien que ce code ne montre pas directement l'utilisation d'OpenGL, pygame est souvent utilisé conjointement avec PyOpenGL pour les graphismes avancés.
    
    # Configuration de la fenêtre principale avec Pygame
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Blades of Honor: Clash of Cultures")
    
    # Pipeline de transformation et pipeline graphique programmable, comme étapes pour l’animation :
    # Le pipeline graphique programmable fait référence aux étapes personnalisables dans le processus de rendu graphique, telles que les vertex et fragment shaders.
    # Dans ce contexte, le code initialise la fenêtre de jeu et appelle les fonctions show_intro et show_menu, qui pourraient inclure des animations et des transformations graphiques.
    # La gestion de la scène et des objets de jeu peut inclure des transformations (comme les déplacements, rotations, et mises à l'échelle) et des animations pour rendre l'intro et le menu interactifs et visuellement attrayants.
    
    # Afficher l'intro
    print("Lancement de l'intro")
    show_intro(screen)
    
    # Afficher le menu principal
    print("Affichage du menu principal")
    show_menu(screen)

    # Opérations sur les fragments, illumination et textures :
    # Les opérations sur les fragments concernent les calculs effectués sur les pixels avant l'affichage, incluant l'illumination et les textures.
    # Bien que ce code principal n'inclue pas directement ces opérations, les fonctions show_intro et show_menu peuvent appliquer des textures sur les éléments graphiques et gérer l'éclairage pour améliorer l'esthétique du jeu.
    # Par exemple, les textures peuvent être utilisées pour les arrière-plans et les éléments de l'interface utilisateur, tandis que l'illumination peut créer des effets de lumière réalistes pour améliorer l'immersion.

    # Quitter Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
