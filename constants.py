import pygame as pg


# Screen
CAPTION = "rpg thing"
BASE_UNIT = 20  # ascii level files need to be 19x19
BASE_RES = BASE_UNIT * (12 + 2)  # 12 for whole lvl; +2 to include level edges
RES_MUL = 3
RESOLUTION = BASE_RES * RES_MUL
UNIT = BASE_UNIT * RES_MUL

# Player
PLAYER_IDLE = "assets/textures/player_idle.png"
PLAYER_IDLE_DEBUG = "assets/textures/player_idle_testing.png"
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

GRASS_TEXTURE = "assets/textures/tiles/grass.png"
GRASS_SPRITE = pg.transform.scale(pg.image.load(GRASS_TEXTURE), (UNIT, UNIT))

EDGE_STRAIGHT = "assets/textures/tiles/edge_straight.png"
EDGE_STRAIGHT_SPRITE = pg.transform.scale(pg.image.load(EDGE_STRAIGHT), (UNIT, UNIT))
EDGE_SINGLE = "assets/textures/tiles/edge_single.png"
EDGE_SINGLE_SPRITE = pg.transform.scale(pg.image.load(EDGE_SINGLE), (UNIT, UNIT))
# EDGE_STRAIGHT_CORNER = "assets/textures/tiles/edge_straight_corner.png"
# EDGE_STRAIGHT_CORNER_SPRITE = pg.transform.scale(pg.image.load(EDGE_STRAIGHT_CORNER), (UNIT, UNIT))
# EDGE_STRAIGHT_CORNERS = "assets/textures/tiles/edge_straight_corners.png"
# EDGE_STRAIGHT_CORNERS_SPRITE = pg.transform.scale(pg.image.load(EDGE_STRAIGHT_CORNERS), (UNIT, UNIT))
# EDGE_STRAIGHT_STRAIGHT = "assets/textures/tiles/edge_straight_straight.png"
# EDGE_STRAIGHT_STRAIGHT_SPRITE = pg.transform.scale(pg.image.load(EDGE_STRAIGHT_STRAIGHT), (UNIT, UNIT))

EDGE_CORNER = "assets/textures/tiles/edge_corner.png"
EDGE_CORNER_SPRITE = pg.transform.scale(pg.image.load(EDGE_CORNER), (UNIT, UNIT))
# EDGE_CORNERS_OPP = "assets/textures/tiles/edge_corners_opp.png"
# EDGE_CORNERS_OPP_SPRITE = pg.transform.scale(pg.image.load(EDGE_CORNERS_OPP), (UNIT, UNIT))
# EDGE_CORNERS_INL = "assets/textures/tiles/edge_corners_inl.png"
# EDGE_CORNERS_INL_SPRITE = pg.transform.scale(pg.image.load(EDGE_CORNERS_INL), (UNIT, UNIT))

EDGE_ICORNER = "assets/textures/tiles/edge_icorner.png"
EDGE_ICORNER_SPRITE = pg.transform.scale(pg.image.load(EDGE_ICORNER), (UNIT, UNIT))
# EDGE_ICORNER_CORNER = "assets/textures/tiles/edge_icorner_corner.png"
# EDGE_ICORNER_CORNER_SPRITE = pg.transform.scale(pg.image.load(EDGE_ICORNER_CORNER), (UNIT, UNIT))
#
# EDGE_END = "assets/textures/tiles/edge_end.png"
# EDGE_END_SPRITE = pg.transform.scale(pg.image.load(EDGE_END), (UNIT, UNIT))

# ASCII
ASCII_TO_SPRITE = {
    ".": GRASS_SPRITE
}

# insanity inducing edge placements
OUTLINES_STRAIGHT = {
    EDGE_STRAIGHT_SPRITE: [True, False, True, True],
    pg.transform.flip(EDGE_STRAIGHT_SPRITE, 0, 1): [False, True, True, True],
    pg.transform.rotate(EDGE_STRAIGHT_SPRITE, -90): [True, True, True, False],
    pg.transform.rotate(EDGE_STRAIGHT_SPRITE, 90): [True, True, False, True],
    EDGE_SINGLE_SPRITE: [False, False, False, False]
}

OUTLINES_CORNER = {
    EDGE_CORNER_SPRITE: [True, True, False, True],
    pg.transform.flip(EDGE_CORNER_SPRITE, 0, 1): [False, True, True, True],
    pg.transform.rotate(EDGE_CORNER_SPRITE, -90): [True, True, True, False],
    pg.transform.rotate(EDGE_CORNER_SPRITE, 180): [True, False, True, True]
}

OUTLINES_ICORNER = {
    EDGE_ICORNER_SPRITE: [True, False, False, True],
    pg.transform.flip(EDGE_ICORNER_SPRITE, 0, 1): [False, True, False, True],
    pg.transform.rotate(EDGE_ICORNER_SPRITE, -90): [True, False, True, False],
    pg.transform.rotate(EDGE_ICORNER_SPRITE, 180): [False, True, True, False]
}
