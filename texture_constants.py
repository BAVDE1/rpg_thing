from rendering.split_sheet import split_sheet
from constants import GameUnits, DirectionalValues

import pygame as pg


class RenderValues:
    SHADOW_QUALITY: int = 8  # the higher the number, the better quality but is harder on performance (is later automatically converted to an even number and clamped between 2 and 10)


class PlayerTextures:
    PLAYER_IDLE = "assets/textures/player_idle.png"
    PLAYER_JUMP_HORIZONTAL = "assets/textures/player_jump_horizontal.png"
    PLAYER_JUMP_VERTICAL = "assets/textures/player_jump_vertical.png"
    PLAYER_IDLE_DEBUG = "assets/textures/player_idle_debug.png"


class TileTextures:
    FADE_TEXTURE = "assets/textures/tiles/fade_tile.png"
    FADE_SPRITE = pg.transform.scale(pg.image.load(FADE_TEXTURE), (GameUnits.UNIT, GameUnits.UNIT))

    GRASS_TEXTURE = "assets/textures/tiles/grass.png"
    GRASS_SPRITE = pg.transform.scale(pg.image.load(GRASS_TEXTURE), (GameUnits.UNIT, GameUnits.UNIT))

    LEAVES_TILESET = "assets/textures/tiles/leaves_tileset.png"
    LEAVES_TILESET_SPRITE = pg.image.load(LEAVES_TILESET)
    LEAVES_TILESET_SPRITES = split_sheet(LEAVES_TILESET_SPRITE, (20, 20), 5, 5)


ASCII_TO_SPRITE = {
    "Gr": TileTextures.GRASS_SPRITE
}


def get_outline_tileset_dict(tileset_sprites):
    """ MUST be in order from the most amount of requirements to least (True=has tile, False=empty tile)"""
    return {
        # corner (3r)
        pg.transform.scale(tileset_sprites[0], (GameUnits.UNIT, GameUnits.UNIT)): {DirectionalValues.TILE: True, DirectionalValues.SOUTH: True, DirectionalValues.EAST: True, DirectionalValues.SOUTH_EAST: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[0], (GameUnits.UNIT, GameUnits.UNIT)), -90): {DirectionalValues.TILE: True, DirectionalValues.SOUTH: True, DirectionalValues.WEST: True, DirectionalValues.SOUTH_WEST: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[0], (GameUnits.UNIT, GameUnits.UNIT)), 180): {DirectionalValues.TILE: True, DirectionalValues.NORTH: True, DirectionalValues.WEST: True, DirectionalValues.NORTH_WEST: False},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[0], (GameUnits.UNIT, GameUnits.UNIT)), 90): {DirectionalValues.TILE: True, DirectionalValues.NORTH: True, DirectionalValues.EAST: True, DirectionalValues.NORTH_EAST: False},
        pg.transform.scale(tileset_sprites[11], (GameUnits.UNIT, GameUnits.UNIT)): {DirectionalValues.TILE: False, DirectionalValues.NORTH: False, DirectionalValues.WEST: False, DirectionalValues.NORTH_WEST: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[11], (GameUnits.UNIT, GameUnits.UNIT)), -90): {DirectionalValues.TILE: False, DirectionalValues.NORTH: False, DirectionalValues.EAST: False, DirectionalValues.NORTH_EAST: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[11], (GameUnits.UNIT, GameUnits.UNIT)), 180): {DirectionalValues.TILE: False, DirectionalValues.SOUTH: False, DirectionalValues.EAST: False, DirectionalValues.SOUTH_EAST: True},
        pg.transform.rotate(pg.transform.scale(tileset_sprites[11], (GameUnits.UNIT, GameUnits.UNIT)), 90): {DirectionalValues.TILE: False, DirectionalValues.SOUTH: False, DirectionalValues.WEST: False, DirectionalValues.SOUTH_WEST: True},

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
