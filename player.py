import time
import pygame

movement_pause = 0.1


class Player:
    def __init__(self, x_pos, y_pos, surface):
        self.position = pygame.Vector2(x_pos, y_pos)
        self.surface = surface
        self.moving = False
        self.last_moved = time.time()

    def move(self, x, y):
        """ Moves player from user input """
        self.position = pygame.Vector2(self.position.x + x, self.position.y + y)
        self.last_moved = time.time()

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
        return not self.moving and time.time() - movement_pause > self.last_moved

    def draw_player(self, unit):
        pygame.draw.circle(self.surface, "yellow", self.position, unit / 2)
