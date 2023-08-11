import os

import rendering.level
from constants import *
from rendering.level import Level
from entity.player import Player


def render(player, level_to_render, surface):
    while not player.is_player_loaded():
        player.render_player(surface)

    current_level = Level(level_to_render, surface)
    current_level.draw_level()
    player.render_player(surface)
