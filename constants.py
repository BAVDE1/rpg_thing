import pygame as pg


# Screen
CAPTION = "rpg thing"
BASE_RES = 288  # 256 + 32 for edges
BASE_UNIT = 16  # ascii files need to be 19x19
RES_MUL = 2
RESOLUTION = BASE_RES * RES_MUL
UNIT = BASE_UNIT * RES_MUL

# Player
PLAYER_TEXTURE = "assets/textures/player_new.png"
MOVEMENT_PAUSE = 1  # 0.15
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

DIR_DICT = {
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

# Render
SHADOW_ALPHA = 50  # 0 - 255
SHADOW_WIDTH = 0.6  # %
SHADOW_HEIGHT = 0.4  # %

# Textures
GRASS_TEXTURE = "assets/textures/grass.png"
GRASS_01_TEXTURE = "assets/textures/grass_1.png"
GRASS_02_TEXTURE = "assets/textures/grass_2.png"
GRASS_03_TEXTURE = "assets/textures/grass_3.png"
GRASS_04_TEXTURE = "assets/textures/grass_4.png"

# Levels
OVERWORLD = "assets/levels/overworld.txt"
OVERWORLD_00 = "assets/levels/overworld_0.txt"
OVERWORLD_01 = "assets/levels/overworld_1.txt"
