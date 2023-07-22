import pygame
import input_handler
from entity import player
import rendering.render_handler as renderer
from constants import *


# Setup
pygame.init()
screen = pygame.display.set_mode((RESOLUTION, RESOLUTION))
clock = pygame.time.Clock()
running = True

# Defaults
mid_width = screen.get_width() / 2
mid_height = screen.get_height() / 2
player = player.Player(mid_width, mid_height)

# Game values
current_area = None
current_level = None


def events():
    """ Events, loops through all events in event queue """
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


def functionality():
    """ Functionality here """

    input_handler.player_input(player)


def render():
    """ Render here (after functionality)
        Render player last """

    renderer.render(player, OVERWORLD_LEVEL_DIR, screen)

    # Flip the display to put stuff on screen
    pygame.display.flip()


# Main loop, loops every frame
while running:
    events()

    # Fill the screen with a color to wipe away anything from last frame, i think?
    screen.fill("black")

    functionality()
    render()

    # Lock frame rate
    clock.tick(FRAME_RATE)

# Close screen
pygame.quit()
