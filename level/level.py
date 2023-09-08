from constants import GameUnits, DirectionalValues
from texture_constants import get_outline_tileset_dict, TileTextures, ASCII_TO_SPRITE
from rendering.sprites_holder import TileSprite
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
    """ Returns suitable outline for tiles' position depending upon its surrounding tiles.
    Returns None if no suitable outline is found """
    outlines = get_outline_tileset_dict(TileTextures.LEAVES_TILESET_SPRITES)

    sprite_to_add = None
    for sprite in outlines.keys():
        found_suitable_sprite = True
        for requirement in outlines[sprite]:  # if even one requirement is not met, 'found_suitable_sprite' will be false
            found_suitable_sprite = False if bool(dic[requirement]) != outlines[sprite][requirement] else found_suitable_sprite

        if found_suitable_sprite:
            sprite_to_add = sprite
            break  # stop loop once it finds a suitable tile

    return sprite_to_add


def store_layer(layer: list, layer_lines):
    """ Generates a list of split lines of the level file given
     eg: [[  ,Gr,Gr,  ], [Gr,Gr,Gr,  ]]
     """
    for line in layer_lines:
        row = [ASCII_TO_SPRITE[chars] if chars in ASCII_TO_SPRITE else None for chars in line.split(',')]
        layer.append(row)


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
            # create tiles & fill groups
            self.store_group(self.ground_layer_group, self.ground_layer_lines)
            self.store_outline(True)

            # finish
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
        """ Converts ascii chars from layer_lines into valid TileSprites and stores them into the given group """
        for row_n, line in enumerate(layer_lines):
            for column_n, chars in enumerate(line.split(",")):
                if raw_sprite := ASCII_TO_SPRITE[chars] if chars in ASCII_TO_SPRITE else None:
                    raw_sprite = self.create_scaled_sprite(raw_sprite)
                    t_pos = self.create_tile_pos(raw_sprite, row_n, column_n)

                    tile_sprite = TileSprite(raw_sprite, t_pos)
                    tile_sprite.add(group)

    def store_outline(self, store_fade=False):
        """ Used to determine and put sprites into the outline group """
        ground_layer_bools = []
        for line in self.ground_layer_lines:
            row = [1 if chars in ASCII_TO_SPRITE else 0 for chars in line.split(',')]
            ground_layer_bools.append(row)

        for row_n, line in enumerate(ground_layer_bools):
            for column_n, chars in enumerate(line):
                north_t = max(0, row_n - 1)
                south_t = min(len(ground_layer_bools) - 1, row_n + 1)
                east_t = min(len(line) - 1, column_n + 1)
                west_t = max(0, column_n - 1)

                cardinal_dic = {
                    DirectionalValues.TILE: chars,
                    DirectionalValues.NORTH: ground_layer_bools[north_t][column_n],
                    DirectionalValues.SOUTH: ground_layer_bools[south_t][column_n],
                    DirectionalValues.EAST: ground_layer_bools[row_n][east_t],
                    DirectionalValues.WEST: ground_layer_bools[row_n][west_t],
                    DirectionalValues.NORTH_EAST: ground_layer_bools[north_t][east_t],
                    DirectionalValues.NORTH_WEST: ground_layer_bools[north_t][west_t],
                    DirectionalValues.SOUTH_EAST: ground_layer_bools[south_t][east_t],
                    DirectionalValues.SOUTH_WEST: ground_layer_bools[south_t][west_t]
                }

                if raw_sprite := outline_decider(cardinal_dic):
                    raw_sprite = self.create_scaled_sprite(raw_sprite)
                    t_pos = self.create_tile_pos(raw_sprite, row_n, column_n)

                    tile_sprite = TileSprite(raw_sprite, t_pos)
                    tile_sprite.add(self.outline_layer_group)

                # store fade tiles after other tiles, so it renders on top
                if store_fade and (column_n == 0 or column_n == len(line) - 1):  # only on the level sides atm
                    f_raw_sprite = pg.transform.flip(TileTextures.FADE_SPRITE, 1, 0) if column_n == 0 else TileTextures.FADE_SPRITE
                    f_raw_sprite = self.create_scaled_sprite(f_raw_sprite)
                    f_pos = self.create_tile_pos(f_raw_sprite, row_n, column_n)

                    f_tile_sprite = TileSprite(f_raw_sprite, f_pos)
                    f_tile_sprite.add(self.outline_layer_group)

    def create_scaled_sprite(self, sprite) -> pg.surface.Surface:
        """ Returns given sprite scaled to levels' size """
        return pg.transform.scale(sprite, (sprite.get_width() * self.size, sprite.get_height() * self.size))

    def create_tile_pos(self, sprite: pg.surface.Surface, row, column) -> pg.Vector2:
        """ Returns Vector2 of a given sprites position depending upon row, column and level size """
        return pg.Vector2(
            ((((column * GameUnits.UNIT) - sprite.get_width() / 2) + GameUnits.LEVEL_OFFSET) * self.size) + self.pos_offset.x,
            (((row * GameUnits.UNIT) - sprite.get_height() / 2) * self.size) + self.pos_offset.y)
