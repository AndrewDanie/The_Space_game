import pygame
from config import settings

class Game_logic:

    def __init__(self, level_objects):
        self.objects = level_objects
        self.ship = self.objects[4]
        self.window_center_x = settings['resolution_x'] // 2
        self.window_center_y = settings['resolution_y'] // 2

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.calc_velocity_vector(event.pos)

    def do_tick_logic(self):
        self.change_velocity()
        self.move_objects()

    def change_velocity(self):
        pass

    def gravitate(self, first_obj, secong_obj):
        pass

    def calc_velocity_vector(self, mouse_target):
        x = self.window_center_x - mouse_target[0]
        y = self.window_center_y - mouse_target[1]
        print(x, y)
        k = (x**2 + y**2)**0.5 / self.ship.thrust
        self.ship.velocity_x -= x / k
        self.ship.velocity_y -= y / k


    def move_objects(self):
        for obj in self.objects:
            obj.x += obj.velocity_x
            obj.y += obj.velocity_y