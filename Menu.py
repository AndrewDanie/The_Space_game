import pygame
import pygame_gui

class Menu:

    def __init__(self, game):
        self.game = game
        pygame.display.set_mode(self.game.resolution)

    def loop(self):
        """
        Цикл меню
        """
        print('This is a menu loop')
        buttons = self.make_menu_buttons()

        while self.game.F_current_loop_running:
            time_delta = self.game.clock.tick(60) / 1000.0
            self.menu_check_events()
            self.game.manager.update(time_delta)
            self.game.display.fill('black')
            self.game.window.blit(self.game.display, (0, 0))
            self.game.manager.draw_ui(self.game.window)
            pygame.display.update()

    def menu_check_events(self):
        """
        Проверка  событий главного меню
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.F_current_loop_running = False
                self.game.F_running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_game_button:
                    self.game.F_current_loop_running = False
                    self.kill_menu_buttons()
                    self.game.current_loop = 'game'
                if event.ui_element == self.settings_button:
                    self.game.F_current_loop_running = False
                    self.kill_menu_buttons()
                    self.game.current_loop = 'settings'
                if event.ui_element == self.quit_button:
                    self.game.F_current_loop_running = False
                    self.game.F_running = False

            self.game.manager.process_events(event)  # Обработка событий GUI

    def make_menu_buttons(self):
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


    def kill_menu_buttons(self):
        self.start_game_button.kill()
        self.quit_button.kill()
        self.settings_button.kill()


class Settings_menu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
