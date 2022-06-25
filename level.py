import sqlite3

import pygame
import game_loop as G


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
            self.image = G.imgload(current_level['image'])
            self.victory_time = current_level['victory_time']
            self.ktime_1 = current_level['ktime_1']
            self.ktime_2 = current_level['ktime_2']
            self.screen_size = current_level['screen_size']
            self.radius_max = current_level['radius_max']
            self.goal_planet = current_level['goal_planet']
            self.victory_rad_inn = current_level['victory_rad_inn']
            self.victory_rad_out = current_level['victory_rad_out']

            self.level_objects = []
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
                self.level_objects.append(ship)

        print(f'level_{self.level_id} successfully initialised')


class Grav_object(pygame.sprite.Sprite):

    def __init__(self, params):
        pygame.sprite.Sprite.__init__(self)
        self.image_data = G.imgload(params['image'])
        self.image = self.image_data
        self.image_width = params['img_width']
        self.image_height = params['img_height']
        self.scale_image()

        self.x = params['x']
        self.y = params['y']
        self.name = params['name']
        self.velocity = (params['velocity_x'], params['velocity_y'])
        self.color = params['color']

    def scale_image(self):
        self.image = pygame.transform.scale(self.image_data, (self.image_width, self.image_height))


class Planet(Grav_object):

    def __init__(self, params):
        Grav_object.__init__(self, params)
        self.radius = params['radius']
        self.mass = params['mass']


class Ship(Grav_object):

    def __init__(self, params):
        Grav_object.__init__(self, params)
        self.engine_image = G.imgload(params['engine_image'])
        self.IDK_what_is_it = params['IDK_what_is_it']
        self.IDK_what_is_it_2 = params['IDK_what_is_it_2']
        self.fuel_mass = params['fuel_mass']
        self.mass = params['ship_mass']  # Масса все равно большая, надо менять
        self.thrust = params['engine_thrust']
        self.specific_impulse = params['engine_specific_impulse']
        self.acceleration = self.thrust / (self.mass + self.fuel_mass)


class Pointer(pygame.sprite.Sprite):

    def __init__(self, params):
        pygame.sprite.Sprite.__init__(self)
        self.name = params['name']
        self.pos = params['position']
