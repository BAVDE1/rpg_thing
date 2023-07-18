import pygame

# Controls
up = [pygame.K_w, pygame.K_UP]
down = [pygame.K_s, pygame.K_DOWN]
left = [pygame.K_a, pygame.K_LEFT]
right = [pygame.K_d, pygame.K_RIGHT]


def player_input(player, unit):
    keys = pygame.key.get_pressed()
    has_active_input = any(keys)

    # Movement
    if player.can_move() and has_active_input:
        movement_input(player, unit, keys)


def movement_input(player, unit, keys):
    player.moving = True

    if keys[up[0]] or keys[up[1]]:
        player.move(0, -unit)
    elif keys[down[0]] or keys[down[1]]:
        player.move(0, unit)
    elif keys[left[0]] or keys[left[1]]:
        player.move(-unit, 0)
    elif keys[right[0]] or keys[right[1]]:
        player.move(unit, 0)
