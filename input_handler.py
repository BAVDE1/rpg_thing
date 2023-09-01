import time
from entity.player import Player
from constants import DirectionalValues, PlayerValues

held_direction_keys = []


def player_key_down(player: Player, key):
    # Movement
    if key in DirectionalValues.DIRECTION_DICT:
        held_direction_keys.append(key)
        if player.can_move():
            player.direction = DirectionalValues.DIRECTION_DICT[held_direction_keys[0]]
            player.move()


def sprint_manager(player: Player):
    if len(held_direction_keys) > 0:
        if DirectionalValues.DIRECTION_DICT.get(held_direction_keys[0]) and player.can_move():
            if not player.sprinting and time.time() - player.last_moved > PlayerValues.HOLD_TIME_TO_SPRINT:
                player.sprinting = True  # start sprint
            elif player.sprinting:
                player.direction = DirectionalValues.DIRECTION_DICT[held_direction_keys[0]]
                player.move()  # continue sprint
    elif len(held_direction_keys) == 0 and player.sprinting:
        player.sprinting = False  # stop sprint


def player_key_up(key):
    if key in held_direction_keys:
        held_direction_keys.remove(key)
