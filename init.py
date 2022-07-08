import os
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
resolution = (resolution_x, resolution_y)
window_center = (resolution_x // 2, resolution_y // 2)
clock = pygame.time.Clock()
window = pygame.display.set_mode(resolution)
display = pygame.Surface(resolution)  # Главная отрисовываемая поверхность
manager = pygame_gui.UIManager(resolution)  # Запускаем GUI-менеджер


def musicload(filename):
    music = pygame.mixer.music.load(os.path.join('sounds', filename))
    pygame.mixer.music.play(-1)
    return music


def mixerload(filename):
    return pygame.mixer.Sound(os.path.join('sounds', filename))
# Разобраться с разницей между musicload и mixerload


def imgload(filename):
    return pygame.image.load(os.path.join('image', filename)).convert_alpha()


