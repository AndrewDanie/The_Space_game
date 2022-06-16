import pygame
import pygame_gui


import Menu
from Game_loop import Game_loop
from config import settings


class Game:

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        self.init_main_audio()
        self.init_main_graphic()
        self.init_menus()

    def init_main_audio(self):
        self.F_mixer_running = True
        try:
            pygame.mixer.init()
        except:
            self.F_mixer_running = False
        finally:
            print('Sound mixer running is', self.F_mixer_running)
        pygame.mixer.music.set_volume(settings['mixer_volume'])

    def init_main_graphic(self):
        pygame.display.set_caption('SPACE GAME')  # Название окна
        res_x, res_y = settings['resolution_x'], settings['resolution_y']
        self.resolution = (res_x, res_y)
        self.window_center = (res_x // 2, res_y // 2)
        self.window = pygame.display.set_mode(self.resolution)
        self.display = pygame.Surface(self.resolution)   # Главная отрисовываемая поверхность
        self.manager = pygame_gui.UIManager(self.resolution) # Запускаем GUI-менеджер
        self.clock = pygame.time.Clock()
        self.FPS = settings['FPS']

    def init_menus(self):
        self.Main_menu = Menu.Main_menu(self)
        self.Game_loop = Game_loop(self)
        self.Setting_menu = Menu.Settings_menu(self)
        self.Volume_settings = Menu.Volume_settings(self)
        self.loop_set = {'Game':self.Game_loop,
                         'Main_menu': self.Main_menu,
                         'Settings_menu': self.Setting_menu,
                         'Volume_settings': self.Volume_settings}
        self.current_loop = 'Main_menu'

    def run(self):
        self.F_running = True   # Флаг работы программы
        self.F_current_loop_running = True  # Флаг работы текущего цикла

        while self.F_running:
            self.F_current_loop_running = True
            self.loop_set[self.current_loop].loop()
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()