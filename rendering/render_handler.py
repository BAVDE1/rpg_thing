import os
from rendering.level import render_level


def parse_level(level_source):
    """ Returns list of lines in level file """
    if not os.path.exists(level_source):
        raise FileNotFoundError("level file {} could not be found. Was there a typo, was the directory not declared?".format(level_source))

    level_lines = []
    with open(level_source) as file:
        for line in file:
            level_lines.append(line)
    return level_lines


def render(level_to_render, unit, surface):
    render_level(parse_level(level_to_render), unit, surface)
