from constants import GameUnits

import pygame as pg
import game


def main():
    pg.init()
    pg.display.set_caption(GameUnits.CAPTION)
    pg.display.set_icon(pg.image.load("assets/textures/old_player.png"))  # change this later
    pg.display.set_mode([GameUnits.RESOLUTION_Y, GameUnits.RESOLUTION_X])
    game.Game().main_loop()
    pg.quit()


if __name__ == "__main__":
    main()
