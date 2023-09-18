import pygame as pg

EDITING_TAG = " - editing"


# Screen
class GameUnits:
    CAPTION = "rpg thing"
    LVL_WIDTH = 14  # 13 for whole lvl; +1 to include level edge (+0.5 for each edge)
    LVL_HEIGHT = 14
    UNIT = 20  # ascii level files need to be 19x19
    RES_MUL: int = 2  # must be whole number  (3 has average of 200fps)

    RES_H = UNIT * LVL_HEIGHT
    SIDE_GIVE = RES_H * .75  # give amount beside the level
    RES_W = RES_H + SIDE_GIVE
    
    LEVEL_OFFSET = SIDE_GIVE * .5


class DirectionalValues:
    UP = "dir_up"
    DOWN = "dir_down"
    LEFT = "dir_left"
    RIGHT = "dir_right"

    TILE = "tile_t"

    NORTH = "dir_n"
    SOUTH = "dir_s"
    EAST = "dir_e"
    WEST = "dir_w"

    NORTH_EAST = "dir_ne"
    NORTH_WEST = "dir_nw"
    SOUTH_EAST = "dir_se"
    SOUTH_WEST = "dir_sw"

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
        UP: (0, -GameUnits.UNIT),
        DOWN: (0, GameUnits.UNIT),
        LEFT: (-GameUnits.UNIT, 0),
        RIGHT: (GameUnits.UNIT, 0)
    }


class PlayerValues:
    MOVEMENT_PAUSE = .15  # 0.15
    HOLD_TIME_TO_SPRINT = .2

    PLAYER_MOVE_ANIM_SPEED = .125  # .125


# TEMPORARY
class LevelLocations:
    OVERWORLD = "assets/levels/overworld/overworld.txt"
    OVERWORLD_00 = "assets/levels/overworld/overworld_00.txt"
    OVERWORLD_01 = "assets/levels/overworld/overworld_01.txt"
