from constants import *
import rendering.render_handler
from rendering.rendering_other import split_sheet


def activate_dev_mode(screen):
    pass


def player_key_down(game, player, keys):
    if keys[pg.K_p]:
        game.bpm = 60 if game.bpm == 120 else 120 if game.bpm > 120 else 180
    if keys[pg.K_m]:
        texture_idle = pg.image.load(PLAYER_IDLE_DEBUG).convert_alpha()
        ss_idle = split_sheet(texture_idle, (BASE_UNIT, BASE_UNIT), 4)
        player.animator.change_idle_anim(False, new_idle_ss=[PLAYER_IDLE_DEBUG, ss_idle], boomerang_idle=False)
    if keys[pg.K_n]:
        player.animator.change_idle_anim(set_to_default=True)


def dev_mode_loop(game):
    pg.display.set_caption("DEV MODE || {} - FPS: {:.2f}".format(CAPTION, game.clock.get_fps()))
