import utility.logging
from texture_constants import RenderValues
from rendering.sprites_holder import BasicSprite
import pygame as pg

SHADOW_CLARITY = 10 - RenderValues.SHADOW_QUALITY * 2  # makes even & translates to correct value
SHADOW_CLARITY = min(10 - RenderValues.SHADOW_QUALITY_MIN * 2,
                     max(10 - RenderValues.SHADOW_QUALITY_MAX * 2, SHADOW_CLARITY))  # clamps value

SUN_SLOPE = .8
SUN_SIGN = -.5


class OffsetGoal:
    """ OffsetGoal returns a vector2 depending upon the classes current iteration. The current iteration can be advanced to increase the offset closer to the offset_goal. \n
        Example: \n
        A current_iter of 0 and an iter_length of 5, will have a vector2 offset of: goal_offset * 0   (0%, or 0/5, of the goal_offset: 0, 0) \n
        A current_iter of 1 and an iter_length of 5, will have a vector2 offset of: goal_offset * .2  (20%, or 1/5, of the goal_offset)
    """

    def __init__(self, iteration_len: int, goal_offset: pg.Vector2, reverse=False):
        self.iteration_len = iteration_len
        self.current_iteration = 0
        self.reverse = reverse
        self.finished = False

        self.goal_offset = goal_offset
        self.offset_iterations: list[pg.Vector2] = self.create_iteration_list()

    def create_iteration_list(self) -> list[pg.Vector2]:
        li = []

        for i in range(self.iteration_len):
            offset = pg.Vector2(self.goal_offset * (i / self.iteration_len))
            li.append(offset)

        if self.reverse:
            return li[::-1]
        return li

    def advance_iteration(self):
        if self.current_iteration < self.iteration_len:
            self.current_iteration += 1
        else:
            self.finished = True

    def get_current_offset(self) -> pg.Vector2:
        return self.offset_iterations[self.current_iteration - 1]


class Shadow:
    def __init__(self, surface: pg.surface.Surface, sprite: pg.surface.Surface, position: pg.Vector2, logger: utility.logging.Logger):
        self.logger = logger
        self.surface = surface
        self.sprite = sprite

        self.shadow_offset: pg.Vector2 = pg.Vector2(0, 0)
        self.shadow_offset_goal: OffsetGoal | None = None

        self.shadow_strips_group = pg.sprite.Group()
        self.update_shadow_elements(position)

    def update_shadow_elements(self, position: pg.Vector2):
        """ Split the image into horizontal strips.
        WARNING: updating this too often is heavy on performance, SHADOW_QUALITY can be turned down as well
        """
        color_key = self.sprite.get_colorkey()
        blank_col = (0, 0, 0, 0)
        transparent = color_key if color_key else blank_col

        if self.shadow_offset_goal:
            self.shadow_offset_goal.advance_iteration()
            if self.shadow_offset_goal.finished:
                self.shadow_offset_goal = None

        shadow_strips: list[BasicSprite] = []
        for y_row in range(self.sprite.get_height()):
            if SHADOW_CLARITY == 0 or y_row % SHADOW_CLARITY == 0:
                horizontal_strip = pg.Surface((self.sprite.get_width(), 1)).convert_alpha()
                horizontal_strip.fill(blank_col)

                # set colour
                for x_column in range(self.sprite.get_width()):
                    pixel_colour = self.sprite.get_at((x_column, y_row))
                    if pixel_colour != transparent:
                        horizontal_strip.set_at((x_column, 0), (10, 0, 10, RenderValues.SHADOW_ALPHA if SHADOW_CLARITY else RenderValues.SHADOW_ALPHA / 2))  # sets colour value (if on highest quality, halve alpha)

                # scale horizontal strips' height
                if SHADOW_CLARITY:
                    horizontal_strip = pg.transform.scale(horizontal_strip, (
                        horizontal_strip.get_width(),
                        horizontal_strip.get_height() * (SHADOW_CLARITY / 2)))

                # create position
                angled = pg.Vector2(
                    (self.sprite.get_rect().x + (self.sprite.get_height() - y_row) * SUN_SLOPE * SUN_SIGN),
                    (self.sprite.get_rect().bottom - 1 + (self.sprite.get_height() - y_row) * SUN_SIGN))

                pos = pg.Vector2((position.x - self.sprite.get_width() / 2 + angled.x) + self.shadow_offset.x,
                                 (position.y - self.sprite.get_height() / 2 + angled.y) + self.shadow_offset.y)

                # offset goal
                if self.shadow_offset_goal:
                    pos = pg.Vector2(pos.x + self.shadow_offset_goal.get_current_offset().x,
                                     pos.y + self.shadow_offset_goal.get_current_offset().y)

                shadow_strips.append(BasicSprite(horizontal_strip, pos))
        self.shadow_strips_group.empty()
        self.shadow_strips_group.add(*shadow_strips)

    def draw(self):
        """ Draw each strip of the shadow offsetting the x-axis accordingly. """
        self.shadow_strips_group.draw(self.surface)

    def add_offset_goal(self, iteration_len, goal_offset, reverse=False):
        self.shadow_offset_goal = OffsetGoal(iteration_len, goal_offset, reverse)

    def update_shadow(self, position: pg.Vector2, new_sprite: pg.surface.Surface = None, offset: pg.Vector2 = pg.Vector2(0, 0)):
        """ Updates the shadow with a new position and a new sprite """
        if not new_sprite:
            new_sprite = self.sprite
        self.sprite = new_sprite
        self.shadow_offset = offset
        self.update_shadow_elements(position)
