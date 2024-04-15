# Board
SCREEN_WIDTH = 820  # EDGE_BLANK + (SQUARE_SIZE * 9) + EDGE_BLANK
SCREEN_HEIGHT = 920  # EDGE_BLANK + (SQUARE_SIZE * 9) + EDGE_BLANK + 100
EDGE_BLANK = 50
BOARD_ROWS = 9
BOARD_COLS = 9
SQUARE_SIZE = 80
LINE_WIDTH = 2  # Regular line width
BOX_LINE_WIDTH = 5  # Box line width

# Button size
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

# Color
BG_COLOR = (230, 230, 230)  # Background color
LINE_COLOR = (0, 0, 0)  # All line color
NUM_COLOR_RED = (255, 0, 0)  # Color of temporary number
NUM_COLOR_BLACK = (0, 0, 0)  # Color of question number
NUM_COLOR_BLUE = (0, 0, 255)  # Color of answer number
CELL_SELECTED_COLOR = (255, 0, 0)
BUTTON_COLOR = (255, 128, 0)  # All button number
TEXT_COLOR = (0, 0, 0)  # Text color in button/start screen/end screen

# Font
NUM_FONT = 50  # Font for numbers in cell
GAME_START_FONT = 80
DIFFICULTY_FONT = 50
GAME_OVER_FONT = 80
GAME_RESTART_FONT = 40
GAME_EXIT_FONT = 40
BUTTON_FONT = 30

# Difficulty
EASY = 30
MEDIUM = 40
HARD = 50

# Determine if win
GAME_LOSE = 0
GAME_WIN = 1
GAME_RESTART = 2
