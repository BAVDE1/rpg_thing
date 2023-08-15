import pygame as pg
from rendering.rendering_other import split_sheet

# Screen
CAPTION = "rpg thing"
BASE_UNIT = 20  # ascii level files need to be 19x19
LVL_SIZE = 13
BASE_RES = BASE_UNIT * (LVL_SIZE + 1)  # 13 for whole lvl; +1 to include level edge
RES_MUL = 3  # should be whole number
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

LEAVES_TILESET = "assets/textures/tiles/leaves_tileset.png"
LEAVES_TILESET_SPRITE = pg.image.load(LEAVES_TILESET)
LEAVES_TILESET_SPRITES = split_sheet(LEAVES_TILESET_SPRITE, (20, 20), 9, 5)
print(LEAVES_TILESET_SPRITES)

# ASCII
ASCII_TO_SPRITE = {
    ".": GRASS_SPRITE
}


def get_outline_tileset_dict(tileset_sprites):
    """ Requirements orders (True=not empty tile, False=empty tile):
    [tile,      north, south, east, west,       north-east, north-west, south-east, south-west] """
    return {
        pg.transform.scale(tileset_sprites[0],   (UNIT, UNIT)): [True,   True, True, True, True,         True, True, False, True],
        pg.transform.scale(tileset_sprites[1],   (UNIT, UNIT)): [True,   True, False, True, True,        True, True, False, True],
        pg.transform.scale(tileset_sprites[2],   (UNIT, UNIT)): [True,   True, False, True, True,        True, True, False, False],
        pg.transform.scale(tileset_sprites[3],   (UNIT, UNIT)): [True,   True, False, True, True,        True, True, True, False],
        pg.transform.scale(tileset_sprites[4],   (UNIT, UNIT)): [True,   True, True, True, True,         True, True, True, False],
        pg.transform.scale(tileset_sprites[5],   (UNIT, UNIT)): [False,  False, False, False, False,     False, False, True, False],
        pg.transform.scale(tileset_sprites[6],   (UNIT, UNIT)): [False,  False, True, False, False,      False, False, True, False],
        pg.transform.scale(tileset_sprites[7],   (UNIT, UNIT)): [False,  False, True, False, False,      False, False, False, True],
        pg.transform.scale(tileset_sprites[8],   (UNIT, UNIT)): [False,  False, False, False, False,     False, False, False, True],
        pg.transform.scale(tileset_sprites[9],   (UNIT, UNIT)): [True,   True, True, False, True,        True, True, False, True],
        pg.transform.scale(tileset_sprites[10],  (UNIT, UNIT)): [False,  True, False, False, True,       True, True, False, True],
        pg.transform.scale(tileset_sprites[11],  (UNIT, UNIT)): [False,  True, False, False, False,      True, True, False, False],
        pg.transform.scale(tileset_sprites[12],  (UNIT, UNIT)): [False,  True, False, True, False,       True, True, True, False],
        pg.transform.scale(tileset_sprites[13],  (UNIT, UNIT)): [True,   True, True, True, False,        True, True, True, False],
        pg.transform.scale(tileset_sprites[14],  (UNIT, UNIT)): [False,  False, False, True, False,      False, False, True, False],
        pg.transform.scale(tileset_sprites[15],  (UNIT, UNIT)): [True,   False, True, True, False,      False, False, True, False],
        pg.transform.scale(tileset_sprites[16],  (UNIT, UNIT)): [True,   False, True, False, True,      False, False, False, True],
        pg.transform.scale(tileset_sprites[17],  (UNIT, UNIT)): [False,  False, False, False, True,      False, False, False, True],
        pg.transform.scale(tileset_sprites[18],  (UNIT, UNIT)): [True,   True, True, False, True,       False, True, False, True],
        pg.transform.scale(tileset_sprites[19],  (UNIT, UNIT)): [False,  False, False, False, True,     False, True, False, True],
        #pg.transform.scale(tileset_sprites[20],  (UNIT, UNIT)): [True,   False, False, False, False,       False, False, False, False],
        pg.transform.scale(tileset_sprites[21],  (UNIT, UNIT)): [False,  False, False, True, False,     True, False, True, False],
        pg.transform.scale(tileset_sprites[22],  (UNIT, UNIT)): [True,   True, True, True, False,       True, False, True, False],
        pg.transform.scale(tileset_sprites[23],  (UNIT, UNIT)): [False,  False, False, True, False,     True, False, False, False],
        pg.transform.scale(tileset_sprites[24],  (UNIT, UNIT)): [True,   True, False, True, False,      True, False, False, False],
        pg.transform.scale(tileset_sprites[25],  (UNIT, UNIT)): [True,   True, False, False, True,      False, True, False, False],
        pg.transform.scale(tileset_sprites[26],  (UNIT, UNIT)): [False,  False, False, False, True,     False, True, False, False],
        pg.transform.scale(tileset_sprites[27],  (UNIT, UNIT)): [True,   True, True, False, True,       False, True, True, True],
        pg.transform.scale(tileset_sprites[28],  (UNIT, UNIT)): [False,  False, True, False, True,       False, True, True, True],
        pg.transform.scale(tileset_sprites[29],  (UNIT, UNIT)): [False,  False, True, False, False,     False, False, True, True],
        pg.transform.scale(tileset_sprites[30],  (UNIT, UNIT)): [False,  False, True, True, False,       True, False, True, True],
        pg.transform.scale(tileset_sprites[31],  (UNIT, UNIT)): [True,   True, True, True, False,         True, False, True, True],
        pg.transform.scale(tileset_sprites[32],  (UNIT, UNIT)): [False,  False, False, False, False,     True, False, False, False],
        pg.transform.scale(tileset_sprites[33],  (UNIT, UNIT)): [False,  True, False, False, False,      True, False, False, False],
        pg.transform.scale(tileset_sprites[34],  (UNIT, UNIT)): [False,  True, False, False, False,      False, True, False, False],
        pg.transform.scale(tileset_sprites[35],  (UNIT, UNIT)): [False, False, False, False, False,      False, True, False, False],
        pg.transform.scale(tileset_sprites[36], (UNIT, UNIT)): [True,   True, True, True, True,         False, True, True, True],
        pg.transform.scale(tileset_sprites[37], (UNIT, UNIT)): [True,  False, True, True, True,         False, True, True, True],
        pg.transform.scale(tileset_sprites[38], (UNIT, UNIT)): [True,   False, True, True, True,         False, False, True, True],
        pg.transform.scale(tileset_sprites[39], (UNIT, UNIT)): [True,   False, True, True, True,         True, False, True, True],
        pg.transform.scale(tileset_sprites[40], (UNIT, UNIT)): [True,   True, True, True, True,         True, False, True, True],
    }
