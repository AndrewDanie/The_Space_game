import pygame
import pygame_gui
import os
from numpy import array, zeros

import level
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
        self.__INIT_GAME_PROCESS()
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
        self.__draw_background()
        self.camera.draw_level_objects()
        self.__draw_static_pics()
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

    def __INIT_GAME_PROCESS(self):
        self.__LOAD_GAME_AUDIO()
        self.__LOAD_GAME_GRAPHIC()
        self.__LOAD_CURRENT_LEVEL()

    def __LOAD_GAME_AUDIO(self):
        self.sound_ambient = mixerload('Ambient1.wav')
        self.sound_of_engine = mixerload('engine.wav')
        self.sound_of_engine.set_volume(0.01)

    def __LOAD_GAME_GRAPHIC(self):
        self.resolution = array(self.game.resolution)
        self.indent_cord = array([100, 150])  # Отступ рамки
        self.camera_cord = array([- self.resolution[0] // 2, - self.resolution[1] // 2])  # Начальное положение камеры

        self.pic_frame = level.Static_object('Frame.png')
        self.pic_gear = level.Static_object('gear.png')
        self.pic_tank = level.Static_object('Tank.png')
        self.pic_background = level.Static_object('field_1.jpg')
        self.pic_gear.image = pygame.transform.rotozoom(self.pic_gear.image, 0, 0.4)
        self.pic_tank.image = pygame.transform.rotozoom(self.pic_tank.image, 0, 0.2)

    def __LOAD_CURRENT_LEVEL(self):
        self.current_level = Level(self.current_level_number)
        print('Level objects:')
        for obj in self.current_level.level_objects:
            print(obj.__dict__)

    def __draw_background(self):
        self.__draw_object(self.pic_background, self.game.window_center)

    def __draw_static_pics(self):
        self.__draw_object(self.pic_frame, self.game.window_center)
        self.__draw_object(self.pic_gear, self.game.resolution)
        self.__draw_object(self.pic_tank, (35, self.game.resolution[1]-115))

    def __draw_object(self, obj, pos: tuple):
        obj.rect = obj.image.get_rect(center=pos)
        self.window.blit(obj.image, obj.rect)


def musicload(filename):
    music = pygame.mixer.music.load(os.path.join('sounds', filename))
    pygame.mixer.music.play(-1)
    return music


def mixerload(filename):
    return pygame.mixer.Sound(os.path.join('sounds', filename))
# Разобраться с разницей между musicload и mixerload


def imgload(filename):
    return pygame.image.load(os.path.join('image', filename)).convert_alpha()