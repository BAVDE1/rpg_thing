from rendering.level import Level


def render(player, level_to_render, surface):
    while not player.is_player_loaded():
        player.render_player(surface)

    Level(level_to_render, surface).draw_level()
    player.render_player(surface)
