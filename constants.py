import pygame as pg
from rendering.rendering_other import split_sheet

# Screen
CAPTION = "rpg thing"
LVL_SIZE = 13 + 1  # 13 for whole lvl; +1 to include level edge (+0.5 for each edge)
BASE_UNIT = 20  # ascii level files need to be 19x19
BASE_RES = BASE_UNIT * LVL_SIZE
RES_MUL = 3  # should be whole number

RESOLUTION_X = BASE_RES * RES_MUL
SIDE_GIVE = RESOLUTION_X * 0.75  # give amount beside the level
RESOLUTION_Y = RESOLUTION_X + SIDE_GIVE
LEVEL_OFFSET = SIDE_GIVE * 0.5
UNIT = BASE_UNIT * RES_MUL

# Player
PLAYER_IDLE = "assets/textures/player_idle.png"
PLAYER_JUMP = "assets/textures/player_jump.png"
PLAYER_IDLE_DEBUG = "assets/textures/player_idle_debug.png"
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
OVERWORLD = "assets/levels/overworld/overworld.txt"
OVERWORLD_00 = "assets/levels/overworld/overworld_00.txt"
OVERWORLD_01 = "assets/levels/overworld/overworld_01.txt"


# -------------------->
# Texture Loader
# -------------------->

TILE = "t"
NORTH = "n"
SOUTH = "s"
EAST = "e"
WEST = "w"
NORTH_EAST = "ne"
NORTH_WEST = "nw"
SOUTH_EAST = "se"
SOUTH_WEST = "sw"

FADE_TEXTURE = "assets/textures/tiles/fade_tile.png"
FADE_SPRITE = pg.transform.scale(pg.image.load(FADE_TEXTURE), (UNIT, UNIT))

GRASS_TEXTURE = "assets/textures/tiles/grass.png"
GRASS_SPRITE = pg.transform.scale(pg.image.load(GRASS_TEXTURE), (UNIT, UNIT))

LEAVES_TILESET = "assets/textures/tiles/leaves_tileset.png"
LEAVES_TILESET_SPRITE = pg.image.load(LEAVES_TILESET)
LEAVES_TILESET_SPRITES = split_sheet(LEAVES_TILESET_SPRITE, (20, 20), 5, 5)

# ASCII
ASCII_TO_SPRITE = {
    "Gr": GRASS_SPRITE
}


def get_outline_tileset_dict(tileset_sprites):
    """ MUST be in order from the most amount of requirements to least (True=has tile, False=empty tile)"""
    return {
        # corner (3r)
        pg.transform.scale(tileset_sprites[0], (UNIT, UNIT)): {TILE: True, SOUTH: True, EAST: True, SOUTH_EAST: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[0], (UNIT, UNIT)), -90): {TILE: True, SOUTH: True, WEST: True, SOUTH_WEST: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[0], (UNIT, UNIT)), 180): {TILE: True, NORTH: True, WEST: True, NORTH_WEST: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[0], (UNIT, UNIT)), 90): {TILE: True, NORTH: True, EAST: True, NORTH_EAST: False},
        pg.transform.scale(tileset_sprites[11], (UNIT, UNIT)): {TILE: False, NORTH: False, WEST: False, NORTH_WEST: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[11], (UNIT, UNIT)), -90): {TILE: False, NORTH: False, EAST: False, NORTH_EAST: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[11], (UNIT, UNIT)), 180): {TILE: False, SOUTH: False, EAST: False, SOUTH_EAST: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[11], (UNIT, UNIT)), 90): {TILE: False, SOUTH: False, WEST: False, SOUTH_WEST: True},

        # inside corner (2r)
        pg.transform.scale(tileset_sprites[5], (UNIT, UNIT)): {TILE: True, SOUTH: False, EAST: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[5], (UNIT, UNIT)), -90): {TILE: True, SOUTH: False, WEST: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[5], (UNIT, UNIT)), 180): {TILE: True, NORTH: False, WEST: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[5], (UNIT, UNIT)), 90): {TILE: True, NORTH: False, EAST: False},
        pg.transform.scale(tileset_sprites[6], (UNIT, UNIT)): {TILE: False, NORTH: True, WEST: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[6], (UNIT, UNIT)), -90): {TILE: False, NORTH: True, EAST: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[6], (UNIT, UNIT)), 180): {TILE: False, SOUTH: True, EAST: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[6], (UNIT, UNIT)), 90): {TILE: False, SOUTH: True, WEST: True},

        # straight (1r)
        pg.transform.scale(tileset_sprites[1], (UNIT, UNIT)): {TILE: True, SOUTH: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[1], (UNIT, UNIT)), -90): {TILE: True, WEST: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[1], (UNIT, UNIT)), 180): {TILE: True, NORTH: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[1], (UNIT, UNIT)), 90): {TILE: True, EAST: False},
        pg.transform.scale(tileset_sprites[10], (UNIT, UNIT)): {TILE: False, NORTH: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[10], (UNIT, UNIT)), -90): {TILE: False, EAST: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[10], (UNIT, UNIT)), 180): {TILE: False, SOUTH: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[10], (UNIT, UNIT)), 90): {TILE: False, WEST: True},
    }
