import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ Класс, представляющий оджого пришельца"""

    def __init__(self, game_settings, screen):
        """ Инициализтрйет пришельца и задает его начальную позицию"""
        super().init()
        