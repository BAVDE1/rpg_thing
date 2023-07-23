import pygame
import time
import entity.player
from constants import *

# Controls
DIR_DICT = {
    pygame.K_w: UP,
    pygame.K_UP: UP,
    pygame.K_s: DOWN,
    pygame.K_DOWN: DOWN,
    pygame.K_a: LEFT,
    pygame.K_LEFT: LEFT,
    pygame.K_d: RIGHT,
    pygame.K_RIGHT: RIGHT
}

held_dir_keys = []


def player_key_down(player: entity.player.Player, key):

    # Movement
    if key in DIR_DICT:
        held_dir_keys.append(key)
        if player.can_move():
            # TODO: send beat event
            player.direction = DIR_DICT[held_dir_keys[0]]
            player.move()


def sprint_manager(player: entity.player.Player):
    if len(held_dir_keys) > 0:
        if DIR_DICT.get(held_dir_keys[0]):
            if player.can_move() and not player.sprinting and time.time() - player.last_moved > HOLD_TIME_TO_SPRINT:
                # start sprint
                player.movement_pause = SPRINT_MOVEMENT_PAUSE
                player.sprinting = True
            elif player.sprinting and player.can_move():
                # continue sprint
                player.direction = DIR_DICT[held_dir_keys[0]]
                player.move()
    elif len(held_dir_keys) == 0 and player.sprinting:
        # stop sprint
        player.movement_pause = WALK_MOVEMENT_PAUSE
        player.sprinting = False


def player_key_up(player: entity.player.Player, key):
    if key in held_dir_keys:
        held_dir_keys.remove(key)
        if len(held_dir_keys) > 0:
            player.direction = DIR_DICT[held_dir_keys[0]]
