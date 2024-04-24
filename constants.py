import pygame as pg

EDITING_TAG = " - editing"


class GameUnits:
    CAPTION = "rpg thing"
    LVL_WIDTH = 14  # +1 to include level edge (+0.5 for each edge)
    LVL_HEIGHT = 14
    UNIT = 20  # ascii level files need to be 19x19
    RES_MUL: int = 2  # must be whole number  (3 has average of 200fps)

    RES_H = UNIT * LVL_HEIGHT
    SIDE_GIVE = RES_H * .75  # give amount beside the level
    RES_W = RES_H + SIDE_GIVE

    LEVEL_X_OFFSET = SIDE_GIVE * .5
    LEVEL_OFFSET = -(UNIT / 2)

    ENTITY_Y_OFFSET = -8


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

    OPPOSITE_DIR = {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT,

        NORTH: SOUTH,
        SOUTH: NORTH,
        EAST: WEST,
        WEST: EAST,

        NORTH_EAST: SOUTH_WEST,
        SOUTH_WEST: NORTH_EAST,
        NORTH_WEST: SOUTH_EAST,
        SOUTH_EAST: NORTH_WEST
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

    LEVEL_EDGE_Y = {
        0: NORTH,
        GameUnits.LVL_HEIGHT: SOUTH,
    }

    LEVEL_EDGE_X = {
        0: WEST,
        GameUnits.LVL_WIDTH: EAST
    }


class PlayerValues:
    BEAT_GIVE_BEFORE = 0.14  # time given to perform an action on either side of a beat
    BEAT_GIVE_AFTER = 0.14

    MOVEMENT_PAUSE = .15  # 0.15
    HOLD_TIME_TO_SPRINT = .2

    PLAYER_MOVE_ANIM_SPEED = .125  # .125

    LVL_CHANGE_DIR_TO_POS = {
        DirectionalValues.NORTH: pg.Vector2(0, 13),
        DirectionalValues.SOUTH: pg.Vector2(0, 1),
        DirectionalValues.EAST: pg.Vector2(1, 0),
        DirectionalValues.WEST: pg.Vector2(13, 0)
    }


# TEMPORARY
class LevelLocations:
    LEVEL_LAYER_SEPERATOR = "*"
    OVERWORLD = "assets/areas/overworld/overworld.txt"
    OVERWORLD_00 = "assets/areas/overworld/overworld_00.txt"
    OVERWORLD_01 = "assets/areas/overworld/overworld_01.txt"
