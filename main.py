import pygame
from player import Player
from input_handler import player_input

# Constant values
frame_rate = 30
screen_size = 600
unit = 20

# Setup
pygame.init()
screen = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()
running = True

# Defaults
mid_width = screen.get_width() / 2
mid_height = screen.get_height() / 2
player = Player(mid_width, mid_height, screen)


# Main loop, loops every frame
while running:
    # Events, loops through all events in event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color to wipe away anything from last frame, i think?
    screen.fill("black")

    # Functionality here
    player_input(player, unit)

    # Render last
    player.draw_player(unit)

    # Flip the display to put stuff on screen
    pygame.display.flip()

    # Lock frame rate
    clock.tick(frame_rate)

# Close screen
pygame.quit()
