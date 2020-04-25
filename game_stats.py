class GameStats():
    """ Отслеживание статистики для игры"""

    def __init__(self, game_settings):
        """ Инициализирует статистику"""
        self.game_settings = game_settings
        self.reset_stats()

    def reset_stats(self):
        """ Инициализирует статистику, изменяющуюся в ходе игры"""
        self.ships_left = self.game_settings.ship_limit
        