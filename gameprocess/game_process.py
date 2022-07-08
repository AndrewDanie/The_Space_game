from numpy import array, zeros
from game_init import *

from gameprocess.camera import Camera
from gameprocess.game_logic import Game_logic
from gameprocess.level_objects import Level, Static_object


class Game_process():

    def __init__(self):
        self.load_game_audio()
        self.load_game_graphic()
        self.current_level_number = 1
        self.current_level = Level(self.current_level_number)
        self.camera = Camera(self)
        self.logic = Game_logic(self.current_level.level_objects, self.current_level.level_ships)
        print('game process successfully initialized')

    def load_game_audio(self):
        self.sound_ambient = mixerload('Ambient1.wav')
        self.sound_of_engine = mixerload('engine.wav')
        self.sound_of_engine.set_volume(0.01)

    def load_game_graphic(self):
        self.resolution = array(resolution)
        self.indent_cord = array([100, 150])  # Отступ рамки
        self.camera_cord = array([- self.resolution[0] // 2, - self.resolution[1] // 2])  # Начальное положение камеры

        self.pic_frame = Static_object('Frame.png')
        self.pic_gear = Static_object('gear.png')
        self.pic_tank = Static_object('Tank.png')
        self.pic_background = Static_object('field_1.jpg')
        self.pic_gear.image = pygame.transform.rotozoom(self.pic_gear.image, 0, 0.4)
        self.pic_tank.image = pygame.transform.rotozoom(self.pic_tank.image, 0, 0.2)