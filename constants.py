"""
Constants and Configuration for Nobita's Late Dash
All game parameters, colors, costs, and settings in one place
"""

# ============================================================================
# SCREEN SETTINGS
# ============================================================================
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60
GAME_TITLE = "Nobita's Late Dash!"

# ============================================================================
# GRID SETTINGS
# ============================================================================
GRID_ROWS = 15
GRID_COLS = 20
CELL_SIZE = 40
GRID_OFFSET_X = 50
GRID_OFFSET_Y = 100

# ============================================================================
# COLORS (RGB)
# ============================================================================
# Basic colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

# Entity colors
COLOR_NOBITA = (0, 100, 255)  # Blue
COLOR_SCHOOL = (0, 200, 0)    # Green
COLOR_GIAN = (255, 50, 50)    # Red
COLOR_WALL = (80, 80, 80)     # Dark gray
COLOR_EMPTY = (245, 245, 245) # Off-white

# Gadget colors
COLOR_BAMBOO = (255, 200, 0)  # Yellow/Gold
COLOR_DOOR = (200, 0, 200)    # Purple

# Path visualization
COLOR_PATH = (0, 255, 255)       # Cyan
COLOR_EXPLORED = (200, 220, 255) # Light blue
COLOR_CURRENT = (255, 165, 0)    # Orange

# UI colors
COLOR_BG = (230, 230, 250)       # Lavender
COLOR_TEXT = (20, 20, 20)
COLOR_SUCCESS = (0, 180, 0)
COLOR_DANGER = (220, 0, 0)

# ============================================================================
# MOVEMENT COSTS
# ============================================================================
BASE_COST = 1.0
DIAGONAL_COST = 1.414  # sqrt(2)
WALL_COST = float('inf')
GIAN_PROXIMITY_COST = 3.0  # Extra cost near Gian

# Gadget effects
BAMBOO_SPEED_MULTIPLIER = 0.5   # 50% faster (half cost)
BAMBOO_DURATION = 10            # Number of moves
ANYWHERE_DOOR_COST = 1          # Cost to use door
DOOR_MAX_USES = 1               # Number of uses per door

# ============================================================================
# GIAN PATROL SETTINGS
# ============================================================================
GIAN_SPEED = 0.5               # Cells per second
GIAN_PATROL_PAUSE = 2.0        # Seconds to pause at waypoints
GIAN_DANGER_RADIUS = 2         # Cells around Gian that are dangerous
GIAN_CATCH_RADIUS = 1          # Distance at which Gian catches Nobita

# ============================================================================
# GAME STATES
# ============================================================================
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PATHFINDING = "pathfinding"
STATE_MOVING = "moving"
STATE_PAUSED = "paused"
STATE_WON = "won"
STATE_LOST = "lost"

# ============================================================================
# CELL TYPES
# ============================================================================
CELL_EMPTY = 0
CELL_WALL = 1
CELL_NOBITA = 2
CELL_SCHOOL = 3
CELL_GIAN = 4
CELL_BAMBOO = 5
CELL_DOOR = 6

# ============================================================================
# ANIMATION SETTINGS
# ============================================================================
MOVEMENT_SPEED = 0.2           # Seconds per cell move
PATH_ANIMATION_DELAY = 0.05    # Delay between showing path cells
EXPLORATION_ANIMATION = True   # Show A* exploration visually

# ============================================================================
# UI SETTINGS
# ============================================================================
FONT_SIZE_TITLE = 48
FONT_SIZE_LARGE = 32
FONT_SIZE_MEDIUM = 24
FONT_SIZE_SMALL = 18
STATUS_BAR_HEIGHT = 80
MENU_BUTTON_WIDTH = 200
MENU_BUTTON_HEIGHT = 50

# ============================================================================
# CONTROLS
# ============================================================================
KEY_UP = 'up'
KEY_DOWN = 'down'
KEY_LEFT = 'left'
KEY_RIGHT = 'right'
KEY_SPACE = 'space'
KEY_R = 'r'
KEY_ESC = 'escape'
KEY_P = 'p'

# ============================================================================
# SOUND SETTINGS (for future implementation)
# ============================================================================
SOUND_ENABLED = False
SOUND_VOLUME = 0.7
