import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

def run_game():
    # Инициализирует игру и создает объект экрана
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(
        (game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("Aliens")

    # Создание кнопки Play
    play_button = Button(game_settings, screen, "Play")

    # Создание экземпляра для хранения игровой статистики
    stats = GameStats(game_settings)
    sb = Scoreboard(game_settings, screen, stats)

    # Создание корабля
    ship = Ship(game_settings, screen)
    
    # Создание группы для хранения пуль
    bullets = Group()

    # Создание пришельцев
    aliens = Group()

    # Создание флота пришельцев
    gf.create_fleet(game_settings, screen, ship, aliens)

    # Запуск основного цикла игры
    while True:
        # Отслеживание событий клавиаутры и мыши
        gf.check_events(game_settings, screen, stats, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(game_settings, screen, ship, aliens, bullets)
            gf.update_aliens(game_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(game_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()
