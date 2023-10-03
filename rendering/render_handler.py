from level.area import Area
from entity.player import Player
from utility.text_object import TextObjectsHolder


is_loaded = False


def render_active_level(game, surface, player: Player, area: Area, txt_holder: TextObjectsHolder):
    """ Renders an active player, level & its entities """
    global is_loaded

    # on load
    if not is_loaded:
        game.on_level_fully_loaded()
        is_loaded = True

    area.level.render_level(surface)
    area.level.render_entities(surface)
    player.render_player(surface)
    area.level.render_level_foreground(surface)

    txt_holder.render()
