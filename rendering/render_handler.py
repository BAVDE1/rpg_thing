from rendering.level import Level


level = None


def render(game, player, level_to_render, surface):
    global level

    if not level:
        level = Level(level_to_render, surface)

    while not player.is_player_loaded():
        player.render_player()

    level.render_level()
    player.render_player()
    level.render_level_foreground()

    if game.dev_mode:
        level.render_dev_mode()
