import pygame
import sys
from sudoku_generator import generate_sudoku
from constant import *
import copy


class SudokuGame:
    def __init__(self, remove_size: int):
        """
        Initialize the Sudoku Game

        :param remove_size: Difficulty of the Sudoku game
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.selected_cell = []
        self.is_full = False
        self.sudoku_board = generate_sudoku(9, remove_size)
        self.answer_board = copy.deepcopy(self.sudoku_board)
        self.temp_board = [[0 for _ in range(9)] for _ in range(9)]

        pygame.display.set_caption("Sudoku")

    def draw_grid(self):
        """
        Draw the Sudoku grid
        """
        # draw horizontal lines
        for i in range(0, BOARD_ROWS + 1):
            if i % 3 == 0:
                width = BOX_LINE_WIDTH  # Draw box line
            else:
                width = LINE_WIDTH  # Draw regular line
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (EDGE_BLANK, i * SQUARE_SIZE + EDGE_BLANK),
                (EDGE_BLANK + SQUARE_SIZE * 9, i * SQUARE_SIZE + EDGE_BLANK),
                width
            )

        # draw vertical lines
        for i in range(0, BOARD_COLS + 1):
            if i % 3 == 0:
                width = BOX_LINE_WIDTH
            else:
                width = LINE_WIDTH
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (i * SQUARE_SIZE + EDGE_BLANK, EDGE_BLANK),
                (i * SQUARE_SIZE + EDGE_BLANK, EDGE_BLANK + SQUARE_SIZE * 9),
                width
            )

    def draw_button(self):
        """
        Draw buttons for actions (restart, reset, exit).
        """
        button_top = SCREEN_HEIGHT - 100  # All buttons share the same vertical coordinate
        restart_button_left = SCREEN_WIDTH / 2 - 250  # The x-coordinate of the left boundary of the restart button
        reset_button_left = SCREEN_WIDTH / 2 - 50  # The x-coordinate of the left boundary of the reset button
        exit_button_left = SCREEN_WIDTH / 2 + 150  # The x-coordinate of the left boundary of the exit button

        # Draw rectangles of all three buttons
        pygame.draw.rect(self.screen, BUTTON_COLOR, (restart_button_left, button_top, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(self.screen, BUTTON_COLOR, (reset_button_left, button_top, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(self.screen, BUTTON_COLOR, (exit_button_left, button_top, BUTTON_WIDTH, BUTTON_HEIGHT))

        # Put text in rectangles
        self._draw_text(BUTTON_FONT, "RESTART",
                        (restart_button_left + BUTTON_WIDTH // 2, button_top + BUTTON_HEIGHT // 2))
        self._draw_text(BUTTON_FONT, "RESET",
                        (reset_button_left + BUTTON_WIDTH // 2, button_top + BUTTON_HEIGHT // 2))
        self._draw_text(BUTTON_FONT, "EXIT",
                        (exit_button_left + BUTTON_WIDTH // 2, button_top + BUTTON_HEIGHT // 2))

    def run_game(self):
        """
        Main loop for running Sudoku game

        :return: Winning status of the game. If win return True, if full but not win return False
        """
        while True:
            restart = self._check_event()  # Check mouse clicks or key presses
            if restart:
                # If the restart button is clicked
                return GAME_RESTART  # Restart the game
            self._update_screen()  # Update the game screen
            if self._check_win():  # Check if win the game, return True when winning
                return GAME_WIN
            elif self.is_full:  # If the board is full but didn't win, return False
                return GAME_LOSE

    def _check_event(self):
        """
        Check events (e.g., mouse clicks, key presses).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If a quit event is detected,
                sys.exit()  # Exit the program
            elif event.type == pygame.MOUSEBUTTONDOWN:  # If a mouse button is pressed,
                return self._handle_mouse_click(event)  # Handle the mouse click event
            elif event.type == pygame.KEYDOWN and self.selected_cell:  # If a key is pressed and a cell is selected,
                self._handle_key_click(event)  # Handle the key press event
                return False

    def _update_screen(self):
        """
        Update the display screen with the current state of the Sudoku game.
        """
        self.screen.fill(BG_COLOR)  # Clear the screen with the background color
        self.draw_grid()  # Draw the Sudoku grid
        self.draw_button()  # Draw the action buttons
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                # Draw numbers from sudoku_board, answer_board, and temp_board
                if self.sudoku_board[row][col] != 0:
                    self._draw_number(str(self.sudoku_board[row][col]), row, col, NUM_COLOR_BLACK)
                    continue  # If not continue, all cells would be drawn as an answer number
                if self.answer_board[row][col] != 0:
                    self._draw_number(str(self.answer_board[row][col]), row, col, NUM_COLOR_BLUE)
                if self.temp_board[row][col] != 0:
                    self._draw_number(str(self.temp_board[row][col]), row, col, NUM_COLOR_RED)

        if self.selected_cell:  # Draw a border around the selected cell
            self._draw_selected_cell_border()
        pygame.display.flip()

    def _check_win(self):
        """
        Check if the game is won.

        :return: True if the game is won (all cells are filled and no duplicate numbers are found), False otherwise.
        """
        # Check if the answer board is full
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                # Check if the cell is empty
                if self.answer_board[row][col] != 0:
                    continue
                else:
                    return False
        self.is_full = True

        # Check rows and columns for duplicates
        for i in range(BOARD_ROWS):
            row_set = set()
            col_set = set()
            for j in range(BOARD_COLS):
                # Check for duplicate numbers in rows
                if self.answer_board[i][j] != 0:
                    if self.answer_board[i][j] in row_set:
                        return False
                    row_set.add(self.answer_board[i][j])

                # Check for duplicate numbers in columns
                if self.answer_board[j][i] != 0:
                    if self.answer_board[j][i] in col_set:
                        return False
                    col_set.add(self.answer_board[j][i])

        # Check 3x3 box for duplicates
        for i in range(0, BOARD_ROWS, 3):
            for j in range(0, BOARD_COLS, 3):
                box_set = set()
                for m in range(3):
                    for n in range(3):
                        num = self.answer_board[i + m][j + n]
                        if num != 0:
                            if num in box_set:
                                return False
                            box_set.add(num)
        return True

    def _handle_mouse_click(self, event):
        """
        Handle mouse clicks on the Sudoku grid.

        :param event: The pygame mouse event containing the mouse click information
        :return : Return True if the restart button is clicked, False otherwise
        """
        x, y = event.pos
        col = (x - EDGE_BLANK) // SQUARE_SIZE
        row = (y - EDGE_BLANK) // SQUARE_SIZE

        # Check if the click is outside the Sudoku grid
        if (col < 0 or col > 8) or (row < 0 or row > 8):
            # Check if the click is within the button area for actions
            if 820 < y < 870:
                if 160 < x < 260:
                    # If the click is within the RESTART button, restart the game
                    return True
                elif 360 < x < 460:
                    # If the click is within the RESET button, reset the board
                    self.answer_board = copy.deepcopy(self.sudoku_board)
                    self.temp_board = [[0 for _ in range(9)] for _ in range(9)]
                    return False
                elif 560 < x < 660:
                    # If the click is within the EXIT button, quit the game
                    pygame.quit()
                    sys.exit()
            return False

        # If a cell within the Sudoku grid is clicked, update the answer_board with the value from temp_board
        # for the selected cell
        self._auto_update_number()

        # Update the selected_cell attribute with the clicked cell coordinates
        self.selected_cell = [row, col]

    def _draw_selected_cell_border(self):
        """
        Draw a border around the selected cell.
        """
        if self.selected_cell:
            x = self.selected_cell[1] * SQUARE_SIZE + EDGE_BLANK  # Calculate the x-coordinate of the selected cell
            y = self.selected_cell[0] * SQUARE_SIZE + EDGE_BLANK  # Calculate the y-coordinate of the selected cell
            # Draw a rectangle around the selected cell with the specified color and thickness
            pygame.draw.rect(self.screen, CELL_SELECTED_COLOR, pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE), 3)

    def _handle_key_click(self, event):
        """
        Handle key presses for entering numbers into the Sudoku grid.

        :param event:The pygame key event containing the key press information.
        """
        row = self.selected_cell[0]  # Get the row index of the selected cell
        col = self.selected_cell[1]  # Get the column index of the selected cell

        # Handle arrow keys event
        if event.key == pygame.K_UP:
            if row > 0:
                self._auto_update_number()
                self.selected_cell[0] -= 1
        elif event.key == pygame.K_DOWN:
            if row < 8:
                self._auto_update_number()
                self.selected_cell[0] += 1
        elif event.key == pygame.K_LEFT:
            if col > 0:
                self._auto_update_number()
                self.selected_cell[1] -= 1
        elif event.key == pygame.K_RIGHT:
            if col < 8:
                self._auto_update_number()
                self.selected_cell[1] += 1

        # Handle entering number event
        # Check if the selected cell is empty in both the sudoku_board and answer_board
        if self.sudoku_board[row][col] == 0 and self.answer_board[row][col] == 0:
            # Check if the pressed key corresponds to a number (0-9)
            if pygame.K_0 <= event.key <= pygame.K_9:
                # Update the temp_board with the entered number for the selected cell
                self.temp_board[row][col] = int(pygame.key.name(event.key))

            # Check if the pressed key is the RETURN key
            if event.key == pygame.K_RETURN:
                # Update the answer_board with the entered number from the temp_board
                self.answer_board[row][col] = self.temp_board[row][col]
                # Reset the temp_board for the selected cell to 0
                self.temp_board[row][col] = 0
        # Check if the number to be deleted is allowed to be removed
        elif self.sudoku_board[row][col] == 0 and self.answer_board[row][col] != 0:
            if event.key == pygame.K_BACKSPACE:
                # Removed the selected number
                self.answer_board[row][col] = 0
                self.temp_board[row][col] = 0

    def _auto_update_number(self):
        # If a cell is selected by pressing the arrow keys
        if self.selected_cell and self.answer_board[self.selected_cell[0]][self.selected_cell[1]] == 0:
            # Update the answer_board with the value from temp_board for the last selected cell
            self.answer_board[self.selected_cell[0]][self.selected_cell[1]] = (
                self.temp_board)[self.selected_cell[0]][self.selected_cell[1]]
            self.temp_board[self.selected_cell[0]][self.selected_cell[1]] = 0

    def _draw_number(self, number: str, row: int, col: int, num_color: tuple):
        """
        Draw a number onto the Sudoku grid.

        :param number: The number to be drawn on the grid
        :param row: The row index of the cell where the number will be drawn
        :param col: The column index of the cell where the number will be drawn
        :param num_color: The RGB color tuple for the color of the number
        """
        num_font = pygame.font.Font(None, NUM_FONT)  # Load the font for rendering the number
        num_surf = num_font.render(number, True, num_color)  # Render the number onto a surface
        mid_x = (col * SQUARE_SIZE + EDGE_BLANK) + SQUARE_SIZE / 2  # Calculate the x-coordinate
        mid_y = (row * SQUARE_SIZE + EDGE_BLANK) + SQUARE_SIZE / 2  # Calculate the y-coordinate
        num_rect = num_surf.get_rect(center=(mid_x, mid_y))  # Get the rectangle containing the number surface
        self.screen.blit(num_surf, num_rect)  # Draw the number onto the screen at the specified position

    def _draw_text(self, font: int, text: str, text_center: tuple):
        """
        Draw text onto the screen at the specified center position.

        :param font: The font for text
        :param text: The text to be drawn on the screen
        :param text_center: The (x, y) coordinates of the center of the text
        """
        text_font = pygame.font.Font(None, font)  # Load the font for rendering the text
        text_surf = text_font.render(text, False, TEXT_COLOR)  # Render the text onto a surface
        text_rect = text_surf.get_rect(center=text_center)  # Get the rectangle containing the text surface
        self.screen.blit(text_surf, text_rect)  # Draw the text onto the screen at the specified position


class DisplayStartOver:
    """
    Class to manage display functions for the start and game over screens of a Sudoku game.
    """
    def __init__(self):
        # Initializes the game window and sets the default difficulty level.
        pygame.init()
        self.difficulty = MEDIUM  # Sets the default game difficulty to medium
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Creates the window

    def draw_game_start(self):
        """
        Draws the initial game start screen, which includes difficulty selection buttons.

        :return: (int) The selected difficulty level for the game
        """
        self.screen.fill(BG_COLOR)  # Fills the screen with a background color
        start_text = "Welcome  to  Sudoku"
        select_text = "Select  Game  Mode:"
        running = True
        button_top = SCREEN_HEIGHT - 200
        easy_button_left = SCREEN_WIDTH / 2 - 250
        medium_button_left = SCREEN_WIDTH / 2 - 50
        hard_button_left = SCREEN_WIDTH / 2 + 150

        # Draw buttons for difficulty selection
        pygame.draw.rect(self.screen, BUTTON_COLOR, (easy_button_left, button_top, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(self.screen, BUTTON_COLOR, (medium_button_left, button_top, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(self.screen, BUTTON_COLOR, (hard_button_left, button_top, BUTTON_WIDTH, BUTTON_HEIGHT))

        # Label buttons
        self._draw_text(BUTTON_FONT, "EASY", (easy_button_left + BUTTON_WIDTH // 2, button_top + BUTTON_HEIGHT // 2))
        self._draw_text(BUTTON_FONT, "MEDIUM", (medium_button_left + BUTTON_WIDTH//2, button_top + BUTTON_HEIGHT//2))
        self._draw_text(BUTTON_FONT, "HARD", (hard_button_left + BUTTON_WIDTH // 2, button_top + BUTTON_HEIGHT // 2))

        # Draw welcome text
        self._draw_text(GAME_START_FONT, start_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self._draw_text(DIFFICULTY_FONT, select_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))

        # Event loop to handle input
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if button_top < y < button_top + BUTTON_HEIGHT:  # 620 - 720
                        if easy_button_left < x < easy_button_left + BUTTON_WIDTH:
                            self.difficulty = EASY
                            running = False
                        elif medium_button_left < x < medium_button_left + BUTTON_WIDTH:
                            self.difficulty = MEDIUM
                            running = False
                        elif hard_button_left < x < hard_button_left + BUTTON_WIDTH:
                            self.difficulty = HARD
                            running = False

            pygame.display.flip()  # Update the display

        return self.difficulty

    def draw_game_over(self, is_win: bool):
        """
        Draws the game over screen.

        :param is_win: True if the player won the game, False otherwise
        """
        self.screen.fill(BG_COLOR)  # Clears the screen with a background color

        if is_win:
            end_text = "Game  Won!"
        else:
            end_text = "Game  Over  :("

        restart_text = "Press  R  to  play  the  game  again"
        exit_text = "Press  Esc  to  exit"

        # Display game over messages
        self._draw_text(GAME_OVER_FONT, end_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        self._draw_text(GAME_RESTART_FONT, restart_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self._draw_text(GAME_EXIT_FONT, exit_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))

        # Handle events and display messages
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:
                        return  # Restart the game

            pygame.display.flip()

    def _draw_text(self, font: int, text: str, text_center: tuple):
        """
        Draw text onto the screen at the specified center position.

        :param font: The font for text
        :param text: The text to be drawn on the screen
        :param text_center: The (x, y) coordinates of the center of the text
        """
        text_font = pygame.font.Font(None, font)  # Load the font for rendering the text
        text_surf = text_font.render(text, False, TEXT_COLOR)  # Render the text onto a surface
        text_rect = text_surf.get_rect(center=text_center)  # Get the rectangle containing the text surface
        self.screen.blit(text_surf, text_rect)  # Draw the text onto the screen at the specified position
