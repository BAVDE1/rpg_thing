from level.level import Level

level = None


def render(surface, player, level_to_render, logger):
    global level

    if not level:
        level = Level(surface, level_to_render)

    while not player.is_player_loaded():
        player.render_player()

    level.render_level()
    player.render_player()
    level.render_level_foreground()

    # for debugging:
    logger.render_logs()
