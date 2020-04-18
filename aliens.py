import pygame

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
    ship = Ship(screen)

    # Запуск основного цикла игры
    while True:
        # Отслеживание событий клавиаутры и мыши
        gf.check_events(ship)
        ship.update()
        gf.update_screen(game_settings, screen, ship)

run_game()
