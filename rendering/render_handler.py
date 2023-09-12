from level.level import Level
from constants import GameUnits
import pygame as pg

level = None


def render(surface, player, level_to_render):
    global level

    if not level:
        level = Level(surface, level_to_render, pos_offset=pg.Vector2(GameUnits.LEVEL_OFFSET, 0))

    while not player.is_player_loaded():
        player.render_player()

    level.render_level()
    player.render_player()
    level.render_level_foreground()
