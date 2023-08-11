from texture_loader import *
import os


def parse_level(level_source):
    """ Returns list of lines in level file """
    if not os.path.exists(level_source):
        raise FileNotFoundError(
            f"level file {level_source} could not be found. Was there a typo; was the directory not properly declared?")

    level_lines = []
    with open(level_source) as file:
        for line in file:
            level_lines.append(line)
    return level_lines


class Level:
    def __init__(self, level_source, surface):
        self.is_initialised = False
        self.surface = surface
        self.ground_layer_lines = parse_level(level_source)
        self.ground_layer = []

        self.initialise_level()

    def initialise_level(self):
        self.is_initialised = False
        for line in self.ground_layer_lines:
            row = []
            for char in line:
                row.append(ASCII[char] if char in ASCII else None)
            self.ground_layer.append(row)
        self.is_initialised = True

    def draw_level(self):
        if self.is_initialised:
            self.draw_layer(self.ground_layer)

    def draw_layer(self, layer):
        r = 0
        for column in layer:
            c = 0
            for sprite in column:
                if sprite:
                    self.surface.blit(sprite, [(c * UNIT) - sprite.get_width() // 2, (r * UNIT) - sprite.get_height() // 2])
                c += 1
            r += 1
