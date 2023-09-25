from level.level import Level
from entity.player import Player
from utility.text_object import TextObjectsHolder


def render_active_level(game, player: Player, level: Level, txt_holder: TextObjectsHolder):
    """ Renders an active player, level & its entities """
    # initialise
    if not player.is_player_loaded() or not level.is_initialised:
        while not player.is_player_loaded():
            player.render_player()
        while not level.is_initialised:  # isn't needed here, but just in case
            level.initialise_level()

        # called once everything is loaded
        game.on_level_fully_loaded()

    level.render_level()
    player.render_player()
    level.render_level_foreground()

    txt_holder.render()
