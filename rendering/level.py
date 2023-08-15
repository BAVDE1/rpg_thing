from constants import *
import os

TILE = "t"

NORTH = "n"
SOUTH = "s"
EAST = "e"
WEST = "w"
NORTH_EAST = "ne"
NORTH_WEST = "nw"
SOUTH_EAST = "se"
SOUTH_WEST = "sw"


def parse_level(level_source):
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
    add = None
    all_args = [bool(dic[TILE]),
                bool(dic[NORTH]), bool(dic[SOUTH]), bool(dic[EAST]), bool(dic[WEST]),
                bool(dic[NORTH_EAST]), bool(dic[NORTH_WEST]), bool(dic[SOUTH_EAST]), bool(dic[SOUTH_WEST])]

    outlines = get_outline_tileset_dict(LEAVES_TILESET_SPRITES)
    if all_args in outlines.values():
        for key in outlines.keys():
            if outlines[key] == all_args:
                add = key
    return add


def store_layer(layer: list, layer_lines):
    for line in layer_lines:
        row = []
        for char in line:
            row.append(ASCII_TO_SPRITE[char] if char in ASCII_TO_SPRITE else None)
        layer.append(row)


class Level:
    def __init__(self, level_source, surface):
        self.is_initialised = False
        self.surface = surface
        self.ground_layer_lines = parse_level(level_source)
        self.ground_layer = []
        self.outline_layer = []

        self.initialise_level()

    def initialise_level(self):
        if not self.is_initialised:
            self.is_initialised = False

            store_layer(self.ground_layer, self.ground_layer_lines)
            self.initialise_outline()

            self.is_initialised = True

    def initialise_outline(self):
        row_num = 0
        for column in self.ground_layer:
            col_num = 0
            row = []
            for sprite in column:
                n = max(0, row_num - 1)
                s = min(len(self.ground_layer) - 1, row_num + 1)
                e = min(len(column) - 1, col_num + 1)
                w = max(0, col_num - 1)

                row.append(outline_decider({
                    TILE: sprite,
                    NORTH: self.ground_layer[n][col_num],
                    SOUTH: self.ground_layer[s][col_num],
                    EAST: self.ground_layer[row_num][e],
                    WEST: self.ground_layer[row_num][w],
                    NORTH_EAST: self.ground_layer[n][e],
                    NORTH_WEST: self.ground_layer[n][w],
                    SOUTH_EAST: self.ground_layer[s][e],
                    SOUTH_WEST: self.ground_layer[s][w]
                }))
                col_num += 1
            self.outline_layer.append(row)
            row_num += 1

    def render_level(self):
        """ Called every frame """
        if self.is_initialised:
            self.draw_layer(self.ground_layer)

    def render_level_foreground(self):
        """ Called every frame (after other things have been rendered) """
        if self.is_initialised:
            self.draw_layer(self.outline_layer)

    def draw_layer(self, layer):
        r = 0
        for column in layer:
            c = 0
            for sprite in column:
                if sprite:
                    self.surface.blit(sprite,
                                      [(c * UNIT) - sprite.get_width() // 2, (r * UNIT) - sprite.get_height() // 2])
                c += 1
            r += 1


