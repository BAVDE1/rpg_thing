from constants import *
import game


def main():
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_icon(pg.image.load("assets/textures/old_player.png"))  # change this later
    pg.display.set_mode([RESOLUTION_Y, RESOLUTION_X])
    game.Game().main_loop()
    pg.quit()


if __name__ == "__main__":
    main()
