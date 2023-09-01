from level.level import Level
from utility.util import time_it

level = None


# @time_it  # about 0.015 to be expected though?
def render(surface, player, level_to_render):
    global level

    if not level:
        level = Level(surface, level_to_render)

    while not player.is_player_loaded():
        player.render_player()

    level.render_level()
    player.render_player()
    level.render_level_foreground()
