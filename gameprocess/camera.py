from game_init import *

camera_speed = 5


class Camera:

    def __init__(self, game_loop):
        self.CENTER_X = window_center[0]
        self.CENTER_Y = window_center[1]

        #self.zoom = 1.0

        self.zoom = 1 * 10 ** - 6 # пикселей в метре

        self.zoom_out_factor = 1 - 0.2
        self.zoom_in_factor = 1 + 0.2

        self.cam_mode = 0
        self.level_objects = game_loop.current_level.level_objects
        self.level_ships = game_loop.current_level.level_ships

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
            window.blit(obj.image, obj.rect)



    def draw_level_radius(self):

        for obj in (self.level_objects):
            if self.cam_mode == 0:
                self.focus_x = self.focus_ship.x
                self.focus_y = self.focus_ship.y
            x = self.CENTER_X + (self.free_cam_x + obj.x - self.focus_x) * self.zoom
            y = self.CENTER_Y + (self.free_cam_y + obj.y - self.focus_y) * self.zoom

            pygame.draw.circle(window, (255, 255, 255), (x, y), max(3, obj.radius * self.zoom), 2)
            window.blit(obj.image, obj.rect)

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
        if self.zoom > 0.0:
            self.zoom *= self.zoom_out_factor
            for obj in self.level_objects:
                obj.image_width *= self.zoom_out_factor
                obj.image_height *= self.zoom_out_factor
                obj.scale_image()

                #print(f'zoom is {self.zoom}')

    def zoom_in(self):
        if self.zoom < 5 * 10 ** - 4:
            self.zoom *= self.zoom_in_factor
            for obj in self.level_objects:
                obj.image_width *= self.zoom_in_factor
                obj.image_height *= self.zoom_in_factor
                obj.scale_image()
                #print(f'zoom is {self.zoom}')

    def _move_right(self):
        self.free_cam_x -= camera_speed  / self.zoom

    def _move_left(self):
        self.free_cam_x += camera_speed  / self.zoom

    def _move_up(self):
        self.free_cam_y += camera_speed  / self.zoom

    def _move_down(self):
        self.free_cam_y -= camera_speed  / self.zoom