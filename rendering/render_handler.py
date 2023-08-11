import os
from constants import *
from rendering.level import render_level
from entity.player import Player


def parse_level(level_source):
    """ Returns list of lines in level file """
    if not os.path.exists(level_source):
        raise FileNotFoundError(f"level file {level_source} could not be found. Was there a typo; was the directory not properly declared?")

    level_lines = []
    with open(level_source) as file:
        for line in file:
            level_lines.append(line)
    return level_lines


def render(player, level_to_render, surface):
    while not player.is_player_loaded():
        player.render_player(surface)

    render_level(parse_level(level_to_render), UNIT, surface)
    player.render_player(surface)
