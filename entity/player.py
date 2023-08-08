import time
from constants import *
from rendering.shadow import render_shadow
from utility.tweening import LinearTween

tween_x = None
tween_y = None


class Player:
    def __init__(self, centre_screen):
        # https://www.pg.org/docs/tut/SpriteIntro.html
        self.direction = UP
        self.texture = pg.image.load(PLAYER_TEXTURE).convert_alpha()

        self.position = pg.Vector2(centre_screen[0], centre_screen[1])
        self.sprite_pos = self.position
        self.flipped = False

        self.moving = False
        self.sprinting = False
        self.last_moved = time.time()

    def move(self):
        """ Moves player from user input """
        global tween_x
        global tween_y
        self.moving = True

        x = DIRECTION_MOV[self.direction][0]
        y = DIRECTION_MOV[self.direction][1]
        self.position = pg.Vector2(self.position.x + x, self.position.y + y)
        self.last_moved = time.time()

        # sprite pos animation / movement here
        if self.direction == LEFT and not self.flipped:
            self.flipped = True
        elif self.direction == RIGHT and self.flipped:
            self.flipped = False

        if x:
            tween_x = LinearTween(self.sprite_pos.x, self.position.x, MOVEMENT_PAUSE)
        elif y:
            tween_y = LinearTween(self.sprite_pos.y, self.position.y, MOVEMENT_PAUSE)

        # TODO: send beat event (after player movement)

        self.moving = False

    def set_pos(self, x, y):
        """ Sets player position instantly """
        self.moving = True
        self.position.x = x
        self.position.y = y
        self.sprite_pos.x = x
        self.sprite_pos.y = y
        self.last_moved = time.time()
        self.moving = False

    def can_move(self):
        """ Returns true if the player is allowed to move """
        return not self.moving and time.time() - MOVEMENT_PAUSE > self.last_moved

    def render_player(self, surface: pg.Surface):
        global tween_x
        global tween_y

        if isinstance(tween_x, LinearTween):
            self.sprite_pos.x = tween_x.get_value()
            if tween_x.has_reached_goal():
                tween_x = None

        if isinstance(tween_y, LinearTween):
            self.sprite_pos.y = tween_y.get_value()
            if tween_y.has_reached_goal():
                tween_y = None

        sprite = pg.transform.scale(self.texture, (UNIT, UNIT))
        if self.flipped:
            sprite = pg.transform.flip(sprite, 1, 0)

        blit_xy = (self.sprite_pos.x - sprite.get_width() // 2,
                   self.sprite_pos.y - sprite.get_height() // 2)

        render_shadow(sprite, blit_xy, surface)
        surface.blit(sprite, blit_xy)

# https://github.com/nobrelli/tweener
