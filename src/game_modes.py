import pygame
import os
import cv2
from src.game_logic.unvdeux.mode_1_vs_2 import Game1vs2
from src.game_logic.vcomputer.mode_1_vs_computer import Game1vsc
from src.game_logic.aivai.mode_ai_vs_ai import Gameaivai
from src.game_logic.trid.mode_3d_adventure import Game
from src.game_logic.pendulu.pend import GamePendulum
from src.game_logic.life.lifu import GameLife
from src.game_logic.cube.patron import GameCube3D

class Button:
    def __init__(self, text, font, color, x, y, width, height):
        self.text = text
        self.font = font
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False
        self.original_size = (width, height)
        self.hovered_size = (int(width * 1.1), int(height * 1.1))

    def draw(self, screen):
        if self.hovered:
            button_rect = pygame.Rect(self.rect.x, self.rect.y, *self.hovered_size)
            button_rect.center = self.rect.center
            pygame.draw.rect(screen, (255, 255, 255), button_rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

def show_animation_modes(screen, root_dir):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)  # Aller au niveau supérieur pour accéder à assets
    video_path = os.path.join(project_root, "game","assets", "video", "3_background.mp4")
    click_sound_path = os.path.join(project_root,"game",  "assets", "sfx", "click.wav")
    hover_sound_path = os.path.join(project_root, "game", "assets", "sfx", "hover.wav")

    cap = cv2.VideoCapture(video_path)

    sound_path = os.path.join(project_root, "game", "assets", "music", "LEMMiNO - Cipher (BGM).mp3")
    pygame.mixer.init()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)

    click_sound = pygame.mixer.Sound(click_sound_path)
    hover_sound = pygame.mixer.Sound(hover_sound_path)

    animation_mode_items = ["Life", "Pendule", "Cube 3D", "Retour"]
    selected_item = 0

    font_path = os.path.join(project_root, "game", "assets", "fonts", "Seagram tfb.ttf")
    font = pygame.font.Font(font_path, 50)
    title_font = pygame.font.Font(font_path, 80)

    clock = pygame.time.Clock()

    hover_states = {item: False for item in animation_mode_items}

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if selected_item == 0:
                        print("Life sélectionné")
                        game = GameLife(root_dir)
                        game.run()
                    elif selected_item == 1:
                        print("Pendule sélectionné")
                        game = GamePendulum(root_dir)
                        game.run()
                    elif selected_item == 2:
                        print("Cube 3D sélectionné")
                        game = GameCube3D(root_dir)
                        game.run()
                    elif selected_item == 3:
                        return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.hovered:
                        click_sound.play()
                        if i == 0:
                            print("Life sélectionné")
                            game = GameLife(root_dir)
                            game.run()
                        elif i == 1:
                            print("Pendule sélectionné")
                            game = GamePendulum(root_dir)
                            game.run()
                        elif i == 2:
                            print("Cube 3D sélectionné")
                            game = GameCube3D(root_dir)
                            game.run()
                        elif i == 3:
                            return

        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (screen.get_width(), screen.get_height()))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))

        title_text = title_font.render("Animation Modes", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() / 2, 100))
        screen.blit(title_text, title_rect)

        buttons = []
        button_width = screen.get_width() // 3
        button_height = screen.get_height() // 12
        button_x = (screen.get_width() - button_width) // 2
        button_y_start = screen.get_height() // 3
        button_y_padding = screen.get_height() // 10

        for i, item in enumerate(animation_mode_items):
            button_y = button_y_start + i * button_y_padding
            button = Button(item, font, (200, 200, 200), button_x, button_y, button_width, button_height)
            button.check_hover(mouse_pos)
            if button.hovered and not hover_states[item]:
                hover_sound.play()
                hover_states[item] = True
            elif not button.hovered:
                hover_states[item] = False
            button.draw(screen)
            buttons.append(button)

        pygame.display.flip()
        clock.tick(30)

def show_game_modes(screen, root_dir):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)  # Aller au niveau supérieur pour accéder à assets
    video_path = os.path.join(project_root, "game","assets", "video", "3_background.mp4")

    cap = cv2.VideoCapture(video_path)
    
    click_sound_path = os.path.join(project_root,"game", "assets", "sfx", "click.wav")
    hover_sound_path = os.path.join(project_root, "game","assets", "sfx", "hover.wav")
    
    click_sound = pygame.mixer.Sound(click_sound_path)
    hover_sound = pygame.mixer.Sound(hover_sound_path)
    
    sound_path = os.path.join(project_root, "game", "assets", "music", "LEMMiNO - Cipher (BGM).mp3")
    pygame.mixer.init()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)

    game_mode_items = ["1 vs Computer", "1 vs 2", "AI vs AI", "3D Adventure", "Animation Mode", "Retour"]
    selected_item = 0

    font_path = os.path.join(project_root, "game", "assets", "fonts", "Seagram tfb.ttf")
    font = pygame.font.Font(font_path, 50)
    title_font = pygame.font.Font(font_path, 80)

    clock = pygame.time.Clock()

    hover_states = {item: False for item in game_mode_items}

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if selected_item == 0:
                        print("1 vs Computer sélectionné")
                        game = Game1vsc(root_dir)
                        game.run()
                    elif selected_item == 1:
                        print("1 vs 2 sélectionné")
                        game = Game1vs2(root_dir)
                        game.run()
                    elif selected_item == 2:
                        print("AI vs AI sélectionné")
                        game = Gameaivai(root_dir)
                        game.run()
                    elif selected_item == 3:
                        print("3D Adventure sélectionné")
                        pygame.mixer.music.stop()
                        game = Game(root_dir)
                        game.run()
                    elif selected_item == 4:
                        print("Animation Mode sélectionné")
                        show_animation_modes(screen, root_dir)
                    elif selected_item == 5:
                        return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.hovered:
                        click_sound.play()
                        if i == 0:
                            print("1 vs Computer sélectionné")
                            game = Game1vsc(root_dir)
                            game.run()
                        elif i == 1:
                            print("1 vs 2 sélectionné")
                            game = Game1vs2(root_dir)
                            game.run()
                        elif i == 2:
                            print("AI vs AI sélectionné")
                            game = Gameaivai(root_dir)
                            game.run()
                        elif i == 3:
                            print("3D Adventure sélectionné")
                            pygame.mixer.music.stop()
                            game = Game(root_dir)
                            game.run()
                        elif i == 4:
                            print("Animation Mode sélectionné")
                            show_animation_modes(screen, root_dir)
                        elif i == 5:
                            return

        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (screen.get_width(), screen.get_height()))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))

        title_text = title_font.render("Modes de Jeu", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() / 2, 100))
        screen.blit(title_text, title_rect)

        buttons = []
        button_width = screen.get_width() // 3
        button_height = screen.get_height() // 12
        button_x = (screen.get_width() - button_width) // 2
        button_y_start = screen.get_height() // 3
        button_y_padding = screen.get_height() // 10

        for i, item in enumerate(game_mode_items):
            button_y = button_y_start + i * button_y_padding
            button = Button(item, font, (200, 200, 200), button_x, button_y, button_width, button_height)
            button.check_hover(mouse_pos)
            if button.hovered and not hover_states[item]:
                hover_sound.play()
                hover_states[item] = True
            elif not button.hovered:
                hover_states[item] = False
            button.draw(screen)
            buttons.append(button)

        pygame.display.flip()
        clock.tick(30)

    cap.release()
    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "game","assets", "music", "LEMMiNO - Cipher (BGM).mp3")
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play(-1)

    show_game_modes(screen, os.path.dirname(os.path.abspath(__file__)))
    pygame.quit()
