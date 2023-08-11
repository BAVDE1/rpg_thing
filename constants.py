import pygame as pg


# Screen
CAPTION = "rpg thing"
BASE_UNIT = 20  # ascii level files need to be 19x19
BASE_RES = BASE_UNIT * (12 + 2)  # 12 for whole lvl; +2 to include level edges
RES_MUL = 2
RESOLUTION = BASE_RES * RES_MUL
UNIT = BASE_UNIT * RES_MUL

# Player
PLAYER_IDLE = "assets/textures/player_idle.png"
MOVEMENT_PAUSE = 0.15  # 0.15
HOLD_TIME_TO_SPRINT = 0.5

UP = "u"
DOWN = "d"
LEFT = "l"
RIGHT = "r"

OPP_DIR = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}

DIRECTION_DICT = {
    **dict.fromkeys([pg.K_w, pg.K_UP], UP),
    **dict.fromkeys([pg.K_s, pg.K_DOWN], DOWN),
    **dict.fromkeys([pg.K_a, pg.K_LEFT], LEFT),
    **dict.fromkeys([pg.K_d, pg.K_RIGHT], RIGHT),
}

# [0]: x, [1]: y
DIRECTION_MOV = {
    UP: (0, -UNIT),
    DOWN: (0, UNIT),
    LEFT: (-UNIT, 0),
    RIGHT: (UNIT, 0)
}

# Rendering
SHADOW_ALPHA = 50  # 0 - 255
SHADOW_WIDTH = 0.8  # %
SHADOW_HEIGHT = 0.4  # %

# Levels
OVERWORLD = "assets/levels/overworld.txt"
OVERWORLD_00 = "assets/levels/overworld_0.txt"
OVERWORLD_01 = "assets/levels/overworld_1.txt"


# -------------------->
# Texture Loader
# -------------------->

GRASS_TEXTURE = "assets/textures/grass.png"
GRASS_SPRITE = pg.transform.scale(pg.image.load(GRASS_TEXTURE), (UNIT, UNIT))


# ASCII
ASCII = {
    ".": GRASS_SPRITE
}
