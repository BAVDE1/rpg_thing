from level.area import Area
from entity.player import Player
from utility.text_object import TextObjectsHolder


def render_active_level(game, surface, player: Player, area: Area, txt_holder: TextObjectsHolder):
    """ Renders an active player, level & its entities """
    # initialise
    if not player.is_player_loaded() or not area.level.is_initialised:
        while not player.is_player_loaded():
            player.render_player(surface)
        while not area.level.is_initialised:  # isn't needed here, but just in case
            area.level.initialise_level()

        # called once everything is loaded
        game.on_level_fully_loaded()

    area.level.render_level(surface)
    player.render_player(surface)
    area.level.render_level_foreground(surface)

    txt_holder.render()
