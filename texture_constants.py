from rendering.split_sheet import split_sheet
from constants import DirectionalValues
import pygame as pg


def rotate_90(sprite, rot_amt):
    """ Returns a sprite rotated by 90 * rot_amt """
    return pg.transform.rotate(sprite, 90 * rot_amt)


def single_tile(char, sprite):
    """ Generates one sprite """
    if char in ASCII_TO_SPRITE:
        raise KeyError(f"The entry '{char}' already exists in dictionary ({ASCII_TO_SPRITE})")
    ASCII_TO_SPRITE[char] = sprite


def four_way_rotated_tile(char, sprite):
    """ Generates 4 clockwise rotated sprites """
    for i in range(4):
        single_tile(f"{char}*{i}", rotate_90(sprite, -i))


def tileset_list(char, sprites: list):
    for i, sprite in enumerate(sprites):
        single_tile(f"{char}^{i}", sprite)


class TileTextures:
    """ Register new textures here """
    # SINGLE
    FADE_IMAGE = pg.image.load("assets/textures/tiles/fade_tile.png")
    GRASS_IMAGE = pg.image.load("assets/textures/tiles/grass.png")

    PLACEHOLDER_TILE = pg.image.load("assets/textures/tiles/tile_placeholder.png")
    PLACEHOLDER_DIR_TILE = pg.image.load("assets/textures/tiles/devart/dir_tile.png")

    # TIMESETS
    DARK_GRASS_TILESET_IMAGES = split_sheet("assets/textures/tiles/dark_grass_tileset.png", columns=8, rows=3, remove_end_splits=1)
    GRASS_WALLS_TILESET_IMAGES = split_sheet("assets/textures/tiles/grass_walls_tileset.png", columns=8, rows=3, remove_end_splits=1)

    # OUTLINES TILESET
    LEAVES_TILESET_IMAGES = split_sheet("assets/textures/tiles/leaves_tileset.png", columns=5, rows=5)


def register_tiles():
    """ Register new tiles here """
    single_tile('Gr', TileTextures.GRASS_IMAGE)
    tileset_list('Dg', TileTextures.DARK_GRASS_TILESET_IMAGES)
    tileset_list('Gw', TileTextures.GRASS_WALLS_TILESET_IMAGES)

    # placeholders
    four_way_rotated_tile('Dt', TileTextures.PLACEHOLDER_DIR_TILE)
    single_tile('Pt', TileTextures.PLACEHOLDER_TILE)


ASCII_TO_SPRITE = {}
register_tiles()


class RenderValues:
    SHADOW_ALPHA = 100
    SHADOW_QUALITY_MIN = 1
    SHADOW_QUALITY_MAX = 5
    SHADOW_QUALITY: int = 5  # the higher the number, the better quality but is harder on performance


class PlayerTextures:
    PLAYER_IDLE = "assets/textures/player/player_idle.png"
    PLAYER_JUMP_HORIZONTAL = "assets/textures/player/player_jump_horizontal.png"
    PLAYER_JUMP_HORIZONTAL_STUNTED = "assets/textures/player/player_jump_horizontal_stunted.png"
    PLAYER_JUMP_VERTICAL = "assets/textures/player/player_jump_vertical.png"
    PLAYER_JUMP_VERTICAL_STUNTED = "assets/textures/player/player_jump_vertical_stunted.png"
    PLAYER_IDLE_DEBUG = "assets/textures/player/player_idle_debug.png"


class EntityTextures:
    PLACEHOLDER = PlayerTextures.PLAYER_IDLE


def get_outline_tileset_dict(tileset_sprites):
    """ MUST be in order from the most amount of requirements to least (True=has tile, False=empty tile)"""
    t = DirectionalValues.TILE
    n, s, e, w = DirectionalValues.NORTH, DirectionalValues.SOUTH, DirectionalValues.EAST, DirectionalValues.WEST
    ne, nw, se, sw = DirectionalValues.NORTH_EAST, DirectionalValues.NORTH_WEST, DirectionalValues.SOUTH_EAST, DirectionalValues.SOUTH_WEST
    return {
        # corner (3r)
        tileset_sprites[0]: {t: True, s: True, e: True, se: False},
        rotate_90(tileset_sprites[0], 1): {t: True, n: True, e: True, ne: False},
        rotate_90(tileset_sprites[0], 2): {t: True, n: True, w: True, nw: False},
        rotate_90(tileset_sprites[0], 3): {t: True, s: True, w: True, sw: False},
        tileset_sprites[11]: {t: False, n: False, w: False, nw: True},
        rotate_90(tileset_sprites[11], 1): {t: False, s: False, w: False, sw: True},
        rotate_90(tileset_sprites[11], 2): {t: False, s: False, e: False, se: True},
        rotate_90(tileset_sprites[11], 3): {t: False, n: False, e: False, ne: True},

        # inside corner (2r)
        tileset_sprites[5]: {t: True, s: False, e: False},
        rotate_90(tileset_sprites[5], 1): {t: True, n: False, e: False},
        rotate_90(tileset_sprites[5], 2): {t: True, n: False, w: False},
        rotate_90(tileset_sprites[5], 3): {t: True, s: False, w: False},
        tileset_sprites[6]: {t: False, n: True, w: True},
        rotate_90(tileset_sprites[6], 1): {t: False, s: True, w: True},
        rotate_90(tileset_sprites[6], 2): {t: False, s: True, e: True},
        rotate_90(tileset_sprites[6], 3): {t: False, n: True, e: True},

        # straight (1r)
        tileset_sprites[1]: {t: True, s: False},
        rotate_90(tileset_sprites[1], 1): {t: True, e: False},
        rotate_90(tileset_sprites[1], 2): {t: True, n: False},
        rotate_90(tileset_sprites[1], 3): {t: True, w: False},
        tileset_sprites[10]: {t: False, n: True},
        rotate_90(tileset_sprites[10], 1): {t: False, w: True},
        rotate_90(tileset_sprites[10], 2): {t: False, s: True},
        rotate_90(tileset_sprites[10], 3): {t: False, e: True},
    }
