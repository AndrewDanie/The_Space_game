import pygame
from config import *
import math



class Game_logic:

    def __init__(self, level_objects, level_ships):
        self.objects = level_objects
        self.ships = level_ships
        self.ship = level_ships[0]
        self.window_center_x = resolution_x // 2
        self.window_center_y = resolution_y // 2

        self.deltaTime0 = 1 # секунд за физический тик
        self.physticks0 = 60 # физических тиков в кадре

        self.deltaTime = self.deltaTime0  # секунд за физический тик
        self.physticks = self.physticks0  # физических тиков в кадре

        self.gravitationalConstant = 6.6743 * 10 ** -11

        for obj in (self.objects + self.ships):
            obj.accel_x = 0
            obj.accel_y = 0

    def check_events(self, event):


        pass


    def game_logic_control(self):
        pressed = pygame.mouse.get_pressed()
        keypressed = pygame.key.get_pressed()
        mouse_position = pygame.mouse.get_pos()

        print(pressed, mouse_position)

        if pressed[0]:
            self.calc_velocity_vector(mouse_position)

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.deltaTime = self.deltaTime0 * 1  # секунд за физический тик
            self.physticks = self.physticks0 * 10  # физических тиков в кадре
        else:
            self.deltaTime = self.deltaTime0  # секунд за физический тик
            self.physticks = self.physticks0  # физических тиков в кадре


        shipaccel = 10
        timemult =self.physticks * self.deltaTime

        if pygame.key.get_pressed()[pygame.K_a]:
            self.ship.velocity_x -= shipaccel * timemult
        if pygame.key.get_pressed()[pygame.K_d]:
            self.ship.velocity_x += shipaccel * timemult
        if pygame.key.get_pressed()[pygame.K_w]:
            self.ship.velocity_y -= shipaccel * timemult
        if pygame.key.get_pressed()[pygame.K_s]:
            self.ship.velocity_y += shipaccel * timemult

    def gravitate(self, obj):

        obj.accel_x = 0.0
        obj.accel_y = 0.0
        for gravyBody in self.objects:

            dxsh = (obj.x - gravyBody.x)
            dysh = (obj.y - gravyBody.y)
            rsh = math.sqrt(dxsh ** 2 + dysh ** 2)
            obj.accel_x -= gravyBody.mass * self.gravitationalConstant * dxsh / rsh ** 3
            obj.accel_y -= gravyBody.mass * self.gravitationalConstant * dysh / rsh ** 3

    def check_collisions(self):
        pass

    def calc_velocity_vector(self, mouse_target):

        x = self.window_center_x - mouse_target[0]
        y = self.window_center_y - mouse_target[1]
        #k = (x**2 + y**2)**0.5 / self.ship.thrust
        k = 1 / self.ship.thrust * self.physticks * self.deltaTime # пока не нормируем
        print('poof')
        try:
            self.ship.velocity_x -= x / k * self.deltaTime
            self.ship.velocity_y -= y / k * self.deltaTime
        except:
            raise ZeroDivisionError




    def move_objects(self):
        for obj in self.objects + self.ships:
            obj.x += obj.velocity_x * self.deltaTime + obj.accel_x * (self.deltaTime ** 2) / 2
            obj.y += obj.velocity_y * self.deltaTime + obj.accel_y * (self.deltaTime ** 2) / 2

            obj.velocity_x += float(obj.accel_x) * self.deltaTime
            obj.velocity_y += float(obj.accel_y) * self.deltaTime

    def do_tick_logic(self):
        self.game_logic_control()
        #self.change_velocity()
        self.move_objects()

        for i in range(self.physticks):
            self.gravitate(self.ship)
            self.move_objects()

