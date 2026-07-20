import pygame
import random


class Enemy:
    """A basic enemy that moves in random direction"""

    def __init__(self, x, y, size, speed, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.speed = speed

        self.dx = random.choice([-speed, speed])
        self.dy = random.choice([-speed, speed])

        self.change_direction_timer = 0
        self.change_interval = random.randint(60, 100)

    def update(self, screen_width, screen_height):
        """Update enemy position and change direction randomly"""

        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.x <= 0 or self.rect.x >= screen_width:
            self.dx = -self.dx
        if self.rect.y <= 0 or self.rect.y >= screen_height:
            self.dy = -self.dy

        self.change_direction_timer += 1
        if self.change_direction_timer >= self.change_interval:
            self.dx = random.choice([-self.speed, -self.speed])
            self.dy = random.choice([-self.speed, -self.speed])
            self.change_direction_timer = 0
            self.change_interval = random.randint(60, 100)

    def draw(self, screen):
        """Draw the enemy on the screen"""

        pygame.draw.rect(screen, self.color, self.rect)