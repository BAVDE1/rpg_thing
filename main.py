import pygame
from player import Player
from control_handler import player_input

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


# Main loop, loops every frame
while running:
    # Events, loops through all events in event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color to wipe away anything from last frame, i think?
    screen.fill("black")

    # Functionality here
    player_input(player, units)

    # Render last
    player.draw_player()

    # Flip the display to put stuff on screen
    pygame.display.flip()

    # Lock frame rate
    clock.tick(30)

# Close on 'x' button pressed
pygame.quit()
