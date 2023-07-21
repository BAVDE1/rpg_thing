import pygame
import input_handler
from entity import player
import rendering.render_handler as renderer

# Constant values
FRAME_RATE = 30
BASE_RES = 288  # 256 + 32 for edges
BASE_UNIT = 16  # 16 x 16 grid (with one remainder for each edge, player sees 17x17, ascii needs to be 18x18)
RES_MUL = 2
RESOLUTION = BASE_RES * RES_MUL
UNIT = BASE_UNIT * RES_MUL

# Setup
pygame.init()
screen = pygame.display.set_mode((RESOLUTION, RESOLUTION))
clock = pygame.time.Clock()
running = True

# Defaults
mid_width = screen.get_width() / 2
mid_height = screen.get_height() / 2
player = player.Player(mid_width, mid_height, screen)

# Game values
current_area = None
current_level = None
starting_level = "levels/overworld_0.txt"


def events():
    """ Events, loops through all events in event queue """
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


def functionality():
    """ Functionality here """

    input_handler.player_input(player, UNIT)


def render():
    """ Render here (after functionality)
        Render player last """

    renderer.render(starting_level, UNIT, screen)

    player.draw_player(UNIT)

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
