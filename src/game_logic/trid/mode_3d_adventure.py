import os
import pygame as pg
import numpy as np
from numba import njit

class Game:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        pg.init()
        pg.mixer.init()

        (self.step, self.step2, self.swoosh, self.hurt, self.deadmonster, self.hitmonster,
         self.hitmonster2, self.healthup, self.died, self.won, self.music) = self.load_sounds()
        
        self.stepdelay = pg.time.get_ticks() / 200
        self.stepdelay2 = self.stepdelay
        
        self.screen = pg.display.set_mode((800, 600))
        self.running = True
        self.clock = pg.time.Clock()
        pg.mouse.set_visible(False)
        pg.event.set_grab(1)

        self.hres = 250  # horizontal resolution
        self.halfvres = int(self.hres * 0.375)  # vertical resolution/2
        self.mod = self.hres / 60  # scaling factor (60° fov)

        self.size = 25
        self.nenemies = self.size * 2  # number of enemies
        self.posx, self.posy, self.rot, self.maph, self.mapc, self.exitx, self.exity = self.gen_map(self.size)
        self.stepscount = self.posx + self.posy
        self.player_health = 10
        self.rotv = 0
        
        self.frame = np.random.uniform(0, 1, (self.hres, self.halfvres * 2, 3))
        self.sky = pg.image.load(self.get_asset_path('../game/assets/textures/skybox2.jpg'))
        self.sky = pg.surfarray.array3d(pg.transform.smoothscale(self.sky, (720, self.halfvres * 4))) / 255
        self.floor = pg.surfarray.array3d(pg.image.load(self.get_asset_path('../game/assets/textures/floor.jpg'))) / 255
        self.wall = pg.surfarray.array3d(pg.image.load(self.get_asset_path('../game/assets/textures/wall.jpg'))) / 255
        self.sprites, self.spsize, self.sword, self.swordsp = self.get_sprites(self.hres)
        
        self.enemies = self.spawn_enemies(self.nenemies, self.maph, self.size)

    def get_asset_path(self, relative_path):
        return os.path.join(self.root_dir, relative_path)

    def load_sounds(self):
        step = pg.mixer.Sound(self.get_asset_path('../game/assets/sounds/playerstep.mp3'))
        step2 = pg.mixer.Sound(self.get_asset_path('../game/assets/sounds/enemystep.mp3'))
        swoosh = pg.mixer.Sound(self.get_asset_path('../game/assets/sounds/sword.mp3'))
        hurt = pg.mixer.Sound(self.get_asset_path('../game/assets/sounds/damage.mp3'))
        deadmonster = pg.mixer.Sound(self.get_asset_path('../game/assets/sounds/deadmonster.mp3'))
        hitmonster = pg.mixer.Sound(self.get_asset_path('../game/assets/sounds/hitmonster.mp3'))
        hitmonster2 = pg.mixer.Sound(self.get_asset_path('../game/assets/sounds/hitmonster2.mp3'))
        healthup = pg.mixer.Sound(self.get_asset_path('../game/assets/sounds/healthup.wav'))
        died = pg.mixer.Sound(self.get_asset_path('../game/assets/sounds/died.wav'))
        won = pg.mixer.Sound(self.get_asset_path('../game/assets/sounds/won.wav'))
        music = pg.mixer.Sound(self.get_asset_path('../game/assets/sounds/battlemusic0.mp3'))
        music.set_volume(0.3)
        music.play(-1)
        won.play()

        return (step, step2, swoosh, hurt, deadmonster, hitmonster, hitmonster2,
                healthup, died, won, music)

    def run(self):
        while self.running:
            ticks = pg.time.get_ticks() / 200
            er = min(self.clock.tick() / 500, 0.3)
            if self.player_health < 0:
                print("You died")
                self.died.play()
                self.running = False
            if self.nenemies < self.size and int(self.posx) == self.exitx and int(self.posy) == self.exity:
                print("You got out of the maze!")
                self.won.play()
                self.running = False
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.running = False
                if self.swordsp < 1 and event.type == pg.MOUSEBUTTONDOWN:
                    self.swordsp = 1
                    
            self.frame = self.new_frame(self.posx, self.posy, self.rot, self.frame, self.sky, self.floor, self.hres, self.halfvres, self.mod, self.maph, self.size,
                                        self.wall, self.mapc, self.exitx, self.exity, self.nenemies, self.rotv)
            surf = pg.surfarray.make_surface(self.frame * 255)

            mape = np.zeros((self.size, self.size))
            health = self.player_health
            self.enemies, self.player_health, mape = self.enemies_ai(self.posx, self.posy, self.enemies, self.maph, self.size, mape, self.swordsp,
                                                                     ticks, self.player_health)
            self.enemies = self.sort_sprites(self.posx, self.posy, self.rot, self.enemies, self.maph, self.size, er / 3)
            
            surf, en = self.draw_sprites(surf, self.sprites, self.enemies, self.spsize, self.hres, self.halfvres, ticks, self.sword,
                                         self.swordsp, self.rotv)

            surf = pg.transform.scale(surf, (800, 600))

            self.screen.blit(surf, (0, 0))
            pg.display.update()

            if health > self.player_health:
                self.hurt.play()

            if ticks - self.stepdelay > 2 and self.stepscount != self.posx + self.posy:
                self.step.play()
                self.stepdelay = ticks
            self.stepscount = self.posx + self.posy
                
            if mape[int(self.posx)][int(self.posy)] > 0:
                delaycontrol = max(0.3, 2 / np.random.uniform(0.99, mape[int(self.posx)][int(self.posy)]))
                if ticks - self.stepdelay2 > delaycontrol:
                    self.step2.play()
                    self.stepdelay2 = ticks
            
            if int(self.swordsp) > 0:
                if self.swordsp == 1:
                    self.swoosh.play()
                    en_o = en        
                    while self.enemies[en][3] > 1.25 and self.enemies[en][3] < 10:
                        self.enemies[en][8] = self.enemies[en][8] - np.random.uniform(1, 4)
                        x = self.enemies[en][0] + 0.3 * np.cos(self.rot)
                        y = self.enemies[en][1] + 0.3 * np.sin(self.rot)
                        if self.maph[int(x)][int(y)] == 0:
                            self.enemies[en][0] = (x + self.enemies[en][0]) / 2  # push back
                            self.enemies[en][1] = (y + self.enemies[en][1]) / 2
                        if self.enemies[en][8] < 0:
                            self.deadmonster.play()
                            self.enemies[en][0] = 0
                            self.nenemies = self.nenemies - 1
                            if np.random.uniform(0, 1) < 0.5:
                                self.player_health = min(self.player_health + 0.5, 10)
                                self.healthup.play()                           
                        en = en - 1
                    if en != en_o:
                        if self.enemies[en_o][4]:
                            self.hitmonster2.play()
                        else:
                            self.hitmonster.play() 
                self.swordsp = (self.swordsp + er * 5) % 4

            fps = int(self.clock.get_fps())
            pg.display.set_caption(f"Health: {self.player_health} Enemies: {self.nenemies} FPS: {fps}")
            self.posx, self.posy, self.rot, self.rotv = self.movement(pg.key.get_pressed(), self.posx, self.posy, self.rot, self.maph, er, self.rotv)

        pg.mixer.fadeout(1000)
        pg.time.wait(1000)
        pg.mixer.quit()
        pg.quit()

    def movement(self, pressed_keys, posx, posy, rot, maph, et, rotv):
        x, y, rot0, diag = posx, posy, rot, 0
        if pg.mouse.get_focused():
            p_mouse = pg.mouse.get_rel()
            rot = rot + np.clip((p_mouse[0]) / 200, -0.2, .2)
            rotv = rotv + np.clip((p_mouse[1]) / 200, -0.2, .2)
            rotv = np.clip(rotv, -1, 1)

        if pressed_keys[pg.K_UP] or pressed_keys[ord('w')]:
            x, y, diag = x + et * np.cos(rot), y + et * np.sin(rot), 1

        elif pressed_keys[pg.K_DOWN] or pressed_keys[ord('s')]:
            x, y, diag = x - et * np.cos(rot), y - et * np.sin(rot), 1
            
        if pressed_keys[pg.K_LEFT] or pressed_keys[ord('a')]:
            et = et / (diag + 1)
            x, y = x + et * np.sin(rot), y - et * np.cos(rot)
            
        elif pressed_keys[pg.K_RIGHT] or pressed_keys[ord('d')]:
            et = et / (diag + 1)
            x, y = x - et * np.sin(rot), y + et * np.cos(rot)

        posx, posy = self.check_walls(posx, posy, maph, x, y)

        return posx, posy, rot, rotv

    def gen_map(self, size):
        return gen_map_njit(size)

    def new_frame(self, posx, posy, rot, frame, sky, floor, hres, halfvres, mod, maph, size, wall, mapc,
                  exitx, exity, nenemies, rotv):
        return new_frame_njit(posx, posy, rot, frame, sky, floor, hres, halfvres, mod, maph, size, wall, mapc,
                              exitx, exity, nenemies, rotv)

    def enemies_ai(self, posx, posy, enemies, maph, size, mape, swordsp, ticks, player_health):
        return enemies_ai_njit(posx, posy, enemies, maph, size, mape, swordsp, ticks, player_health)

    def check_walls(self, posx, posy, maph, x, y):
        return check_walls_njit(posx, posy, maph, x, y)

    def angle2p(self, posx, posy, enx, eny):
        return angle2p_njit(posx, posy, enx, eny)

    def sort_sprites(self, posx, posy, rot, enemies, maph, size, er):
        return sort_sprites_njit(posx, posy, rot, enemies, maph, size, er)

    def spawn_enemies(self, number, maph, msize):
        return spawn_enemies_njit(number, maph, msize)

    def get_sprites(self, hres):
        sheet = pg.image.load(self.get_asset_path('../game/assets/sprites/zombie_n_skeleton4.png')).convert_alpha()
        sprites = [[], []]
        swordsheet = pg.image.load(self.get_asset_path('../game/assets/sprites/sword1.png')).convert_alpha() 
        sword = []
        for i in range(3):
            subsword = pg.Surface.subsurface(swordsheet, (i * 800, 0, 800, 600))
            sword.append(pg.transform.smoothscale(subsword, (hres, int(hres * 0.75))))
            xx = i * 32
            sprites[0].append([])
            sprites[1].append([])
            for j in range(4):
                yy = j * 100
                sprites[0][i].append(pg.Surface.subsurface(sheet, (xx, yy, 32, 100)))
                sprites[1][i].append(pg.Surface.subsurface(sheet, (xx + 96, yy, 32, 100)))

        spsize = np.asarray(sprites[0][1][0].get_size()) * hres / 800

        sword.append(sword[1])  # extra middle frame
        swordsp = 0  # current sprite for the sword
        
        return sprites, spsize, sword, swordsp

    def draw_sprites(self, surf, sprites, enemies, spsize, hres, halfvres, ticks, sword, swordsp, rotv):
        offset = int(rotv * halfvres)
        cycle = int(ticks) % 3  # animation cycle for monsters
        for en in range(len(enemies)):
            if enemies[en][3] >  10:
                break
            types, dir2p = int(enemies[en][4]), int(enemies[en][7])
            cos2 = np.cos(enemies[en][2])
            scale = min(enemies[en][3], 2) * spsize * enemies[en][5] / cos2
            vert = halfvres + halfvres * min(enemies[en][3], 2) / cos2 - offset
            hor = hres / 2 - hres * np.sin(enemies[en][2])
            spsurf = pg.transform.scale(sprites[types][cycle][dir2p], scale)
            surf.blit(spsurf, (hor, vert) - scale / 2)

        swordpos = (np.sin(ticks) * 10 * hres / 800, (np.cos(ticks) * 10 + 15) * hres / 800)  # sword shake
        surf.blit(sword[int(swordsp)], swordpos)

        return surf, en - 1


@njit
def gen_map_njit(size):
    mapc = np.random.uniform(0, 1, (size, size, 3))
    maph = np.random.choice(np.array([0, 0, 0, 0, 1, 2]), (size, size))  # Utilisation d'un tableau numpy
    maph[0, :], maph[size - 1, :], maph[:, 0], maph[:, size - 1] = (1, 1, 1, 1)
    posx, posy = np.random.randint(1, size - 2) + 0.5, np.random.randint(1, size - 2) + 0.5
    rot = np.pi / 4
    x, y = int(posx), int(posy)
    maph[x][y] = 0
    count = 0
    while True:
        testx, testy = (x, y)
        if np.random.uniform() > 0.5:
            testx = testx + np.random.choice(np.array([-1, 1]))  # Utilisation d'un tableau numpy
        else:
            testy = testy + np.random.choice(np.array([-1, 1]))  # Utilisation d'un tableau numpy
        if testx > 0 and testx < size - 1 and testy > 0 and testy < size - 1:
            if maph[testx][testy] == 0 or count > 5:
                count = 0
                x, y = (testx, testy)
                maph[x][y] = 0
                dtx = np.sqrt((x - posx) ** 2 + (y - posy) ** 2)
                if (dtx > size * 0.6 and np.random.uniform() > 0.999) or np.random.uniform() > 0.99999:
                    exitx, exity = (x, y)
                    break
            else:
                count = count + 1
    return posx, posy, rot, maph, mapc, exitx, exity



@njit
def new_frame_njit(posx, posy, rot, frame, sky, floor, hres, halfvres, mod, maph, size, wall, mapc,
                   exitx, exity, nenemies, rotv):
    offset = -int(halfvres * rotv)
    for i in range(hres):
        rot_i = rot + np.deg2rad(i / mod - 30)
        sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i / mod - 30))
        frame[i][:] = sky[int(np.rad2deg(rot_i) * 2 % 718)][halfvres - offset:3 * halfvres - offset]

        x, y = posx, posy
        while maph[int(x) % (size - 1)][int(y) % (size - 1)] == 0:
            x, y = x + 0.01 * cos, y + 0.01 * sin

        n = np.sqrt((x - posx) ** 2 + (y - posy) ** 2)
        h = int(halfvres / (n * cos2 + 0.001))

        xx = int(x * 3 % 1 * 99)
        if x % 1 < 0.02 or x % 1 > 0.98:
            xx = int(y * 3 % 1 * 99)
        yy = np.linspace(0, 3, h * 2) * 99 % 99

        shade = 0.3 + 0.7 * (h / halfvres)
        if shade > 1:
            shade = 1

        ash = 0
        if maph[int(x - 0.33) % (size - 1)][int(y - 0.33) % (size - 1)] != 0:
            ash = 1

        if maph[int(x - 0.01) % (size - 1)][int(y - 0.01) % (size - 1)] != 0:
            shade, ash = shade * 0.6, 0

        c = shade * mapc[int(x) % (size - 1)][int(y) % (size - 1)]
        for k in range(h * 2):
            if halfvres - h + k + offset >= 0 and halfvres - h + k + offset < 2 * halfvres:
                if ash and 1 - k / (2 * h) < 1 - xx / 99:
                    c, ash = 0.6 * c, 0
                frame[i][halfvres - h + k + offset] = c * wall[xx][int(yy[k])]
            if halfvres + 3 * h - k + offset - 1 < halfvres * 2:
                frame[i][halfvres + 3 * h - k + offset - 1] = c * wall[xx][int(yy[k])]

        for j in range(halfvres - h - offset):
            n = (halfvres / (halfvres - j - offset)) / cos2
            x, y = posx + cos * n, posy + sin * n
            xx, yy = int(x * 3 % 1 * 99), int(y * 3 % 1 * 99)

            shade = min(0.2 + 0.8 / n, 1)
            if maph[int(x - 0.33) % (size - 1)][int(y - 0.33) % (size - 1)] != 0:
                shade = shade * 0.6
            elif ((maph[int(x - 0.33) % (size - 1)][int(y) % (size - 1)] and y % 1 > x % 1) or
                  (maph[int(x) % (size - 1)][int(y - 0.33) % (size - 1)] and x % 1 > y % 1)):
                shade = shade * 0.6

            frame[i][halfvres * 2 - j - 1] = shade * (floor[xx][yy] * 2 + frame[i][halfvres * 2 - j - 1]) / 3

            if nenemies < size and int(x) == exitx and int(y) == exity and (x % 1 - 0.5) ** 2 + (y % 1 - 0.5) ** 2 < 0.2:
                ee = j / (10 * halfvres)
                frame[i][j:2 * halfvres - j] = (ee * np.ones(3) + frame[i][j:2 * halfvres - j]) / (1 + ee)

    return frame


@njit
def enemies_ai_njit(posx, posy, enemies, maph, size, mape, swordsp, ticks, player_health):
    for en in range(len(enemies)):
        if enemies[en][8] > 0:
            x, y = int(enemies[en][0]), int(enemies[en][1])
            mape[x - 1:x + 2, y - 1:y + 2] = mape[x - 1:x + 2, y - 1:y + 2] + 1

    for en in range(len(enemies)):
        if enemies[en][8] > 0 and np.random.uniform(0, 1) < 0.1:
            enx, eny, angle = enemies[en][0], enemies[en][1], enemies[en][6]
            health, state, cooldown = enemies[en][8], enemies[en][9], enemies[en][10]
            dist2p = np.sqrt((enx - posx) ** 2 + (eny - posy) ** 2 + 1e-16)

            friends = mape[int(enx)][int(eny)] - 1
            if dist2p > 1.42:
                friends = friends + mape[int(posx)][int(posy)]

            not_afraid = 0
            if health > 1 + enemies[en][4] or health + friends > 3 + enemies[en][4]:
                not_afraid = 1

            if state == 0 and dist2p < 6:
                angle = angle2p_njit(enx, eny, posx, posy)
                angle2 = (enemies[en][6] - angle) % (2 * np.pi)
                if angle2 > 11 * np.pi / 6 or angle2 < np.pi / 6 or (swordsp >= 1 and dist2p < 3):
                    if vision_njit(posx, posy, enx, eny, dist2p, maph, size):
                        if not_afraid:
                            state = 1
                        else:
                            state = 2
                            angle = angle - np.pi
                    else:
                        angle = enemies[en][6]

            elif state == 1:
                if dist2p < 0.6 and ticks - cooldown > 10:
                    enemies[en][10] = ticks
                    player_health = player_health - np.random.uniform(0, 1) / np.sqrt(1 + mape[int(posx)][int(posy)])
                if not_afraid:
                    angle = angle2p_njit(enx, eny, posx, posy)
                else:
                    state = 2

            elif state == 2:
                if not_afraid:
                    state = 0
                else:
                    angle = angle2p_njit(posx, posy, enx, eny) + np.random.uniform(-0.5, 0.5)

            enemies[en][6], enemies[en][9] = angle + np.random.uniform(-0.2, 0.2), state

    return enemies, player_health, mape


@njit
def check_walls_njit(posx, posy, maph, x, y):
    if not (maph[int(x - 0.1)][int(y)] or maph[int(x + 0.1)][int(y)] or
            maph[int(x)][int(y - 0.1)] or maph[int(x)][int(y + 0.1)]):
        posx, posy = x, y

    elif not (maph[int(posx - 0.1)][int(y)] or maph[int(posx + 0.1)][int(y)] or
              maph[int(posx)][int(y - 0.1)] or maph[int(posx)][int(y + 0.1)]):
        posy = y

    elif not (maph[int(x - 0.1)][int(posy)] or maph[int(x + 0.1)][int(posy)] or
              maph[int(x)][int(posy - 0.1)] or maph[int(x)][int(posy + 0.1)]):
        posx = x

    return posx, posy


@njit
def angle2p_njit(posx, posy, enx, eny):
    angle = np.arctan((eny - posy) / (enx - posx))
    if abs(posx + np.cos(angle) - enx) > abs(posx - enx):
        angle = (angle - np.pi) % (2 * np.pi)
    return angle


@njit
def sort_sprites_njit(posx, posy, rot, enemies, maph, size, er):
    for en in range(len(enemies)):
        enemies[en][3] = 9999
        if enemies[en][8] > 0:
            enx, eny = enemies[en][0], enemies[en][1]
            speed = er * (1 + enemies[en][9] / 2)
            cos, sin = speed * np.cos(enemies[en][6]), speed * np.sin(enemies[en][6])
            x, y = enx + cos, eny + sin
            enx, eny = check_walls_njit(enx, eny, maph, x, y)
            if enx == enemies[en][0] or eny == enemies[en][1]:
                enemies[en][6] = enemies[en][6] + np.random.uniform(-0.5, 0.5)
                if np.random.uniform(0, 1) < 0.01:
                    enemies[en][9] = 0
            enemies[en][0], enemies[en][1] = enx, eny

            angle = angle2p_njit(posx, posy, enx, eny)
            angle2 = (rot - angle) % (2 * np.pi)
            if angle2 > 10.5 * np.pi / 6 or angle2 < 1.5 * np.pi / 6:
                dir2p = ((enemies[en][6] - angle - 3 * np.pi / 4) % (2 * np.pi)) / (np.pi / 2)
                dist2p = np.sqrt((enx - posx) ** 2 + (eny - posy) ** 2 + 1e-16)
                enemies[en][2] = angle2
                enemies[en][7] = dir2p
                if vision_njit(posx, posy, enx, eny, dist2p, maph, size):
                    enemies[en][3] = 1 / dist2p

    enemies = enemies[enemies[:, 3].argsort()]
    return enemies


@njit
def vision_njit(posx, posy, enx, eny, dist2p, maph, size):
    cos, sin = (posx - enx) / dist2p, (posy - eny) / dist2p
    x, y = enx, eny
    seen = 1
    for i in range(int(dist2p / 0.05)):
        x, y = x + 0.05 * cos, y + 0.05 * sin
        if (maph[int(x - 0.02) % (size - 1)][int(y - 0.02) % (size - 1)] or
                maph[int(x - 0.02) % (size - 1)][int(y + 0.02) % (size - 1)] or
                maph[int(x + 0.02) % (size - 1)][int(y - 0.02) % (size - 1)] or
                maph[int(x + 0.02) % (size - 1)][int(y + 0.02) % (size - 1)]):
            seen = 0
            break
    return seen


@njit
def spawn_enemies_njit(number, maph, msize):
    enemies = []
    for i in range(number):
        x, y = np.random.uniform(1, msize - 2), np.random.uniform(1, msize - 2)
        while (maph[int(x - 0.1) % (msize - 1)][int(y - 0.1) % (msize - 1)] or
               maph[int(x - 0.1) % (msize - 1)][int(y + 0.1) % (msize - 1)] or
               maph[int(x + 0.1) % (msize - 1)][int(y - 0.1) % (msize - 1)] or
               maph[int(x + 0.1) % (msize - 1)][int(y + 0.1) % (msize - 1)]):
            x, y = np.random.uniform(1, msize - 1), np.random.uniform(1, msize - 1)
        angle2p, invdist2p, dir2p = 0, 1, 0
        entype = np.random.choice(np.array([0, 1]))  # Utilisation d'un tableau numpy
        direction = np.random.uniform(0, 2 * np.pi)
        size = np.random.uniform(7, 10)
        health = size / 2
        state = 0
        cooldown = 0
        enemies.append([x, y, angle2p, invdist2p, entype, size, direction, dir2p, health, state, cooldown])
    return np.asarray(enemies)



if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath(__file__))
    game = Game(root_dir)
    game.run()
