import sqlite3
import os
import pygame


'''Упрощаем запись загружающих функций'''
def musicload(filename):
    music = pygame.mixer.music.load(os.path.join('sounds', filename))
    pygame.mixer.music.play(-1)
    return music


def mixerload(filename):
    return pygame.mixer.Sound(os.path.join('sounds', filename))


def imgload(filename):
    return pygame.image.load(os.path.join('image', filename)).convert()


class Level:
    """
    Загрузка и инициализация объектов игрового уровня
    """
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


class Grav_object():

    def __init__(self, params):
        self.name = params['name']
        self.pos = (params['x'], params['y'])
        self.vector = (params['vector_x'], params['vector_y'])
        self.color = params['color']
        self.mass = params['mass']
        self.img = imgload(params['image'])
        self.zoom = params['zoom']


class Planet(Grav_object):

    def __init__(self, params):
        Grav_object.__init__(self, params)
        self.radius = params['radius']


class Ship(Grav_object):

    def __init__(self, params):
        Grav_object.__init__(self, params)
        self.engine_image = imgload(params['engine_image'])
        self.IDK_what_is_it = params['IDK_what_is_it']
        self.IDK_what_is_it_2 = params['IDK_what_is_it_2']
        self.accel = params['acceleration']


class Pointer():

    def __init__(self, params):
        self.name = params['name']
        self.pos = params['position']
