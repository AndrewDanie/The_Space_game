import pygame

class Camera:

    def __init__(self, game):
        self.window = game.window
        self.CENTER_X = game.window_center[0]
        self.CENTER_Y = game.window_center[1]

        self.zoom = 1.0
        self.zoom_out_factor = 1 - 0.03
        self.zoom_in_factor = 1 + 0.03

        self.cam_mode = 0
        self.level_objects = game.Game_loop.current_level.level_objects
        self.level_ships = game.Game_loop.current_level.level_ships

        self.focus_ship = self.level_ships[0]
        self.focus_x = self.focus_ship.x
        self.focus_y = self.focus_ship.y
        self.focus_to_the_ship()

    def draw_level_objects(self):
        for obj in (self.level_objects + self.level_ships):
            if self.cam_mode == 0:
                self.focus_x = self.focus_ship.x
                self.focus_y = self.focus_ship.y
            x = self.CENTER_X + (self.free_cam_x + obj.x - self.focus_x) * self.zoom
            y = self.CENTER_Y + (self.free_cam_y + obj.y - self.focus_y) * self.zoom
            obj.rect = obj.image.get_rect(center=(x,y))
            self.window.blit(obj.image, obj.rect)

    def check_events(self, event=None):
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.cam_mode += 1
                    self.cam_mode %= 2
                    print(f'camera mode is {self.cam_mode}')
                    if self.cam_mode == 0:
                        self.focus_to_the_ship()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    self.zoom_out()
                elif event.button == 4:
                    self.zoom_in()

        else:
            if self.cam_mode == 1:
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    self._move_left()
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    self._move_right()
                if pygame.key.get_pressed()[pygame.K_UP]:
                    self._move_up()
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    self._move_down()

    def focus_to_the_ship(self):
        self.free_cam_x = 0
        self.free_cam_y = 0

    def zoom_out(self):
        if self.zoom > 0.03:
            self.zoom *= self.zoom_out_factor
            for obj in self.level_objects:
                obj.image_width *= self.zoom_out_factor
                obj.image_height *= self.zoom_out_factor
                obj.scale_image()

    def zoom_in(self):
        if self.zoom < 5:
            self.zoom *= self.zoom_in_factor
            for obj in self.level_objects:
                obj.image_width *= self.zoom_in_factor
                obj.image_height *= self.zoom_in_factor
                obj.scale_image()

    def _move_right(self):
        self.free_cam_x -= 10

    def _move_left(self):
        self.free_cam_x += 10

    def _move_up(self):
        self.free_cam_y += 10

    def _move_down(self):
        self.free_cam_y -= 10