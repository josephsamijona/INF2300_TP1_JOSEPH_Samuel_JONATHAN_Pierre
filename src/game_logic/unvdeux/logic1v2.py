import pygame
# Ce code est destiné au mode de jeu 1 vs 2, où un joueur combat  son adversaire. 
# Son but est d'établir la logique de jeu en gérant les déplacements, les attaques, les animations, 
# et les interactions des combattants sur le terrain.
class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        # Initialisation des attributs du combattant
        self.player = player  # Identifiant du joueur (1 ou 2)
        self.size = data[0]  # Taille de chaque sprite dans le sprite sheet
        self.image_scale = data[1]  # Échelle de l'image
        self.offset = data[2]  # Décalage pour centrer l'image
        self.flip = flip  # Indique si l'image doit être retournée horizontalement
        self.animation_list = self.load_images(sprite_sheet, animation_steps)  # Chargement des animations
        self.action = 0  # Action actuelle du combattant (0: idle, 1: run, etc.)
        self.frame_index = 0  # Index de la frame actuelle dans l'animation
        self.image = self.animation_list[self.action][self.frame_index]  # Image actuelle à afficher
        self.update_time = pygame.time.get_ticks()  # Temps de la dernière mise à jour de l'image
        self.rect = pygame.Rect((x, y, 80, 180))  # Rectangle de collision pour le combattant
        self.vel_y = 0  # Vitesse verticale (pour les sauts et la gravité)
        self.running = False  # Indique si le combattant court
        self.jump = False  # Indique si le combattant saute
        self.attacking = False  # Indique si le combattant attaque
        self.attack_type = 0  # Type d'attaque (1 ou 2)
        self.attack_cooldown = 0  # Cooldown entre les attaques
        self.attack_sound = sound  # Son joué lors de l'attaque
        self.hit = False  # Indique si le combattant a été touché
        self.health = 100  # Santé du combattant
        self.alive = True  # Indique si le combattant est en vie

    def load_images(self, sprite_sheet, animation_steps):
        # Charger les images à partir du sprite sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10  # Vitesse de déplacement
        GRAVITY = 2  # Gravité appliquée au combattant
        dx = 0  # Déplacement horizontal
        dy = 0  # Déplacement vertical
        self.running = False  # Réinitialisation de l'état de course
        self.attack_type = 0  # Réinitialisation du type d'attaque

        # Récupérer les touches pressées
        key = pygame.key.get_pressed()

        # Ne peut effectuer d'autres actions que si le combattant n'est pas en train d'attaquer
        if not self.attacking and self.alive and not round_over:
            # Contrôles du joueur 1
            if self.player == 1:
                # Déplacement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                # Saut
                if key[pygame.K_w] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                # Attaque
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    # Déterminer le type d'attaque utilisé
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

            # Contrôles du joueur 2
            if self.player == 2:
                # Déplacement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                # Saut
                if key[pygame.K_UP] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                # Attaque
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    # Déterminer le type d'attaque utilisé
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

        # Appliquer la gravité
        self.vel_y += GRAVITY
        dy += self.vel_y

        # S'assurer que le joueur reste à l'écran
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # S'assurer que les joueurs se font face
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # Appliquer le cooldown des attaques
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Mettre à jour la position du joueur
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        # Vérifier l'action que le joueur est en train de faire
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # 6: death
        elif self.hit:
            self.update_action(5)  # 5: hit
        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(3)  # 3: attack1
            elif self.attack_type == 2:
                self.update_action(4)  # 4: attack2
        elif self.jump:
            self.update_action(2)  # 2: jump
        elif self.running:
            self.update_action(1)  # 1: run
        else:
            self.update_action(0)  # 0: idle

        animation_cooldown = 50  # Délai entre les frames de l'animation
        # Mettre à jour l'image
        self.image = self.animation_list[self.action][self.frame_index]
        # Vérifier si assez de temps s'est écoulé depuis la dernière mise à jour
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # Vérifier si l'animation est terminée
        if self.frame_index >= len(self.animation_list[self.action]):
            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, target):
        if self.attack_cooldown == 0:
            # Exécuter l'attaque
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True

    def update_action(self, new_action):
        # Vérifier si la nouvelle action est différente de la précédente
        if new_action != self.action:
            self.action = new_action
            # Mettre à jour les paramètres de l'animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        # Dessiner le combattant sur la surface donnée
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
