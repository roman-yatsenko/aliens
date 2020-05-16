import game_functions as gf

def run_game():
    gf.init_game()

    # Запуск основного цикла игры
    while True:
        # Отслеживание событий клавиаутры и мыши
        gf.check_events()
        # Обновление игровых объектов и экрана
        gf.update_game_objects()
        gf.update_screen()

run_game()
