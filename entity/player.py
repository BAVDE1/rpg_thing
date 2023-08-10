import time
from constants import *
from rendering.rendering_other import split_sheet
from utility.animator import Animator


class Player:
    def __init__(self, gm, centre_screen):
        self.game = gm
        self.direction = UP
        self.position = pg.Vector2(centre_screen[0], centre_screen[1])
        self.sprite_pos = self.position
        self.flipped = False

        self.texture_idle = pg.image.load(PLAYER_IDLE).convert_alpha()
        self.ss_idle = split_sheet(self.texture_idle, (BASE_UNIT, BASE_UNIT), 4)

        # todo: make first frame of ss_idle for the init (will change around depending on Animator obviously)
        self.current_texture = None
        self.animator = Animator(self.game, self.current_texture, [PLAYER_IDLE, self.ss_idle], False)

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

        self.flipped = True if self.direction == LEFT else False if self.direction == RIGHT else self.flipped
        self.sprite_pos = self.position

        # TODO: send beat event (after player movement)

        self.moving = False

    def set_pos(self, x, y):
        """ Sets player position & sprite pos instantly """
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

    def animate_player(self):
        self.animator.update()
        self.current_texture = self.animator.texture_obj

    def render_player(self, surface: pg.Surface):
        self.animate_player()

        if self.current_texture:
            sprite = pg.transform.scale(self.current_texture, (UNIT, UNIT))
            if self.flipped:
                sprite = pg.transform.flip(sprite, 1, 0)

            blit_xy = (self.sprite_pos.x - sprite.get_width() // 2,
                       self.sprite_pos.y - sprite.get_height() // 2)

            surface.blit(sprite, blit_xy)
