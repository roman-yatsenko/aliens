import sys

import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, game_settings, screen, ship, bullets):
    """Реагирует на нажатие клавиш"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_settings, screen, ship, bullets)    
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(game_settings, screen, ship, bullets):
    """ Выпускает пулю, если максимум еще не достигнут"""
    # Создание новой пули и включение ее в группу bullets
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(game_settings, screen, ship, bullets):
    """Обрабатывает нажатия клавиш и события мыши"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_screen(game_settings, screen, ship, aliens, bullets):
    """Обновляет изображения на экране и отображает новый экран"""
    # При каждом проходе цикла перерисовывается экран
    screen.fill(game_settings.bg_color)
    # Все пули выводятся позади изображений корабля и пришельцев
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # Отображение последнего прорисованного экрана
    pygame.display.flip()

def update_bullets(bullets):
    """ Обновляет позиции пуль и уничтожает старые пули"""
    bullets.update()

    # Удаление пуль вышедших за край экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def create_fleet(game_settings, screen, aliens):
    """ Создает флот пришельцев"""
    # Создание пришельца и вычисление количества пришельцев в ряду
    # Интервал между соседними пришельцами равен одной ширине пришелшьца

    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    available_space_x = game_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))

    # Создание первого ряда пришельцев
    for alien_number in range(number_alien_x):
        # Создание пришельца и размещеение его в ряду
        alien = Alien(game_settings, screen)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        aliens.add(alien)
        