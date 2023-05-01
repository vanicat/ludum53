import arcade 

SCREEN_TITLE = "Before the black water"

STARTING_MONEY = 500
STARTING_FUEL = 1000

# Size of screen to show, in pixels
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 768
TILE_SIZE = 32
BOAT_VIEW_SCALLING = 7

# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 0.7
PLAYER_DAMPING = 0.98
# Friction between objects
PLAYER_FRICTION = 5
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6

# Mass (defaults to 1)
PLAYER_MASS = 2.0

# Keep player from going too fast
PLAYER_MAX_SPEED = 450
ADV_FORCE = 80 
DRAG_FORCE = 80
DERIVE_FORCE = 10

BARRE_SPEED = 2.5
MAX_BARRE = 290 # doit être divisble par BARRE_SPEED, idéalement en calcul exacte


RED = arcade.color_from_hex_string("#950A0A")
SELECTED = arcade.color_from_hex_string("#1023A1")


LOCAL_MULT_PRICE = 0.5
DIST_MULT_PRICE = 2
DIST_MULT_REDUCE = 0.9

LOCAL_PROB_MULT = 2

def myround(x):
    return round(x * 4)/4