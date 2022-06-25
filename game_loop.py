import pygame
import pygame_gui
import os
from numpy import array, zeros

from menu import Menu
from level import Level
from camera import Camera
from  game_logic import Game_logic

class Game_loop(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
        self.current_level_number = 1
        self.window = self.game.window

    def loop(self):
        print(f'This is a {self.__class__}')
        self.INIT_GAME_PROCESS()
        self.camera = Camera(self.game)
        self.logic = Game_logic(self.current_level.level_objects)

        while self.game.F_current_loop_running:
            time_delta = self.game.clock.tick(60) / 1000.0
            self.check_events()
            self.logic.do_tick_logic()
            self.game.manager.update(time_delta)
            self.draw_screen()

    def draw_screen(self):
        self.game.window.fill('black')
        self.camera.draw_level_objects()
        self.game.manager.draw_ui(self.game.window)
        pygame.display.update()

    def check_events(self):
        self.camera.check_events()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_the_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.change_menu('Main_menu')

            self.logic.check_events(event)
            self.camera.check_events(event)
            self.game.manager.process_events(event)  # Обработка событий GUI

    def INIT_GAME_PROCESS(self):
        self.INIT_GAME_AUDIO()
        self.INIT_GAME_GRAPHIC()
        self.LOAD_CURRENT_LEVEL()

    def INIT_GAME_AUDIO(self):
        self.sound_ambient = musicload('Ambient1.wav')
        self.sound_of_engine = mixerload('engine.wav')
        self.sound_of_engine.set_volume(0.01)

    def INIT_GAME_GRAPHIC(self):
        self.resolution = array(self.game.resolution)
        self.indent_cord = array([100, 150])  # Отступ рамки
        self.camera_cord = array([- self.resolution[0] // 2, - self.resolution[1] // 2])  # Начальное положение камеры

        self.pic_frame = imgload('Frame.png')
        self.pic_gear = imgload('gear.png')
        self.pic_tank = imgload('Tank.png')
        self.pic_gear = pygame.transform.rotozoom(self.pic_gear, 0, 0.2)
        self.pic_tank = pygame.transform.rotozoom(self.pic_tank, 0, 0.2)

    def LOAD_CURRENT_LEVEL(self):
        self.current_level = Level(self.current_level_number)
        print('Level objects:')
        for obj in self.current_level.level_objects:
            print(obj.__dict__)


def musicload(filename):
    music = pygame.mixer.music.load(os.path.join('sounds', filename))
    pygame.mixer.music.play(-1)
    return music


def mixerload(filename):
    return pygame.mixer.Sound(os.path.join('sounds', filename))
# Разобраться с разницей между musicload и mixerload


def imgload(filename):
    return pygame.image.load(os.path.join('image', filename)).convert_alpha()