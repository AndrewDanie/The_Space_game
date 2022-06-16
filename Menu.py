import pygame
import pygame_gui


class Menu:

    def __init__(self, game):
        self.game = game
        pygame.display.set_mode(self.game.resolution)

    def loop(self):

        print(f'This is a {self.__class__}')
        self.make_buttons()

        while self.game.F_current_loop_running:
            time_delta = self.game.clock.tick(60) / 1000.0
            self.check_events()
            self.game.manager.update(time_delta)
            self.draw_screen_with_buttons()

    def draw_screen_with_buttons(self):
        self.game.display.fill('black')
        self.game.window.blit(self.game.display, (0, 0))
        self.game.manager.draw_ui(self.game.window)
        pygame.display.update()

    def change_menu(self, new_menu):
        self.kill_buttons()
        self.game.F_current_loop_running = False
        self.game.current_loop = new_menu

    def quit_the_game(self):
        self.kill_buttons()
        self.game.F_current_loop_running = False
        self.game.F_running = False

    def make_buttons(self):
        pass

    def check_events(self):
        pass

    def kill_buttons(self):
        pass


class Main_menu(Menu):

    def make_buttons(self):
        top = self.game.window_center[1] - 100
        left = self.game.window_center[0]-70
        self.start_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                    (left, top), (140, 50)),
                     text='Начать игру',
                     manager=self.game.manager)
        self.settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                    (left, top+70), (140, 50)),
                     text='Настройки',
                     manager=self.game.manager)
        self.quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                    (left, top+140), (140, 50)),
                     text='Выход',
                     manager=self.game.manager)

    def kill_buttons(self):
        self.start_game_button.kill()
        self.quit_button.kill()
        self.settings_button.kill()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_the_game()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_game_button:
                    self.change_menu('game')

                if event.ui_element == self.settings_button:
                    self.change_menu('Settings_menu')

                if event.ui_element == self.quit_button:
                    self.quit_the_game()

            self.game.manager.process_events(event)  # Обработка событий GUI


class Settings_menu(Menu):

    def make_buttons(self):
        top = self.game.window_center[1] - 100
        left = self.game.window_center[0]-70
        self.volume_settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                    (left, top), (140, 50)),
                     text='Звук',
                     manager=self.game.manager)
        self.graphic_settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                    (left, top+70), (140, 50)),
                     text='Графика',
                     manager=self.game.manager)
        self.back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
                    (left, top+140), (140, 50)),
                     text='Назад',
                     manager=self.game.manager)

    def kill_buttons(self):
        self.volume_settings_button.kill()
        self.graphic_settings_button.kill()
        self.back_button.kill()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_the_game()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                print('bruh')
                if event.ui_element == self.volume_settings_button:
                    self.change_menu('Volume_settings')

                if event.ui_element == self.graphic_settings_button:
                    self.change_menu('Graphic_settings')

                if event.ui_element == self.back_button:
                    self.change_menu('Main_menu')

            self.game.manager.process_events(event)  # Обработка событий GUI


class Volume_settings(Menu):

    pass