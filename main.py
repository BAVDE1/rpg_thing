import pygame
import game
from constants import *


def main():
    pygame.init()
    pygame.display.set_caption(CAPTION)
    pygame.display.set_icon(pygame.image.load(PLAYER_TEXTURE))
    pygame.display.set_mode([RESOLUTION, RESOLUTION])
    game.Game().main_loop()
    pygame.quit()


if __name__ == "__main__":
    main()
