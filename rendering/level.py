import pygame


def render_level(level_lines, unit, surface):

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
