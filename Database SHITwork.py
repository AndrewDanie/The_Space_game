

"""Место для тестирования всякой ерунды, в т.ч. SQL-запросов"""


import sqlite3
import pygame
import os

pygame.init()
window = pygame.display.set_mode((1000, 700))

with sqlite3.connect('data/database.db') as db:
    cursor = db.cursor()
    # cursor.execute('DROP TABLE IF EXISTS planets')
    # cursor.execute("""CREATE TABLE IF NOT EXISTS planets(
    #     planets_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     image VARCHAR(30),
    #     name VARCHAR(30),
    #     color VARCHAR(30),
    #     mass INTEGER,
    #     zoom REAL,
    #     radius INTEGER
    # )""")
    # values = [('Sun_1.png', 'Sun', '#ffffff', 1000, 3, 230),
    #           ('Earth.png', 'Earth', '#6464ff', 100, 0.5, 50),
    #           ('Moon.png', 'Moon', '#373737', 10, 0.2, 22),
    #           ('Mars.png', 'Mars', '#ff6400', 50, 0.4, 40),
    # ]
    # cursor.executemany('INSERT INTO planets VALUES(NULL, ?, ?, ?, ?, ?, ?)', values)
    # cursor.execute("""UPDATE levels
    #     SET image = 'field1.jpg'
    # """)
    # cursor.execute('SELECT * FROM levels')
    # print(cursor.fetchone()[1])

    # for i in range(1, 6):
    #     cursor.execute(f'DROP TABLE IF EXISTS level_{i}')
    #     cursor.execute(f"""CREATE TABLE IF NOT EXISTS level_{i}(
    #         planets_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         class VARCHAR(30),
    #         name VARCHAR(30),
    #         x REAL,
    #         y REAL,
    #         vector_x REAL,
    #         vector_y REAL
    #     )""")
    # values = [
    #     [('Planet', 'Sun', 0, 0, 0, 0),
    #         ('Planet', 'Earth', 4000, 0, 0, -0.15),
    #         ('Planet', 'Moon', 4600, 0, -0.05, -0.31),
    #         ('Planet', 'Mars', -7100, 0, 0, 0.15),
    #         ('Ship', 'Ship_1', -4100, 0, 0, -0.6),
    #     ],
    #     [('Planet', 'Sun', 0, 0, 0, 0),
    #         ('Planet', 'Earth', 4000, 0, 0, -0.15),
    #         ('Planet', 'Moon', 4600, 0, -0.05, -0.31),
    #         ('Planet', 'Mars', -7100, 0, 0, 0.15),
    #         ('Ship', 'Ship_2', 4650, 0, 0, -0.44),
    #     ],
    #     [('Planet', 'Sun', 0, 0, 0, 0),
    #          ('Planet', 'Earth', 4000, 0, 0, -0.15),
    #          ('Planet', 'Moon', 4600, 0, -0.05, -0.31),
    #          ('Planet', 'Mars', -7100, 0, 0, 0.15),
    #          ('Ship', 'Ship_1', -7200, 0, 0, -0.05),
    #      ],
    #     [('Planet', 'Sun', 0, 0, 0, 0),
    #          ('Planet', 'Earth', 4000, 0, 0, -0.15),
    #          ('Planet', 'Moon', 4600, 0, -0.05, -0.31),
    #          ('Planet', 'Mars', -7100, 0, 0, 0.15),
    #          ('Ship', 'Ship_2', -4650, 0, 0, -0.44),
    #      ],
    #     [('Planet', 'Sun', 0, 0, 0, 0),
    #          ('Planet', 'Earth', 4000, 0, 0, -0.15),
    #          ('Planet', 'Moon', 4600, 0, -0.05, -0.31),
    #          ('Planet', 'Mars', -7100, 0, 0, 0.15),
    #          ('Ship', 'Ship_2', -7200, 0, 0, -0.05),
    #      ]
    # ]
    # for i in range(5):
    #     cursor.executemany(f'INSERT INTO level_{i+1} VALUES(NULL, ?, ?, ?, ?, ?, ?)', values[i])
    # cursor.execute('DROP TABLE IF EXISTS ships')
    # cursor.execute("""CREATE TABLE IF NOT EXISTS ships(
    #     ships_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     image VARCHAR(30),
    #     name VARCHAR(30),
    #     color VARCHAR(30),
    #     mass INTEGER,
    #     zoom REAL,
    #     IDK_what_is_it REAL,
    #     IDK_what_is_it_2 REAL,
    #     acceleration REAL
    # )""")
    # values = [('Ship_1.png', 'Ship_1', '#37ff64', 2000, 0.1, 0.2, 10, 0.01),
    #           ('Ship_2.png', 'Ship_2', '#37ff64', 10000, 0.1, 0.2, 10, 0.005),
    #           ('Ship_3.png', 'Ship_3', '#37ff64', 20000, 0.05, 0.2, 10, 0.002)
    # ]
    # cursor.executemany('INSERT INTO ships VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)', values)

    # for i in range(5):
    #     cursor.execute(f'ALTER TABLE level_{i+1} ADD COLUMN level_id INTEGER')
    #     cursor.execute(f'UPDATE level_{i+1} SET level_id = {i+1}')
#
# def musicload(filename):
#     music = pygame.mixer.music.load(os.path.join('sounds', filename))
#     pygame.mixer.music.play(-1)
#     return music
#
#
# def mixerload(filename):
#     return pygame.mixer.Sound(os.path.join('sounds', filename))
#
#
# def imgload(filename):
#     return pygame.image.load(os.path.join('image', filename)).convert()
#
#
# class Level:
#     '''Загрузка и инициализация объектов уровня'''
#
#     def __init__(self, level_number):
#         '''Определяем общие параметры уровня'''
#
#         self.number = level_number
#         with sqlite3.connect('data/database.db') as db:
#             db.row_factory = sqlite3.Row
#             cursor = db.cursor()
#             cursor.execute(f'SELECT * FROM levels WHERE level_id = {level_number}')
#             current_level = cursor.fetchone()
#             for key in current_level.keys():
#                 self.__dict__[key]= current_level[key]
#             self.level_objects = []
#             PlanetsTable = cursor.execute(f'SELECT * FROM planets JOIN level_{level_number} USING(name)').fetchall()
#
#         Lvlreader = cursor.execute(f'SELECT * FROM level_{level_number}').fetchall()
#         for row in Lvlreader:
#             params = {
#                 'class': row[1],
#                 'name': row[2],
#                 'position': (row[3], row[4]),
#                 'vector': (row[5], row[6])
#             }
#         PlanetsTable = cursor.execute(f'SELECT * FROM planets JOIN level_{level_number} USING(name)')
#         for row in PlanetsTable:
#             for key in row.keys():
#                 print(key, end=" ")
#             print()
#         ShipsTable = cursor.execute(f'SELECT * FROM ships JOIN level_{level_number} USING(name)')
#         for row in ShipsTable:
#             for key in row.keys():
#                 print(key, end=" ")
#             print()
#
# a = Level(1)
