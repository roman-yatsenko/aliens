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

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, 
            self.game_settings.bg_color)

        # Вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        sef.score_rect.top = 20