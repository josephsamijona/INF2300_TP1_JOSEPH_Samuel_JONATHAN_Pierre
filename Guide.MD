# Guide d'Évaluation pour le Professeur

Ce guide est conçu pour aider le professeur à naviguer efficacement dans le projet "Blades of Honor: Clash of Cultures" et à évaluer les différents aspects techniques et fonctionnels. Voici l'ordre recommandé pour explorer les fichiers et les répertoires du projet :


## 🕹️ Étape 2: Explorer le Menu Principal
**📂 Fichier à voir**: `src/menu.py`

Ce fichier contient la logique pour le menu principal, permettant aux joueurs de naviguer entre les différents modes de jeu et d'accéder aux paramètres.

## 🕵️‍♂️ Étape 3: Comprendre les Modes de Jeu
**📂 Fichiers à voir**:

- `src/game_logic/aivai/mode_ai_vs_ai.py`
- `src/game_logic/trid/mode_3d_adventure.py`
- `src/game_logic/unvdeux/mode_1_vs_2.py`
- `src/game_logic/vcomputer/mode_1_vs_computer.py`

Chaque fichier représente un mode de jeu distinct. Ils contiennent la logique pour les interactions et les règles spécifiques à chaque mode.

### 🤖 3.1. Mode AI vs AI
**📂 Fichier à voir**: `src/game_logic/aivai/mode_ai_vs_ai.py`

Ce mode simule un combat entre deux combattants contrôlés par l'IA. Le fichier contient la logique de l'IA pour les mouvements, les attaques et les décisions.

### 🏞️ 3.2. Mode 3D Adventure
**📂 Fichier à voir**: `src/game_logic/trid/mode_3d_adventure.py`

Ce mode utilise des techniques de ray casting pour créer une expérience de jeu en 3D. Les concepts d'OpenGL en Python, de pipeline de transformation et de pipeline graphique programmable sont appliqués ici.

### 🥋 3.3. Mode 1 vs 2
**📂 Fichier à voir**: `src/game_logic/unvdeux/mode_1_vs_2.py`

Dans ce mode, un joueur combat contre deux adversaires. Le fichier contient la logique pour les contrôles du joueur et l'IA des adversaires.

### 💻 3.4. Mode 1 vs Computer
**📂 Fichier à voir**: `src/game_logic/vcomputer/mode_1_vs_computer.py`

Ce mode permet à un joueur de combattre contre un adversaire contrôlé par l'ordinateur. La logique de l'IA et les interactions du joueur sont gérées ici.

## 🧩 Étape 4: Explorer les Classes et Fonctions Principales
**📂 Fichier à voir**: `src/game_modes.py`

Ce fichier centralise les différents modes de jeu et contient les classes principales utilisées dans chaque mode.

**🏷️ Classes importantes**:

- `Gameaivai`: Gère le mode AI vs AI.
- `Game1vs2`: Gère le mode 1 vs 2.
- `Game1vsc`: Gère le mode 1 vs Computer.
- `Game3D`: Gère le mode 3D Adventure.

## 📦 Étape 5: Gestion des Ressources
**📂 Répertoire à voir**: `game/assets/`

Ce répertoire contient tous les fichiers de ressources nécessaires pour le jeu, tels que les images, les sons, les musiques, les icônes et les textures.

**📁 Sous-répertoires**:

- `audio/`
- `backgrounds/`
- `fonts/`
- `icons/`
- `music/`
- `sprites/`
- `textures/`

## ⚙️ Étape 6: Paramètres et Configurations
**📂 Fichier à voir**: `src/settings.py`

Ce fichier contient les paramètres et configurations du jeu, permettant de modifier des aspects tels que la résolution de l'écran, le volume sonore et d'autres paramètres de jeu.

## 🎓 Étape 7: Crédits et Documentation
**📂 Fichier à voir**: `src/credits.py`

Ce fichier contient les crédits du jeu, répertoriant les contributeurs et les ressources utilisées.

**📂 Fichier à voir**: `README.md`

Le fichier README contient une vue d'ensemble du projet, des instructions d'installation et d'utilisation, ainsi que des informations sur les ressources et les inspirations du projet.

## 🎯 Conclusion

Ce guide vous permettra de naviguer efficacement à travers le projet "Blades of Honor: Clash of Cultures" et d'évaluer les différents aspects techniques et fonctionnels. N'hésitez pas à explorer chaque fichier et répertoire pour une compréhension approfondie du jeu et de son architecture.


