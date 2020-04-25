import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ Класс, представляющий оджого пришельца"""

    def __init__(self, game_settings, screen):
        """ Инициализтрйет пришельца и задает его начальную позицию"""
        super().__init__()
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

    def check_edges(self):
        """ Возвращает True, если пришелей находится у края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """ Перемещает пришельца вправо"""
        self.x += self.game_settings.alien_speed_factor * self.game_settings.fleet_direction
        self.rect.x = self.x
