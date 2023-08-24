import time
from constants import *
from rendering.rendering_other import split_sheet
from utility.animator import Animator


class Player:
    def __init__(self, game, screen: pg.Surface, centre_screen):
        self.game = game
        self.surface = screen
        self.direction = UP
        self.position = pg.Vector2(centre_screen[0], centre_screen[1])
        self.sprite_pos = self.position
        self.flipped = False

        self.texture_idle = pg.image.load(PLAYER_IDLE).convert_alpha()
        self.ss_idle = split_sheet(self.texture_idle, (BASE_UNIT, BASE_UNIT), 4)

        self.current_texture = None
        self.animator = Animator(self.game, [PLAYER_IDLE, self.ss_idle], False,
                                 [PLAYER_JUMP, split_sheet(pg.image.load(PLAYER_JUMP).convert_alpha(), (BASE_UNIT * 2, BASE_UNIT * 2), 8)],
                                 [PLAYER_IDLE_DEBUG, split_sheet(pg.image.load(PLAYER_IDLE_DEBUG).convert_alpha(), (BASE_UNIT, BASE_UNIT), 4)])

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
        self.sprite_pos = self.position  # will need to be changed based on animation

        self.animator.do_animation(PLAYER_JUMP, 0.13, offset_x=-UNIT / 2 if x > 0 else UNIT / 2, offset_y=-UNIT / 2)  # jump anim

        # todo: send beat event (after player movement)

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
        # TODO: replace out animator.current_anim_ss with some other solution to the animation jumping
        return not self.moving and not self.animator.current_anim_ss and time.time() - MOVEMENT_PAUSE > self.last_moved

    def render_player(self):
        self.animator.update()
        self.current_texture = self.animator.texture_obj

        if self.is_player_loaded():
            sprite = pg.transform.scale(self.current_texture, (self.current_texture.get_width() * RES_MUL, self.current_texture.get_height() * RES_MUL))
            if self.flipped:
                sprite = pg.transform.flip(sprite, 1, 0)

            blit = ((self.sprite_pos.x - sprite.get_width() // 2) + self.animator.offset_x,
                    (self.sprite_pos.y - sprite.get_height() // 2) + self.animator.offset_y)

            self.surface.blit(sprite, blit)

    def is_player_loaded(self):
        """ Returns whether player has fully loaded in (add more checks later) """
        return self.current_texture
