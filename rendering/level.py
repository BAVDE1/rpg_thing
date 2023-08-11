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
        self.level_lines = parse_level(level_source)
        self.tiles = []

        self.initialise_level()

    def initialise_level(self):
        self.is_initialised = False
        line_num = 0
        for line in self.level_lines:
            row = []
            char_num = 0
            line = line.strip("]")[1:]  # strips square brackets
            for char in line:
                pos_x = UNIT * char_num
                pos_y = UNIT * line_num

                if char in ASCII:
                    row.append(ASCII[char])
                else:
                    row.append("")
                char_num += 1
            self.tiles.append(row)
            line_num += 1
        self.is_initialised = True

    def draw_level(self):
        if self.is_initialised:
            self.draw_tile()

    def draw_tile(self):
        r = 0
        for column in self.tiles:
            c = 0
            for sprite in column:
                print(self.tiles)
                self.surface.blit(sprite, [c - ASCII[sprite].get_width() // 2, r - sprite.get_height() // 2])
                c += 1
            r += 1
