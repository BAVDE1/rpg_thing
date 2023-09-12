from rendering.split_sheet import split_sheet
from constants import GameUnits, DirectionalValues
import pygame as pg


def rotate_90(sprite, rot_amt):
    """ Returns a sprite rotated by 90 * rot_amt """
    return pg.transform.rotate(sprite, 90 * rot_amt)


def single_tile(char, sprite):
    """ Generates one sprite """
    ASCII_TO_SPRITE[char] = sprite


def four_way_rotated_tiles(char, sprite):
    """ Generates 4 clockwise rotated sprites """
    for i in range(4):
        ASCII_TO_SPRITE[f"{char}*{i}"] = rotate_90(sprite, -i)


class TileTextures:
    """ Register new textures here """
    FADE_SPRITE = pg.image.load("assets/textures/tiles/fade_tile.png")

    GRASS_SPRITE = pg.image.load("assets/textures/tiles/grass.png")

    DEV_TILE = pg.image.load("assets/textures/tiles/devart/dir_tile.png")

    LEAVES_TILESET_SPRITE = pg.image.load("assets/textures/tiles/leaves_tileset.png")
    LEAVES_TILESET_SPRITES = split_sheet(LEAVES_TILESET_SPRITE, (20, 20), 5, 5)


def register_tiles():
    """ Register new tiles here """
    single_tile('Gr', TileTextures.GRASS_SPRITE)

    four_way_rotated_tiles('Dt', TileTextures.DEV_TILE)


ASCII_TO_SPRITE = {}
register_tiles()


class RenderValues:
    SHADOW_ALPHA = 100
    SHADOW_QUALITY_MIN = 1
    SHADOW_QUALITY_MAX = 5
    SHADOW_QUALITY: int = 5  # the higher the number, the better quality but is harder on performance


class PlayerTextures:
    PLAYER_IDLE = "assets/textures/player_idle.png"
    PLAYER_JUMP_HORIZONTAL = "assets/textures/player_jump_horizontal.png"
    PLAYER_JUMP_VERTICAL = "assets/textures/player_jump_vertical.png"
    PLAYER_IDLE_DEBUG = "assets/textures/player_idle_debug.png"


def get_outline_tileset_dict(tileset_sprites):
    """ MUST be in order from the most amount of requirements to least (True=has tile, False=empty tile)"""
    return {
        # corner (3r)
        tileset_sprites[0]: {DirectionalValues.TILE: True, DirectionalValues.SOUTH: True, DirectionalValues.EAST: True, DirectionalValues.SOUTH_EAST: False},
        rotate_90(tileset_sprites[0], 1): {DirectionalValues.TILE: True, DirectionalValues.NORTH: True, DirectionalValues.EAST: True, DirectionalValues.NORTH_EAST: False},
        rotate_90(tileset_sprites[0], 2): {DirectionalValues.TILE: True, DirectionalValues.NORTH: True, DirectionalValues.WEST: True, DirectionalValues.NORTH_WEST: False},
        rotate_90(tileset_sprites[0], 3): {DirectionalValues.TILE: True, DirectionalValues.SOUTH: True, DirectionalValues.WEST: True, DirectionalValues.SOUTH_WEST: False},
        tileset_sprites[11]: {DirectionalValues.TILE: False, DirectionalValues.NORTH: False, DirectionalValues.WEST: False, DirectionalValues.NORTH_WEST: True},
        rotate_90(tileset_sprites[11], 1): {DirectionalValues.TILE: False, DirectionalValues.SOUTH: False, DirectionalValues.WEST: False, DirectionalValues.SOUTH_WEST: True},
        rotate_90(tileset_sprites[11], 2): {DirectionalValues.TILE: False, DirectionalValues.SOUTH: False, DirectionalValues.EAST: False, DirectionalValues.SOUTH_EAST: True},
        rotate_90(tileset_sprites[11], 3): {DirectionalValues.TILE: False, DirectionalValues.NORTH: False, DirectionalValues.EAST: False, DirectionalValues.NORTH_EAST: True},

        # inside corner (2r)
        pg.transform.scale(tileset_sprites[5], (GameUnits.UNIT, GameUnits.UNIT)): {DirectionalValues.TILE: True, DirectionalValues.SOUTH: False, DirectionalValues.EAST: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[5], (GameUnits.UNIT, GameUnits.UNIT)), -90): {DirectionalValues.TILE: True, DirectionalValues.SOUTH: False, DirectionalValues.WEST: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[5], (GameUnits.UNIT, GameUnits.UNIT)), 180): {DirectionalValues.TILE: True, DirectionalValues.NORTH: False, DirectionalValues.WEST: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[5], (GameUnits.UNIT, GameUnits.UNIT)), 90): {DirectionalValues.TILE: True, DirectionalValues.NORTH: False, DirectionalValues.EAST: False},
        pg.transform.scale(tileset_sprites[6], (GameUnits.UNIT, GameUnits.UNIT)): {DirectionalValues.TILE: False, DirectionalValues.NORTH: True, DirectionalValues.WEST: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[6], (GameUnits.UNIT, GameUnits.UNIT)), -90): {DirectionalValues.TILE: False, DirectionalValues.NORTH: True, DirectionalValues.EAST: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[6], (GameUnits.UNIT, GameUnits.UNIT)), 180): {DirectionalValues.TILE: False, DirectionalValues.SOUTH: True, DirectionalValues.EAST: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[6], (GameUnits.UNIT, GameUnits.UNIT)), 90): {DirectionalValues.TILE: False, DirectionalValues.SOUTH: True, DirectionalValues.WEST: True},

        # straight (1r)
        pg.transform.scale(tileset_sprites[1], (GameUnits.UNIT, GameUnits.UNIT)): {DirectionalValues.TILE: True, DirectionalValues.SOUTH: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[1], (GameUnits.UNIT, GameUnits.UNIT)), -90): {DirectionalValues.TILE: True, DirectionalValues.WEST: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[1], (GameUnits.UNIT, GameUnits.UNIT)), 180): {DirectionalValues.TILE: True, DirectionalValues.NORTH: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[1], (GameUnits.UNIT, GameUnits.UNIT)), 90): {DirectionalValues.TILE: True, DirectionalValues.EAST: False},
        pg.transform.scale(tileset_sprites[10], (GameUnits.UNIT, GameUnits.UNIT)): {DirectionalValues.TILE: False, DirectionalValues.NORTH: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[10], (GameUnits.UNIT, GameUnits.UNIT)), -90): {DirectionalValues.TILE: False, DirectionalValues.EAST: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[10], (GameUnits.UNIT, GameUnits.UNIT)), 180): {DirectionalValues.TILE: False, DirectionalValues.SOUTH: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[10], (GameUnits.UNIT, GameUnits.UNIT)), 90): {DirectionalValues.TILE: False, DirectionalValues.WEST: True},
    }
