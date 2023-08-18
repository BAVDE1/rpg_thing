from constants import *


fps = 60
running = True
clock = pg.time.Clock()


def events():
    global running

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False  # close game


def main_loop():
    while running:
        events()
        clock.tick(fps)


def main():
    pg.init()
    pg.display.set_caption("Level editor")
    pg.display.set_mode([RESOLUTION_X * 2, RESOLUTION_X])
    main_loop()
    pg.quit()


if __name__ == "__main__":
    main()
