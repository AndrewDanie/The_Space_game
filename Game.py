import pygame
import pygame_gui
from numpy import array, zeros

import Classes_and_Functions as CF
from Menu import Main_menu, Settings_menu


class Game:

    def __init__(self, resolution, FPS):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        
        pygame.init()

        self.F_mixer_running = True
        try:
            pygame.mixer.init()
        except:
            self.F_mixer_running = False
        finally:
            print('Sound mixer running is', self.F_mixer_running)
        self.F_running = True   # Флаг работы программы
        self.F_current_loop_running = True  # Флаг работы текущего цикл

        pygame.display.set_caption('SPACE GAME')  # Название окна
        self.resolution = array(resolution) # Разрешение экрана     # Array из Numpy для векторной работы
        self.window_center = self.resolution // 2
        print(self.window_center)
        self.window = pygame.display.set_mode(resolution)
        self.display = pygame.Surface(resolution)   # Главная отрисовываемая поверхность
        self.manager = pygame_gui.UIManager(resolution) # Запускаем GUI-менеджер
        self.clock = pygame.time.Clock()
        self.FPS = FPS

        self.Main_menu = Main_menu(self)  # Главное меню игры
        self.Setting_menu = Settings_menu(self)
        self.loop_set = {'game':self,
                         'Main_menu': self.Main_menu,
                         'Settings_menu': self.Setting_menu}
        self.current_loop = 'Main_menu'
        self.current_level_number = 1

    def run(self):
        """
        Цикл циклов!
        """
        while self.F_running:
            self.F_current_loop_running = True
            self.loop_set[self.current_loop].loop()
        pygame.quit()


    def loop(self):
        """
        Основной игровой цикл игры
        """
        print('This is a game loop')
        self.load_level(self.current_level_number)
        while self.F_current_loop_running:
            time_delta = self.clock.tick(60) / 1000.0
            self.check_events()
            self.manager.update(time_delta)
            self.display.fill('black')
            self.window.blit(self.display, (0, 0))
            self.manager.draw_ui(self.window)
            pygame.display.update()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.F_running = False
                self.F_current_loop_running = False

            self.manager.process_events(event)  # Обработка событий GUI

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   # Нажатие левой кнопки мыши
                    pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.F_current_loop_running = False
                    self.current_loop = 'Main_menu'

    def load_level(self, level):
        self.indent_cord = array([100, 150])  # Отступ рамки
        self.camera_cord = array([- self.resolution[0] // 2, - self.resolution[1] // 2])  # Начальное положение камеры

        '''Загрузка и инициализация звуков'''
        self.sound_ambient = CF.musicload('Ambient1.wav')
        pygame.mixer.music.set_volume(0.05)
        sound_of_engine = CF.mixerload('engine.wav')
        sound_of_engine.set_volume(0.01)

        '''Загрузка и инициализация изображений'''
        self.pic_frame = CF.imgload('Frame.png')
        self.pic_gear = CF.imgload('gear.png')
        self.pic_tank = CF.imgload('Tank.png')
        self.pic_gear = pygame.transform.rotozoom(self.pic_gear, 0, 0.2)
        self.pic_tank = pygame.transform.rotozoom(self.pic_tank, 0, 0.2)

        '''Загрузка первого уровня'''
        self.current_level = CF.Level(level)

        print('Level objects:')
        for obj in self.current_level.level_objects:
            print(obj.__dict__)
