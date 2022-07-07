from init import *


class Menu:
    def __init__(self):
        self.F_current_loop_running = True
        self.new_loop = None

    def loop(self):
        print(f'This is a {self.__class__}')
        self.make_elements()

        while self.F_current_loop_running:
            time_delta = clock.tick(60) / 1000.0
            self.check_events()
            manager.update(time_delta)
            self.draw_screen()

        return self.new_loop

    def draw_screen(self):
        window.fill('black')
        window.blit(display, (0, 0))
        manager.draw_ui(window)
        pygame.display.update()

    def change_menu(self):
        self.kill_elements()
        self.F_current_loop_running = False

    def make_elements(self):
        pass

    def check_events(self):
        pass

    def kill_elements(self):
        pass
