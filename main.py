import pygame
from player import Player

# Setup
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True

# Values
mid_width = screen.get_width() / 2
mid_height = screen.get_height() / 2
units = 20

player = Player(mid_width, mid_height, screen)


def controls():
    if player.can_move():
        player.moving = True

        up = [pygame.K_w, pygame.K_UP]
        down = [pygame.K_s, pygame.K_DOWN]
        left = [pygame.K_a, pygame.K_LEFT]
        right = [pygame.K_d, pygame.K_RIGHT]

        keys = pygame.key.get_pressed()

        if keys[up[0]] or keys[up[1]]:
            player.move(0, -units)
        if keys[down[0]] or keys[down[1]]:
            player.move(0, units)

        if keys[left[0]] or keys[left[1]]:
            player.move(-units, 0)
        if keys[right[0]] or keys[right[1]]:
            player.move(units, 0)

        player.moving = False


# Main loop, loops every frame
while running:
    # Events, loops through all events in event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color to wipe away anything from last frame, i think?
    screen.fill("black")

    # Functionality here
    controls()

    # Render last
    player.draw_player()

    # Flip the display to put stuff on screen
    pygame.display.flip()

    # Lock frame rate
    clock.tick(30)

# Close on 'x' button pressed
pygame.quit()
