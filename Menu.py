import pygame
import pygame_gui


class Menu:

    def __init__(self, game):
        self.game = game

    def loop(self):
        print(f'This is a {self.__class__}')
        self.make_elements()

        while self.game.F_current_loop_running:
            time_delta = self.game.clock.tick(60) / 1000.0
            self.check_events()
            self.game.manager.update(time_delta)
            self.draw_screen()

    def draw_screen(self):
        self.game.display.fill('black')
        self.game.window.blit(self.game.display, (0, 0))
        self.game.manager.draw_ui(self.game.window)
        pygame.display.update()

    def change_menu(self, new_menu):
        self.kill_elements()
        self.game.F_current_loop_running = False
        self.game.current_loop = new_menu

    def quit_the_game(self):
        self.kill_elements()
        self.game.F_current_loop_running = False
        self.game.F_running = False

    def make_elements(self):
        pass

    def check_events(self):
        pass

    def kill_elements(self):
        pass


class Main_menu(Menu):

    def make_elements(self):
        top = self.game.window_center[1] - 100
        left = self.game.window_center[0] - 70
        self.start_game_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (left, top), (140, 50)),
                 text='Начать игру',
                 manager=self.game.manager)
        self.settings_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (left, top + 70), (140, 50)),
                 text='Настройки',
                 manager=self.game.manager)
        self.quit_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (left, top + 140), (140, 50)),
                 text='Выход',
                 manager=self.game.manager)

    def kill_elements(self):
        self.start_game_button.kill()
        self.quit_button.kill()
        self.settings_button.kill()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_the_game()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_game_button:
                    self.change_menu('Game')

                if event.ui_element == self.settings_button:
                    self.change_menu('Settings_menu')

                if event.ui_element == self.quit_button:
                    self.quit_the_game()

            self.game.manager.process_events(event)  # Обработка событий GUI


class Settings_menu(Menu):

    def make_elements(self):
        top = self.game.window_center[1] - 100
        left = self.game.window_center[0] - 70
        self.volume_settings_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (left, top), (140, 50)),
                 text='Звук',
                 manager=self.game.manager)
        self.graphic_settings_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (left, top + 70), (140, 50)),
                 text='Графика',
                 manager=self.game.manager)
        self.back_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (left, top + 140), (140, 50)),
                 text='Назад',
                 manager=self.game.manager)

    def kill_elements(self):
        self.volume_settings_button.kill()
        self.graphic_settings_button.kill()
        self.back_button.kill()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_the_game()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.volume_settings_button:
                    self.change_menu('Volume_settings')

                if event.ui_element == self.graphic_settings_button:
                    self.change_menu('Graphic_settings')

                if event.ui_element == self.back_button:
                    self.change_menu('Main_menu')

            self.game.manager.process_events(event)  # Обработка событий GUI


class Volume_settings(Menu):

    def make_elements(self):
        from config import settings

        top = self.game.window_center[1] - 100
        left = self.game.window_center[0] - 100
        self.volume_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(
                    (left - 160, top + 70), (140, 30)),
                html_text='Общая громкость',
                manager=self.game.manager)
        self.volume_slider = pygame_gui.elements.UIHorizontalSlider(
                relative_rect=pygame.Rect(
                    (left, top + 70), (200, 30)),
                 start_value=settings['mixer_volume'],
                 value_range=(0, 1),
                 manager=self.game.manager)
        self.volume_amount_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(
                    (left + 220, top + 70), (40, 30)),
                html_text=f'{int(pygame.mixer.music.get_volume()*100)}',
                manager=self.game.manager)
        self.back_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (left + 30, top + 140), (140, 50)),
                text='Назад',
                manager=self.game.manager)

    def kill_elements(self):
        self.volume_text.kill()
        self.volume_slider.kill()
        self.volume_amount_text.kill()
        self.back_button.kill()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_the_game()

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                pygame.mixer.music.set_volume(event.value)
                self.volume_amount_text.set_text(f'{int(pygame.mixer.music.get_volume()*100)}')

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.back_button:
                    self.change_menu('Settings_menu')

            self.game.manager.process_events(event)  # Обработка событий GUI
