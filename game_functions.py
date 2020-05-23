import sys
from time import sleep

import pygame
# from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from hud import Hud
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

# Глобальные объекты
game_settings = Settings()
screen = None
play_button = None    
hud = None
ship = None
bullets = None
aliens = None

# Создание экземпляра для хранения игровой статистики
stats = GameStats(game_settings)

def init_game():
    """ Инициализирует игру и создает объект экрана"""
    pygame.init()
    global screen
    screen = pygame.display.set_mode(
        (game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("Aliens")

    # Создание кнопки Play
    global play_button
    play_button = Button(game_settings, screen, "Play")

    global hud
    hud = Hud(game_settings, screen, stats)

    # Создание корабля
    global ship
    ship = Ship(game_settings, screen)

    # Создание группы для хранения пуль
    global bullets
    bullets = pygame.sprite.Group()

    # Создание пришельцев
    global aliens
    aliens = pygame.sprite.Group()

    # Создание флота пришельцев
    create_fleet()

def check_keydown_events(event):
    """Реагирует на нажатие клавиш"""
    if stats.game_active:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            fire_bullet()    
    if event.key == pygame.K_q:
        stats.save_high_score()
        sys.exit()

def fire_bullet():
    """ Выпускает пулю, если максимум еще не достигнут"""
    # Создание новой пули и включение ее в группу bullets
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event):
    """Реагирует на отпускание клавиш """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events():
    """Обрабатывает нажатия клавиш и события мыши"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.save_high_score()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(mouse_x, mouse_y)

def check_play_button(mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс игровых настроек
        game_settings.initialize_dynamic_settings()
        # Указатель мыши скрывается
        pygame.mouse.set_visible(False)
        # Сброс игровой статистики
        stats.reset_stats()
        hud.prep_score()
        hud.prep_level()
        hud.prep_ships()
        stats.game_active = True
        # Очистка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре
        create_fleet()
        ship.center_ship()

def update_screen():
    """Обновляет изображения на экране и отображает новый экран"""
    # При каждом проходе цикла перерисовывается экран
    screen.fill(game_settings.bg_color)
    # Все пули выводятся позади изображений корабля и пришельцев
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Вывод счета
    hud.show_score()

    # Кнопка Play отображается в том случае, если игра неактивна
    if not stats.game_active:
        play_button.draw_button()

    # Отображение последнего прорисованного экрана
    pygame.display.flip()

def update_bullets():
    """ Обновляет позиции пуль и уничтожает старые пули"""
    bullets.update()

    # Удаление пуль вышедших за край экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions()

def check_bullet_alien_collisions():    
    """ Обработка коллизий пуль с пришельцами"""
    # Проверка попаданий в пришельцев
    # при обнаружении попадания удалить пулю и пришельца
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for hit_aliens in collisions.values():
            stats.score += game_settings.alien_points * len(hit_aliens)
        hud.prep_score()
        check_high_score()
    if len(aliens) == 0:
        # Уничтожение существующих пуль, повышение скорости и создание нового флота
        bullets.empty()
        # Увеличение уровня
        stats.level += 1
        hud.prep_level()
        game_settings.increase_speed()
        create_fleet()

def get_number_aliens_x(alien_width):
    """ Вычисляет количество пришельцев в ряду"""
    available_space_x = game_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def get_number_rows(ship_height, alien_height):
    """ Определяет количество рядов, помещающихся на экране"""
    available_space_y = (game_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(alien_number, row_number):
    """ Создает пришельца и размещает его в ряду"""
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet():
    """ Создает флот пришельцев"""
    # Создание пришельца и вычисление количества пришельцев в ряду
    # Интервал между соседними пришельцами равен одной ширине пришелшьца

    alien = Alien(game_settings, screen)
    number_aliens_x = get_number_aliens_x(alien.rect.width)
    number_rows = get_number_rows(ship.rect.height, alien.rect.height)

    # Создание первого ряда пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Создание пришельца и размещеение его в ряду
            create_alien(alien_number, row_number)        

def check_fleet_edges():
    """ Реагирует на достижение флотом края экрана"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction()
            break

def change_fleet_direction():
    """ Опускает фесь флот и меняет направление флота"""
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1

def check_aliens_bottom():
    """ Проверяет, доьрались ли пришельцы до нижнего края экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же, что и при столкновении с кораблем
            ship_hit()
            break

def update_aliens():
    """ Обновляет позиции всех пришельцев во флоте"""
    check_fleet_edges()
    aliens.update()

    # Проверка коллизий "пришелец-корабль"
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit()

     # Проверка пришельцев, до бравшихся до нижнего края экрана
    check_aliens_bottom()   

def ship_hit():
    """ Обрабатывает столкновение корабля с пришельцем"""
    if stats.ships_left > 0:
        # Уменьшение ships_left
        stats.ships_left -= 1
        hud.prep_ships()

        # Очистка спсика пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре
        create_fleet()
        ship.center_ship()

        # Пауза
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_game_objects():
    """ Обновление игровых объектов"""
    if stats.game_active:
        ship.update()
        update_bullets()
        update_aliens()

def check_high_score():
    """проверяет, появился ли новый рекорд"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        hud.prep_high_score()