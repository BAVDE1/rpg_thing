import pygame
import game
from constants import *


def main():
    pygame.init()
    pygame.display.set_caption(CAPTION)
    pygame.display.set_mode([BASE_RES * RES_MUL, BASE_RES * RES_MUL])
    game.Game().main_loop()
    pygame.quit()


if __name__ == "__main__":
    main()
