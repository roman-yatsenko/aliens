import pygame.font

class Scoreboard():
    """Класс для вывода игровой информации"""
    def __init__(self, game_settings, screen, stats):
        """ Инициализирует атрибуты подсчета очков"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game_settings = game_settings
        self.stats = stats

        # Настройки шрифта для вывода счета
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Подготовка исходного изображения
        self.prep_score()