import pygame
import random

class Fighter:
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0:idle, 1:run, 2:jump, 3:attack, 4:hit, 5:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100
        self.alive = True
        self.sound = sound

    def load_images(self, sprite_sheet, animation_steps):
        # Charger les images à partir de la feuille de sprites
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # Ne peut pas bouger pendant l'attaque
        if self.attacking == False and self.alive == True and round_over == False:
            # Logique de l'IA pour les deux combattants
            if self.rect.centerx < target.rect.centerx:
                dx = SPEED
                self.running = True
            elif self.rect.centerx > target.rect.centerx:
                dx = -SPEED
                self.running = True

            # Déterminer l'attaque de l'IA
            if abs(self.rect.centerx - target.rect.centerx) < 100:
                self.attack(surface, target)
                self.attack_type = 1

            # Faire sauter l'IA de temps en temps
            if self.jump == False and random.randint(0, 100) < 5:
                self.vel_y = -30
                self.jump = True

        # Appliquer la gravité
        self.vel_y += GRAVITY
        dy += self.vel_y

        # S'assurer que le combattant reste dans les limites de l'écran
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # Mettre à jour la position du rectangle
        self.rect.x += dx
        self.rect.y += dy

        # Mettre à jour l'image du combattant
        self.update()

    def update(self):
        # Vérifier l'action en cours
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(5)  # Mort
        elif self.attacking == True:
            self.update_action(3)  # Attaque
        elif self.jump == True:
            self.update_action(2)  # Saut
        elif self.running == True:
            self.update_action(1)  # Courir
        else:
            self.update_action(0)  # Inactif

        animation_cooldown = 50
        # Mettre à jour l'image
        self.image = self.animation_list[self.action][self.frame_index]
        # Vérifier si assez de temps s'est écoulé depuis la dernière mise à jour
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # Vérifier si l'animation est terminée
        if self.frame_index >= len(self.animation_list[self.action]):
            # Si le combattant est mort, terminer l'animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # Vérifier si une attaque a été exécutée
                if self.action == 3:
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, surface, target):
        if self.attacking == False:
            self.attacking = True
            self.sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.update_action(4)
        self.update()

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
