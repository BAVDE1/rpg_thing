import os
import pygame


def parse_level(level_source):
    """ Returns list of lines in level file """
    if not os.path.exists(level_source):
        raise FileNotFoundError("level file {} could not be found. Was there a typo, was the directory not declared?".format(level_source))

    level_lines = []
    with open(level_source) as file:
        for line in file:
            level_lines.append(line)
    return level_lines


def render_level(level_to_render, unit, surface):
    level_lines = parse_level(level_to_render)

    line_num = 0
    for line in level_lines:
        char_num = 0
        line = line[1:-2]  # strips square brackets
        for char in line:
            pos_x = (unit * -.5) + (unit * char_num)
            pos_y = (unit * -.5) + (unit * line_num)
            if char == ".":
                pygame.draw.rect(surface, "green", (pos_x, pos_y, unit, unit))
            char_num += 1
        line_num += 1
