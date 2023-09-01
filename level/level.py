from constants import GameUnits, DirectionalValues
from texture_constants import get_outline_tileset_dict, TileTextures, ASCII_TO_SPRITE
import os
import pygame as pg


def parse_level_file(level_source):
    """ Returns list of lines in level file """
    if not os.path.exists(level_source):
        raise FileNotFoundError(
            f"level file {level_source} could not be found. Was there a typo; was the directory not properly declared?")

    level_lines = []
    with open(level_source) as file:
        for line in file:
            level_lines.append(line.strip().replace("[", "").replace("]", ""))
    return level_lines


def outline_decider(dic: dict):
    outlines = get_outline_tileset_dict(TileTextures.LEAVES_TILESET_SPRITES)

    add = None
    for key in outlines.keys():
        should = True
        for k in outlines[key]:
            should = False if bool(dic[k]) != outlines[key][k] else should
        if should:
            add = key
            break  # stop loop once it finds a suitable tile
    return add


def store_layer(layer: list, layer_lines):
    for line in layer_lines:
        row = []
        for chars in line.split(","):
            row.append(ASCII_TO_SPRITE[chars] if chars in ASCII_TO_SPRITE else None)
        layer.append(row)


class Level:
    def __init__(self, surface, level_source, pos_offset: pg.Vector2 = pg.Vector2(0, 0), size=1):
        self.is_initialised = False
        self.surface = surface
        self.pos_offset = pos_offset
        self.size = size

        self.ground_layer_lines = parse_level_file(level_source)
        self.ground_layer = []
        self.outline_layer = []

        self.initialise_level()

    def initialise_level(self):
        if not self.is_initialised:
            store_layer(self.ground_layer, self.ground_layer_lines)
            self.initialise_outline()

            self.is_initialised = True

    def initialise_outline(self):
        r = 0
        for column in self.ground_layer:
            c = 0
            row = []
            for sprite in column:
                n = max(0, r - 1)
                s = min(len(self.ground_layer) - 1, r + 1)
                e = min(len(column) - 1, c + 1)
                w = max(0, c - 1)

                row.append(outline_decider({
                    DirectionalValues.TILE: sprite,
                    DirectionalValues.NORTH: self.ground_layer[n][c],
                    DirectionalValues.SOUTH: self.ground_layer[s][c],
                    DirectionalValues.EAST: self.ground_layer[r][e],
                    DirectionalValues.WEST: self.ground_layer[r][w],
                    DirectionalValues.NORTH_EAST: self.ground_layer[n][e],
                    DirectionalValues.NORTH_WEST: self.ground_layer[n][w],
                    DirectionalValues.SOUTH_EAST: self.ground_layer[s][e],
                    DirectionalValues.SOUTH_WEST: self.ground_layer[s][w]
                }))
                c += 1
            self.outline_layer.append(row)
            r += 1

    def render_level(self):
        """ Called every frame """
        if self.is_initialised:
            self.draw_layer(self.ground_layer)

    def render_level_foreground(self):
        """ Called every frame (after other things have been rendered) """
        if self.is_initialised:
            self.draw_layer(self.outline_layer, True)

    def draw_layer(self, layer, has_fade=False):
        r = 0
        for column in layer:
            c = 0
            for sprite in column:
                if sprite and isinstance(sprite, pg.surface.Surface):
                    sprite = pg.transform.scale(sprite, (sprite.get_width() * self.size, sprite.get_height() * self.size))
                    self.surface.blit(sprite, self.create_draw_pos(sprite, r, c))

                # add fade
                if has_fade and c == 0 or c == len(column) - 1:
                    f_s = pg.transform.flip(TileTextures.FADE_SPRITE, 1, 0) if c == 0 else TileTextures.FADE_SPRITE
                    f_s = pg.transform.scale(f_s, (f_s.get_width() * self.size, f_s.get_height() * self.size))
                    self.surface.blit(f_s, self.create_draw_pos(f_s, r, c))
                c += 1
            r += 1

    def create_draw_pos(self, sprite: pg.surface.Surface, row, column):
        return [((((column * GameUnits.UNIT) - sprite.get_width() // 2) + GameUnits.LEVEL_OFFSET) * self.size) + self.pos_offset.x,
                (((row * GameUnits.UNIT) - sprite.get_height() // 2) * self.size) + self.pos_offset.y]
