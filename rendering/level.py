import pygame
from constants import *


def render_level(level_lines, unit, surface):

    line_num = 0
    for line in level_lines:
        char_num = 0
        line = line.strip("]")[1:]  # strips square brackets
        for char in line:
            pos_x = unit * char_num
            pos_y = unit * line_num

            if char == ".":
                draw_grass(surface, pos_x, pos_y)
            char_num += 1
        line_num += 1


def draw_grass(surface, pos_x, pos_y):
    texture = pygame.image.load(GRASS_TEXTURE)
    sprite = pygame.transform.scale(texture, (UNIT, UNIT))
    blit_xy = (pos_x - sprite.get_width() // 2,
               pos_y - sprite.get_height() // 2)

    surface.blit(sprite, blit_xy)
