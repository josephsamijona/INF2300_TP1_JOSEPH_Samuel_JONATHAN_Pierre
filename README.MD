# 🥋 Jeu de Combat - INF2300 Infographie 🥋

## Introduction
Bienvenue dans notre projet de jeu de combat ! Ce projet a été créé avec une passion débordante pour l'apprentissage et l'excellence en programmation. Inspiré par les géants du code, **Coder Space**, **Coding With Russ**, et **FinFET**, nous avons mis tout notre cœur (et un peu de sueur) dans ce jeu. Préparez-vous à découvrir un univers où chaque ligne de code compte et où les combats sont épiques ! 🎮

![Game](https://img.shields.io/badge/GAME-Awesome-blue)
![Code](https://img.shields.io/badge/CODE-100%25-brightgreen)
![Learning](https://img.shields.io/badge/LEARNING-Fun-yellow)

## Inspiration
Ce projet n'aurait pas été possible sans l'inspiration tirée des travaux exceptionnels de :
- **Coder Space**
  - YouTube : [Coder Space Channel](https://www.youtube.com/@CoderSpaceChannel)
  - GitHub : [Stanislav Petrov](https://github.com/StanislavPetrovV)
- **Coding With Russ**
  - YouTube : [Coding With Russ](https://www.youtube.com/@CodingWithRuss)
  - GitHub : [Russ](https://github.com/russs123)
- **FinFET**
  - YouTube : [FinFET](https://www.youtube.com/@FinFET)
  - GitHub : [FinFET Channel](https://github.com/FinFetChannel)
  - itch.io : [Dead and Forgotten](https://finfetchannel.itch.io/dead-and)

Merci à eux pour leur partage de connaissances et leurs tutos incroyables. Vous êtes des rock stars du code ! 🤘

![Inspiration](https://img.shields.io/badge/INSPIRATION-High-blueviolet)

## Utilisation des Assets
Tous les assets utilisés dans ce projet proviennent de [itch.io](https://itch.io/) et ont été fournis gratuitement. Nous respectons pleinement les droits d'auteur des créateurs. Un grand merci à la communauté d'itch.io pour rendre ce projet encore plus visuellement attrayant ! 🎨

![Assets](https://img.shields.io/badge/ASSETS-itch.io-orange)

## Fonctionnalités du Jeu
- 🎬 **Introduction Vidéo :** Une vidéo d'introduction captivante pour plonger les joueurs dans l'ambiance du jeu.
- 🕹️ **Menu Principal :** Avec un fond animé et des options claires (Play, Settings, Credits, Exit).
- 🥊 **Modes de Combat :** Choisissez entre 1 vs 2, 1 vs Computer, ou Computer vs Computer. Peu importe le mode, le choix du personnage est à vous !
- 🎶 **Paramètres :** Ajustez le son, la musique et les effets pour une expérience de jeu optimale.
- 👨‍💻 **Crédits :** Découvrez les cerveaux derrière ce projet incroyable.

![Features](https://img.shields.io/badge/FEATURES-Awesome-red)





## Instructions d'Installation

1. Clonez ce dépôt sur votre machine locale :
   ```sh
   git clone https://github.com/josephsamijona/INF2300_TP1_JOSEPH_Samuel_JONATHAN_Pierre.git

2. accédez au répertoire du projet : 
   ```sh
   cd INF2300_TP2_JOSEPH_Samuel_JONATHAN_Pierre

3. installez les dépendances requises : 
   ```sh
   pip install -r requirements.txt



4. lancez le jeu : 
   ```sh
   python main.py


## contact
nous sommes toujours ouverts aux questions, suggestions et messages d'encouragement (ou même de défis !) :

📧 [isteah.josephsamuel@gmail.com](mailto:isteah.josephsamuel@gmail.com) – joseph samuel jonathan  
📧 [isteah.jpierrelouis03@gmail.com](mailto:isteah.jpierrelouis03@gmail.com) – jonathan pierre louis

## informations du cours
- **📚 cours** : inf2300 infographie  
- **🗓 session** : été 2024  
- **📄 travail no.** : 2  
- **👥 groupe** :
  - joseph samuel jonathan
  - jonathan pierre louis
- **👩‍🏫 soumis à** : dre. franjieh el khoury  
- **📅 date** : 20 juin 2024

## remerciements
un immense merci à nos professeurs, collègues, amis, et bien sûr, à vous, pour votre intérêt et votre soutien. et souvenez-vous : coder, c'est comme combattre – il faut de la stratégie, de la détermination, et parfois, un bon café ! ☕👨‍💻👩‍💻

**merci d'avoir lu notre readme !** nous espérons que vous apprécierez jouer à notre jeu autant que nous avons aimé le créer. **que le code soit avec vous !** 🚀

![thank you](https://github.com/josephsamijona/INF2300_TP1_JOSEPH_Samuel_JONATHAN_Pierre/raw/main/game/assets/video/Sunrise_animation.mp4)


## Structure du Système de Fichiers

```plaintext

BladesOfHonor/
│
├── assets/
│   ├── audio/
│   │   ├── sword.wav
│   │   ├── magic.wav
│   ├── backgrounds/
│   │   ├── menu_background.png
│   │   ├── moon.png
│   ├── characters/
│   │   ├── warrior/
│   │   │   ├── Sprites/
│   │   │   │   ├── warrior.png
│   │   ├── wizard/
│   │   │   ├── Sprites/
│   │   │   │   ├── wizard.png
│   ├── fonts/
│   │   ├── Seagram tfb.ttf
│   ├── icons/
│   │   ├── victory.png
│   │   ├── defeat.png
│   ├── music/
│   │   ├── intro.mp3
│   │   ├── LEMMiNO - Cipher (BGM).mp3
│   ├── video/
│   │   ├── intro.mp4
│
├── src/
│   ├── game_logic/
│   │   ├── unvdeux/
│   │   │   ├── logic1v2.py
│   │   │   ├── mode_1_vs_2.py
│   │   ├── vcomputer/
│   │   │   ├── logic1vcom.py
│   │   │   ├── mode_1_vs_computer.py
│   │   ├── ai_vs_ai/
│   │   │   ├── logic_ai_vs_ai.py
│   │   │   ├── mode_ai_vs_ai.py
│   │   ├── three_d/
│   │   │   ├── mode_3d_adventure.py
│   │   │   ├── shaders/
│   │   │   │   ├── vertex_shader.glsl
│   │   │   │   ├── fragment_shader.glsl
│   ├── intro.py
│   ├── menu.py
│   ├── settings.py
│   ├── credits.py
│   ├── game_modes.py
│   ├── player.py
│   ├── npc.py
│
├── requirements.txt
├── README.md
└── main.py