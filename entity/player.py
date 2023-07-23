import time
from constants import *


class Player:
    def __init__(self, centre_screen):
        # https://www.pg.org/docs/tut/SpriteIntro.html
        self.direction = "n"
        self.texture = pg.image.load(PLAYER_TEXTURE).convert_alpha()

        self.position = pg.Vector2(centre_screen[0], centre_screen[1])
        self.sprite_pos = self.position

        self.moving = False
        self.sprinting = False
        self.last_moved = time.time()

    def move(self):
        """ Moves player from user input """
        self.moving = True

        x = DIRECTION_MOV[self.direction][0]
        y = DIRECTION_MOV[self.direction][1]
        self.position = pg.Vector2(self.position.x + x, self.position.y + y)
        self.last_moved = time.time()

        # sprite pos animation / movement here
        self.sprite_pos = self.position

        self.moving = False

    def set_pos(self, x, y):
        """ Sets player position instantly """
        self.moving = True
        self.position.x = x
        self.position.y = y
        self.last_moved = time.time()
        self.moving = False

    def can_move(self):
        """ Returns true if the player is allowed to move """
        return not self.moving and time.time() - MOVEMENT_PAUSE > self.last_moved

    def render_player(self, surface):
        sprite = pg.transform.scale(self.texture, (UNIT, UNIT))
        blit_xy = (self.sprite_pos.x - sprite.get_width() // 2,
                   self.sprite_pos.y - sprite.get_height() // 2)

        surface.blit(sprite, blit_xy)
