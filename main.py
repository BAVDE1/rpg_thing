import pygame as pg

from constants import GameUnits
from game import Game

game: Game | None = None


def main():
    global game

    pg.init()
    pg.display.set_caption(GameUnits.CAPTION)
    pg.display.set_icon(pg.image.load("assets/textures/player/old_player.png"))  # change this later
    pg.display.set_mode([GameUnits.RES_W * GameUnits.RES_MUL, GameUnits.RES_H * GameUnits.RES_MUL])

    game = Game()
    game.main_loop()

    pg.quit()


if __name__ == "__main__":
    main()
