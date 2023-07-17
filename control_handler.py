import pygame


# Controls
up = [pygame.K_w, pygame.K_UP]
down = [pygame.K_s, pygame.K_DOWN]
left = [pygame.K_a, pygame.K_LEFT]
right = [pygame.K_d, pygame.K_RIGHT]


def player_input(player, units):

    # Movement
    if player.can_move():
        player.moving = True
        movement_input(player, units)
        player.moving = False


def movement_input(player, units):
    keys = pygame.key.get_pressed()

    if keys[up[0]] or keys[up[1]]:
        player.move(0, -units)
    elif keys[down[0]] or keys[down[1]]:
        player.move(0, units)
    elif keys[left[0]] or keys[left[1]]:
        player.move(-units, 0)
    elif keys[right[0]] or keys[right[1]]:
        player.move(units, 0)
