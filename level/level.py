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
    """ Returns None if no outline is suitable """
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


class TileSprite(pg.sprite.Sprite):
    def __init__(self, sprite_img: pg.surface.Surface, pos: pg.Vector2, sprite_offset_pos: pg.Vector2 = pg.Vector2(0, 0)):
        pg.sprite.Sprite.__init__(self)

        self.image = sprite_img
        self.rect = pg.rect.Rect(pos.x + sprite_offset_pos.x, pos.y + sprite_offset_pos.y, self.image.get_width(), self.image.get_height())


class Level:
    def __init__(self, surface, level_source, pos_offset: pg.Vector2 = pg.Vector2(0, 0), size=1):
        self.is_initialised = False
        self.surface = surface
        self.pos_offset = pos_offset
        self.size = size

        self.ground_layer_lines = parse_level_file(level_source)
        self.ground_layer_group = pg.sprite.Group()
        self.outline_layer_group = pg.sprite.Group()

        self.initialise_level()

    def initialise_level(self):
        if not self.is_initialised:
            self.store_group(self.ground_layer_group, self.ground_layer_lines)
            self.store_outline(True)

            self.is_initialised = True

    def render_level(self):
        """ Called every frame """
        if self.is_initialised:
            self.ground_layer_group.draw(self.surface)

    def render_level_foreground(self):
        """ Called every frame (after other things have been rendered) """
        if self.is_initialised:
            self.outline_layer_group.draw(self.surface)

    def store_group(self, group: pg.sprite.Group, layer_lines):
        for r, line in enumerate(layer_lines):
            for c, chars in enumerate(line.split(",")):
                if sp := ASCII_TO_SPRITE[chars] if chars in ASCII_TO_SPRITE else None:
                    sp = self.scaled_sprite(sp)
                    t_pos = self.create_tile_pos(sp, r, c)

                    sprite = TileSprite(sp, t_pos)
                    sprite.add(group)

    def store_outline(self, store_fade=False):
        ground_layer_bools = []
        for line in self.ground_layer_lines:
            row = [1 if chars in ASCII_TO_SPRITE else 0 for chars in line.split(',')]
            ground_layer_bools.append(row)

        for r, line in enumerate(ground_layer_bools):
            for c, chars in enumerate(line):
                n = max(0, r - 1)
                s = min(len(ground_layer_bools) - 1, r + 1)
                e = min(len(line) - 1, c + 1)
                w = max(0, c - 1)

                sp = outline_decider({
                    DirectionalValues.TILE: chars,
                    DirectionalValues.NORTH: ground_layer_bools[n][c],
                    DirectionalValues.SOUTH: ground_layer_bools[s][c],
                    DirectionalValues.EAST: ground_layer_bools[r][e],
                    DirectionalValues.WEST: ground_layer_bools[r][w],
                    DirectionalValues.NORTH_EAST: ground_layer_bools[n][e],
                    DirectionalValues.NORTH_WEST: ground_layer_bools[n][w],
                    DirectionalValues.SOUTH_EAST: ground_layer_bools[s][e],
                    DirectionalValues.SOUTH_WEST: ground_layer_bools[s][w]
                })

                if sp:
                    sp = self.scaled_sprite(sp)
                    t_pos = self.create_tile_pos(sp, r, c)

                    sprite = TileSprite(sp, t_pos)
                    sprite.add(self.outline_layer_group)

                if store_fade and (c == 0 or c == len(line) - 1):
                    f_sp = pg.transform.flip(TileTextures.FADE_SPRITE, 1, 0) if c == 0 else TileTextures.FADE_SPRITE
                    f_sp = self.scaled_sprite(f_sp)
                    f_pos = self.create_tile_pos(f_sp, r, c)

                    f_sprite = TileSprite(f_sp, f_pos)
                    f_sprite.add(self.outline_layer_group)

    def scaled_sprite(self, sprite) -> pg.surface.Surface:
        return pg.transform.scale(sprite, (sprite.get_width() * self.size, sprite.get_height() * self.size))

    def create_tile_pos(self, sprite: pg.surface.Surface, row, column) -> pg.Vector2:
        return pg.Vector2(
            ((((column * GameUnits.UNIT) - sprite.get_width() / 2) + GameUnits.LEVEL_OFFSET) * self.size) + self.pos_offset.x,
            (((row * GameUnits.UNIT) - sprite.get_height() / 2) * self.size) + self.pos_offset.y)
