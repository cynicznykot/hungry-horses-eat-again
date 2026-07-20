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

        if self.rect.left <= 0:
            self.rect.left = 0
            self.dx = random.choice([1, 2]) * self.speed
        elif self.rect.right >= screen_width:
            self.rect.right = screen_width
            self.dx = -random.choice([1, 2]) * self.speed

        if self.rect.top <= 0:
            self.rect.top = 0
            self.dy = random.choice([1, 2]) * self.speed
        elif self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.dy = -random.choice([1, 2]) * self.speed
        self.change_direction_timer += 1
        if self.change_direction_timer >= self.change_interval:
            self.dx = random.choice([-self.speed, self.speed])
            self.dy = random.choice([-self.speed, self.speed])
            self.change_direction_timer = 0
            self.change_interval = random.randint(60, 100)

    def draw(self, screen):
        """Draw the enemy on the screen"""

        pygame.draw.rect(screen, self.color, self.rect)