"""
Horse class for the Hungry Horses Eat Again.

Represents a single horse in the herd with position, size, color,
and methods for drawing and movement.
"""

import pygame


class Horse:
    """ A horse entity in the game."""

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)





