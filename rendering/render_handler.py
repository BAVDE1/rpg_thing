from rendering.level import Level


level = None


def render(player, level_to_render, surface):
    global level

    if not level:
        level = Level(level_to_render, surface)

    while not player.is_player_loaded():
        player.render_player(surface)

    level.draw_level()
    player.render_player(surface)
