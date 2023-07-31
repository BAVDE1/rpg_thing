import os
from constants import *
from rendering.level import render_level
from entity.player import Player


def parse_level(level_source):
    """ Returns list of lines in level file """
    if not os.path.exists(level_source):
        raise FileNotFoundError("level file {} could not be found. Was there a typo, was the directory not properly declared?".format(level_source))

    level_lines = []
    with open(level_source) as file:
        for line in file:
            level_lines.append(line)
    return level_lines


def render(player, level_to_render, surface):
    render_level(parse_level(level_to_render), UNIT, surface)

    Player.render_player(player, surface)





def split_sheet(image, size, columns, rows):
    """ Returns list of rectangles for each frame """
    pass
