import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ Класс, представляющий оджого пришельца"""

    def __init__(self, game_settings, screen):
        """ Инициализтрйет пришельца и задает его начальную позицию"""
        super().init()
        self.screen = screen
        self.game_settings = game_settings

        # Загрузка изображения и назначение атрибута rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Каждый новы йпришелец появляется в верхнем углу
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной позиции пришельца
        self.x = float(self.rect.x)

    def blitme(self):
        """ Выводит пришельца в текущем положении"""
        self.screen.blit(self.image, self.rect)