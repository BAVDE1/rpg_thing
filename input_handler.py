import time
from entity.player import Player
from constants import *

# Controls


held_dir_keys = []


def player_key_down(player: Player, key):

    # Movement
    if key in DIR_DICT:
        held_dir_keys.append(key)
        if player.can_move():
            # TODO: send beat event
            player.direction = DIR_DICT[held_dir_keys[0]]
            player.move()


def sprint_manager(player: Player):
    if len(held_dir_keys) > 0:
        if DIR_DICT.get(held_dir_keys[0]) and player.can_move():
            if not player.sprinting and time.time() - player.last_moved > HOLD_TIME_TO_SPRINT:
                # start sprint
                player.sprinting = True
            elif player.sprinting:
                # continue sprint
                player.direction = DIR_DICT[held_dir_keys[0]]
                player.move()
    elif len(held_dir_keys) == 0 and player.sprinting:
        # stop sprint
        player.sprinting = False


def player_key_up(player: Player, key):
    if key in held_dir_keys:
        held_dir_keys.remove(key)
        if len(held_dir_keys) > 0:
            player.direction = DIR_DICT[held_dir_keys[0]]
