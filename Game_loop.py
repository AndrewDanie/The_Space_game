import pygame
import pygame_gui
import os
from numpy import array, zeros

from Menu import Menu
import Classes_and_Functions as CF


class Game_loop(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
        self.current_level_number = 1

    def loop(self):
        print(f'This is a {self.__class__}')
        self.INIT_GAME_PROCESS()

        while self.game.F_current_loop_running:
            time_delta = self.game.clock.tick(60) / 1000.0
            self.check_events()
            self.game.manager.update(time_delta)
            self.draw_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_the_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.change_menu('Main_menu')

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
        self.current_level = CF.Level(self.current_level_number)
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
    return pygame.image.load(os.path.join('image', filename)).convert()