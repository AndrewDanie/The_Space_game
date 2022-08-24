import pygame
from config import *
import math

from gameprocess.camera import Camera # имеет ли смысл отсюда повторно вызывать?


class Game_logic:

    def __init__(self, level_objects, level_ships):
        self.objects = level_objects
        self.ships = level_ships
        self.ship = level_ships[0]
        self.window_center_x = resolution_x // 2
        self.window_center_y = resolution_y // 2

        self.deltaTime0 = 10 # секунд за физический тик
        self.physticks0 = 6 # физических тиков в кадре

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
        #keypressed = pygame.key.get_pressed()
        mouse_position = pygame.mouse.get_pos()

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.deltaTime = self.deltaTime0 * 1  # секунд за физический тик с ускорением
            self.physticks = self.physticks0 * 10  # физических тиков в кадре с ускорением
        else:
            self.deltaTime = self.deltaTime0  # секунд за физический тик  стандартно
            self.physticks = self.physticks0  # физических тиков в кадре стандартно

        axtry = [0, 0]

        if pressed[0]:
            #self.calc_velocity_vector(mouse_position)
            axtry[0] = pygame.mouse.get_pos()[0] - self.ship.cam_x
            axtry[1] = pygame.mouse.get_pos()[1] - self.ship.cam_y

        #print(self.ship.cam_x, ' ', self.ship.cam_y)
        #print(mouse_position)
        #print(axtry)


        shipaccel = 10
        timemult = self.physticks * self.deltaTime

        if pygame.key.get_pressed()[pygame.K_a]:
            axtry[0] -= 1
        if pygame.key.get_pressed()[pygame.K_d]:
            axtry[0] += 1
        if pygame.key.get_pressed()[pygame.K_w]:
            axtry[1] -= 1
        if pygame.key.get_pressed()[pygame.K_s]:
            axtry[1] += 1
        if axtry != [0, 0]:


            self.ship.angle =( - math.atan2( axtry[1], axtry[0]) * 180 / 3.14 + 180) // 1
            self.ship.accelerating = True
            self.ship.velocity_x += shipaccel * timemult * axtry[0] / math.sqrt(axtry[0] ** 2 + axtry[1] ** 2)
            self.ship.velocity_y += shipaccel * timemult * axtry[1] / math.sqrt(axtry[0] ** 2 + axtry[1] ** 2)
        else:
            self.ship.angle = (180 - math.atan2(pygame.mouse.get_pos()[1] - self.ship.cam_y,
                                               pygame.mouse.get_pos()[0] - self.ship.cam_x) * 180 / 3.14) // 1
            self.ship.accelerating = False

    def check_collisions(self):
        pass

    def calc_velocity_vector(self, mouse_target):

        timemult = self.physticks * self.deltaTime
        x = self.window_center_x - mouse_target[0]
        y = self.window_center_y - mouse_target[1]
        #k = (x**2 + y**2)**0.5 / self.ship.thrust
        k = 1 / self.ship.thrust # пока не нормируем
        print('poof')
        try:
            self.ship.velocity_x -= x / k * timemult
            self.ship.velocity_y -= y / k * timemult
        except:
            raise ZeroDivisionError


    """
    def gravitate(self, obj):

        obj.accel_x = 0.0
        obj.accel_y = 0.0
        for gravyBody in self.objects:

            dxsh = (obj.x - gravyBody.x)
            dysh = (obj.y - gravyBody.y)
            rsh = math.sqrt(dxsh ** 2 + dysh ** 2)
            obj.accel_x -= gravyBody.mass * self.gravitationalConstant * dxsh / rsh ** 3
            obj.accel_y -= gravyBody.mass * self.gravitationalConstant * dysh / rsh ** 3
            
    def move_objects(self):
        for obj in self.objects + self.ships:
            obj.x += obj.velocity_x * self.deltaTime + obj.accel_x * (self.deltaTime ** 2) / 2
            obj.y += obj.velocity_y * self.deltaTime + obj.accel_y * (self.deltaTime ** 2) / 2

            obj.velocity_x += float(obj.accel_x) * self.deltaTime
            obj.velocity_y += float(obj.accel_y) * self.deltaTime
    """
    def gravitational_move(self):

        for i in range(self.physticks):

            for obj in self.objects + self.ships:
                obj.accel_x = 0.0
                obj.accel_y = 0.0
                for gravyBody in self.objects:
                    if gravyBody != obj:
                        dxsh = (obj.x - gravyBody.x)
                        dysh = (obj.y - gravyBody.y)
                        rsh = math.sqrt(dxsh ** 2 + dysh ** 2)
                        obj.accel_x -= gravyBody.mass * self.gravitationalConstant * dxsh / rsh ** 3
                        obj.accel_y -= gravyBody.mass * self.gravitationalConstant * dysh / rsh ** 3



                obj.x += obj.velocity_x * self.deltaTime + obj.accel_x * (self.deltaTime ** 2) / 2
                obj.y += obj.velocity_y * self.deltaTime + obj.accel_y * (self.deltaTime ** 2) / 2

                obj.velocity_x += obj.accel_x * self.deltaTime
                obj.velocity_y += obj.accel_y * self.deltaTime



    def do_tick_logic(self):
        self.game_logic_control()
        #self.change_velocity()

        self.gravitational_move()

        #print(Camera.coordinates_on_screen(self.ship))

        #for i in range(self.physticks):
        #    self.gravitate(self.ship)
        #    self.move_objects()

