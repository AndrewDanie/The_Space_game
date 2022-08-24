import pygame
from config import *
import math
import datetime
from gameprocess.camera import Camera # имеет ли смысл отсюда повторно вызывать?


class Game_logic:

    def __init__(self, level_objects, level_ships):
        self.objects = level_objects
        self.ships = level_ships
        self.focus_ship = level_ships[0]
        self.window_center_x = resolution_x // 2
        self.window_center_y = resolution_y // 2
        self.time = 0                               # - время с начала уровня

        self.deltaTime0 = 10                        # секунд за физический тик
        self.physticks0 = 6                         # физических тиков в кадре

        self.deltaTime = self.deltaTime0            # секунд за физический тик
        self.physticks = self.physticks0            # физических тиков в кадре

        self.gravitationalConstant = 6.6743 * 10 ** -11

        for obj in (self.objects + self.ships):
            obj.accel_x = 0
            obj.accel_y = 0

    def check_events(self, event):


        pass

    def timer(self):
        self.time += self.physticks * self.deltaTime

        timestring = str(datetime.timedelta(seconds=self.time))
        #print(timestring)


    def game_logic_control(self):
        pressed = pygame.mouse.get_pressed()
        #keypressed = pygame.key.get_pressed()
        mouse_position = pygame.mouse.get_pos()

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.deltaTime = self.deltaTime0 * 10
            self.physticks = self.physticks0 * 1  # физических тиков в кадре с ускорением

        elif pygame.key.get_pressed()[pygame.K_LCTRL]:
            self.deltaTime = self.deltaTime0 / 10   # секунд за физический тик с замедлением
            self.physticks = self.physticks0   # физических тиков в кадре с замедлением
        else:
            self.deltaTime = self.deltaTime0  # секунд за физический тик  стандартно
            self.physticks = self.physticks0  # физических тиков в кадре стандартно

        axtry = [0, 0]

        if pressed[0]:
            #self.calc_velocity_vector(mouse_position)
            axtry[0] = mouse_position[0] - self.focus_ship.cam_x
            axtry[1] = mouse_position[1] - self.focus_ship.cam_y

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


            self.focus_ship.angle =( - math.atan2( axtry[1], axtry[0]) * 180 / 3.14 + 180) // 1
            self.focus_ship.accelerating = True
            self.focus_ship.velocity_x += shipaccel * timemult * axtry[0] / math.sqrt(axtry[0] ** 2 + axtry[1] ** 2)
            self.focus_ship.velocity_y += shipaccel * timemult * axtry[1] / math.sqrt(axtry[0] ** 2 + axtry[1] ** 2)
        else:
            self.focus_ship.angle = (180 - math.atan2(mouse_position[1] - self.focus_ship.cam_y,
                                               mouse_position[0] - self.focus_ship.cam_x) * 180 / 3.14) // 1
            self.focus_ship.accelerating = False


    def check_collisions(self):
        for obj in self.objects:
            if ((obj.x - self.focus_ship.x) ** 2 +
                    (obj.y - self.focus_ship.y) ** 2 < obj.radius ** 2):
                obj.collided = True
                self.focus_ship.collided = True
            else:
                obj.collided = False
                self.focus_ship.collided = False


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
       # print(self.deltaTime)
       # print(self.physticks)



    def do_tick_logic(self):
        self.game_logic_control()
        self.gravitational_move()
        self.check_collisions()
        self.timer()
