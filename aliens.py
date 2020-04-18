import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf

def run_game():
    # Инициализирует игру и создает объект экрана
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(
        (game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("Aliens")

    # Создание корабля
    ship = Ship(game_settings, screen)
    
    # Создание группы для хранения пуль
    bullets = Group()

    # Запуск основного цикла игры
    while True:
        # Отслеживание событий клавиаутры и мыши
        gf.check_events(game_settings, screen, ship, bullets)
        ship.update()
        bullets.update()

        # Удаление пуль вышедших за край экрана
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        # print(len(bullets))
        
        gf.update_screen(game_settings, screen, ship, bullets)

run_game()
