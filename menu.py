from init import *
from abstract_menu import Menu
from game_process import Game_process


class Game(Menu):

    def loop(self):
        print(f'This is a {self.__class__}')
        self.game_process = Game_process()
        self.F_pause = False
        while self.F_current_loop_running:
            time_delta = clock.tick(FPS) / 1000.0
            self.check_events()
            if not(self.F_pause):
                self.game_process.logic.do_tick_logic()
            self.draw_screen()
            manager.update(time_delta)

    def check_events(self):
        self.game_process.camera.check_events()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.change_menu()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.new_loop = Main()
                    self.change_menu()
                if event.key == pygame.K_SPACE:
                    self.F_pause = not(self.F_pause)
                    print(f'Pause is {self.F_pause}')
            self.game_process.logic.check_events(event)
            self.game_process.camera.check_events(event)
            manager.process_events(event)  # Обработка событий GUI

    def draw_screen(self):
        self.__draw_background()
        self.game_process.camera.draw_level_objects()
        self.__draw_static_pics()
        manager.draw_ui(window)
        pygame.display.update()

    def __draw_background(self):
        self.__draw_object(self.game_process.pic_background, window_center)

    def __draw_static_pics(self):
        self.__draw_object(self.game_process.pic_frame, window_center)
        self.__draw_object(self.game_process.pic_gear, resolution)
        self.__draw_object(self.game_process.pic_tank, (35, resolution[1]-115))

    def __draw_object(self, obj, pos: tuple):
        obj.rect = obj.image.get_rect(center=pos)
        window.blit(obj.image, obj.rect)


class Main(Menu):

    def make_elements(self):
        top = window_center[1] - 100
        left = window_center[0] - 70
        self.start_game_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (left, top), (140, 50)),
                 text='Начать игру',
                 manager=manager)
        self.settings_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (left, top + 70), (140, 50)),
                 text='Настройки',
                 manager=manager)
        self.quit_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (left, top + 140), (140, 50)),
                 text='Выход',
                 manager=manager)

    def kill_elements(self):
        self.start_game_button.kill()
        self.quit_button.kill()
        self.settings_button.kill()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                self.change_menu()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_game_button:
                    self.new_loop = Game()
                    self.change_menu()


                if event.ui_element == self.settings_button:
                    self.new_loop = Settings()
                    self.change_menu()


                if event.ui_element == self.quit_button:
                    self.change_menu()

            manager.process_events(event)  # Обработка событий GUI


class Settings(Menu):

    def make_elements(self):
        top = window_center[1] - 100
        left = window_center[0] - 70
        self.volume_settings_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (left, top), (140, 50)),
                 text='Звук',
                 manager=manager)
        self.graphic_settings_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (left, top + 70), (140, 50)),
                 text='Графика',
                 manager=manager)
        self.back_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (left, top + 140), (140, 50)),
                 text='Назад',
                 manager=manager)

    def kill_elements(self):
        self.volume_settings_button.kill()
        self.graphic_settings_button.kill()
        self.back_button.kill()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.change_menu()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.volume_settings_button:
                    self.new_loop = Volume_settings()
                    self.change_menu()

                if event.ui_element == self.graphic_settings_button:
                    # self.new_loop = Graphic_settings(self.game)
                    self.change_menu()

                if event.ui_element == self.back_button:
                    self.new_loop = Main()
                    self.change_menu()

            manager.process_events(event)


class Volume_settings(Menu):

    def make_elements(self):
        from config import mixer_volume

        top = window_center[1] - 100
        left = window_center[0] - 100
        self.volume_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(
                    (left - 160, top + 70), (140, 30)),
                html_text='Общая громкость',
                manager=manager)
        self.volume_slider = pygame_gui.elements.UIHorizontalSlider(
                relative_rect=pygame.Rect(
                    (left, top + 70), (200, 30)),
                 start_value=mixer_volume,
                 value_range=(0, 1),
                 manager=manager)
        self.volume_amount_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(
                    (left + 220, top + 70), (40, 30)),
                html_text=f'{int(pygame.mixer.music.get_volume()*100)}',
                manager=manager)
        self.back_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (left + 30, top + 140), (140, 50)),
                text='Назад',
                manager=manager)

    def kill_elements(self):
        self.volume_text.kill()
        self.volume_slider.kill()
        self.volume_amount_text.kill()
        self.back_button.kill()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.change_menu()

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                pygame.mixer.music.set_volume(event.value)
                self.volume_amount_text.set_text(f'{int(pygame.mixer.music.get_volume()*100)}')

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.back_button:
                    self.new_loop = Settings()
                    self.change_menu()

            manager.process_events(event)
