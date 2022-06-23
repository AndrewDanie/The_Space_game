import pygame

class Camera:

    def __init__(self, game):
        self.window = game.window
        self.window_center = game.window_center
        focus_obj = game.Game_loop.current_level.level_objects[4] # Фокус - корабль
        self.focus_x = focus_obj.x
        self.focus_y = focus_obj.y
        self.zoom = 1

    def draw(self, obj):

        x = obj.x*self.zoom - self.focus_x + self.window_center[0]
        y = obj.y*self.zoom - self.focus_y + self.window_center[1]

        obj.rect = obj.image.get_rect(center=(x,y))
        self.window.blit(obj.image, obj.rect)