import pygame
import menu


if __name__ == '__main__':
    current_menu = menu.Main_menu()
    while current_menu is not None:
        current_menu = current_menu.loop()
    pygame.quit()