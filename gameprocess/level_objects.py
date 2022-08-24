import sqlite3
from game_init import imgload
import pygame

maxwidth = 2000 # чтобы не переполнять память
class Level:

    def __init__(self, level_number):
        """
        Определяем общие параметры уровня
        """
        with sqlite3.connect('data/database.db') as db:  # Подключаем базу даных
            db.row_factory = sqlite3.Row
            cursor = db.cursor()

            '''Загружаем характеристики уровня'''
            cursor.execute(f'SELECT * FROM levels WHERE level_id = {level_number}')
            current_level = cursor.fetchone()

            self.level_id = current_level['level_id']
            self.image = imgload(current_level['image'])
            self.victory_time = current_level['victory_time']
            self.ktime_1 = current_level['ktime_1']
            self.ktime_2 = current_level['ktime_2']
            self.screen_size = current_level['screen_size']
            self.radius_max = current_level['radius_max']
            self.goal_planet = current_level['goal_planet']
            self.victory_rad_inn = current_level['victory_rad_inn']
            self.victory_rad_out = current_level['victory_rad_out']

            self.level_objects = []
            self.level_ships = []
            '''Загружаем объекты уровня'''
            '''Добавляем Солнце и планеты'''
            PlanetsTable = cursor.execute(f'SELECT * FROM planets JOIN level_{level_number} USING(name)')
            for params in PlanetsTable:
                planet = Planet(params)
                self.level_objects.append(planet)

            '''Добавляем корабли'''
            ShipsTable = cursor.execute(f'SELECT * FROM ships JOIN level_{level_number} USING(name)')
            for params in ShipsTable:
                ship = Ship(params)
                #self.level_objects.append(ship)
                self.level_ships.append(ship)
                print('add_ship')
        print(f'level_{self.level_id} successfully loaded')


class Grav_object(pygame.sprite.Sprite):

    def __init__(self, params):
        pygame.sprite.Sprite.__init__(self)
        self.image_data = imgload(params['image'])
        self.image = self.image_data
        self.scaled_image = self.image_data
        self.rot_image = self.image_data
        self.image_width = params['img_width'] / 10
        self.image_height = params['img_height'] / 10
        self.scale_image()
        self.angle = 0
        self.last_angle = self.angle
        self.x = params['x']
        self.y = params['y']
        self.name = params['name']
        #self.velocity_x = 0 # Для тестов со статическими планетами
        #self.velocity_y = 0
        self.velocity_x = float(params['velocity_x'])
        self.velocity_y = float(params['velocity_y'])
        self.color = params['color']

        self.cam_x = 0 # - костыль для транслирования положения на экране в gamelogic
        self.cam_y = 0

    def scale_image(self):
        self.scaled_image = pygame.transform.smoothscale(self.image_data, (min(maxwidth, self.image_width), min(maxwidth, self.image_height)))
        self.image = self.scaled_image

    def rotate_image(self):
        if self.angle != self.last_angle:
            self.image = pygame.transform.rotate(self.scaled_image, self.angle)
            self.last_angle = self.angle
       # else:
      #      self.image = self.scaled_image

class Planet(Grav_object):

    def __init__(self, params):
        Grav_object.__init__(self, params)
        self.radius = params['radius']
        self.mass = params['mass']


class Ship(Grav_object):

    def __init__(self, params):
        Grav_object.__init__(self, params)
        self.engine_image = imgload(params['engine_image'])
        self.IDK_what_is_it = params['IDK_what_is_it']
        self.IDK_what_is_it_2 = params['IDK_what_is_it_2']
        self.fuel_mass = params['fuel_mass']
        self.mass = params['ship_mass']  # Масса все равно большая, надо менять

        self.thrust = params['engine_thrust']
        self.specific_impulse = params['engine_specific_impulse']
        self.acceleration = self.thrust / (self.mass + self.fuel_mass)
        self.thrust /= 1000

        self.accelerating = False


class Pointer(pygame.sprite.Sprite):

    def __init__(self, params):
        pygame.sprite.Sprite.__init__(self)
        self.name = params['name']
        self.pos = params['position']


class Static_object(pygame.sprite.Sprite):

    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = imgload(filename)
