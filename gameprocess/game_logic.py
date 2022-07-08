import pygame
from config import *

class Game_logic:

    def __init__(self, level_objects, level_ships):
        self.objects = level_objects
        self.ships = level_ships
        self.ship = level_ships[0]
        self.window_center_x = resolution_x // 2
        self.window_center_y = resolution_y // 2

    def check_events(self, event):
        #pressed = pygame.mouse.get_pressed()
        #pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.calc_velocity_vector(event.pos)

    def do_tick_logic(self):
        self.change_velocity()
        self.move_objects()

    def change_velocity(self):
        pass

    def gravitate(self, first_obj, second_obj):
        pass

    def check_collisions(self):
        pass

    def calc_velocity_vector(self, mouse_target):
        x = self.window_center_x - mouse_target[0]
        y = self.window_center_y - mouse_target[1]
        #k = (x**2 + y**2)**0.5 / self.ship.thrust
        k = 100 / self.ship.thrust # пока не нормируем
        try:
            self.ship.velocity_x -= x / k
            self.ship.velocity_y -= y / k
        except:
            raise ZeroDivisionError


    def move_objects(self):
        for obj in self.objects + self.ships:
            obj.x += obj.velocity_x
            obj.y += obj.velocity_y
