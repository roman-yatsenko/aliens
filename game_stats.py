HIGH_SCORE_FILENAME = 'high_score.dat'
class GameStats():
    """ Отслеживание статистики для игры"""

    def __init__(self, game_settings):
        """ Инициализирует статистику"""
        self.game_settings = game_settings
        self.reset_stats()

        # Игра запускается в неактивном состоянии
        self.game_active = False

        # Рекорд не должен сбрасываться
        self.high_score = 0
        
    def reset_stats(self):
        """ Инициализирует статистику, изменяющуюся в ходе игры"""
        self.ships_left = self.game_settings.ship_limit
        self.score = 0
        self.level = 1
    
    def save_high_score(self):
        """ Сохраняет рекорд в файл"""
        with open(HIGH_SCORE_FILENAME, 'w') as file:
            file.write(str(self.high_score))
