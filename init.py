import pygame
import pygame_gui
from config import *


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()


F_mixer_running = True
try:
    pygame.mixer.init()
except:
    F_mixer_running = False
finally:
    print('Sound mixer running is', F_mixer_running)
pygame.mixer.music.set_volume(mixer_volume)


pygame.display.set_caption('SPACE GAME')  # Название окна
res_x, res_y = resolution_x, resolution_y
resolution = (res_x, res_y)
window_center = (res_x // 2, res_y // 2)
window = pygame.display.set_mode(resolution)
display = pygame.Surface(resolution)  # Главная отрисовываемая поверхность
manager = pygame_gui.UIManager(resolution)  # Запускаем GUI-менеджер
clock = pygame.time.Clock()

