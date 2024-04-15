from sudokuGame import *

if __name__ == '__main__':
    while True:
        game_start_screen = DisplayStartOver()
        difficulty = game_start_screen.draw_game_start()  # Display game start screen and return the difficulty
        sudoku = SudokuGame(difficulty)  # Start the game with specific difficulty
        game_status = sudoku.run_game()  # sudoku.run_game() return True if game win, False otherwise
        if game_status == GAME_RESTART:  # Game restart
            continue
        game_end_screen = DisplayStartOver()
        game_end_screen.draw_game_over(game_status)  # Display game end screen
