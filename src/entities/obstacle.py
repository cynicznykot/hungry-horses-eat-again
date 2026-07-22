"""
Obstacle class for the Hungry Horses Eat Again game.

Represents static obstacles like horses, trees or rocks.
"""

import pygame


class Obstacle:
    """A static obstacle in the game world (houses, rocks, trees)."""

    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

