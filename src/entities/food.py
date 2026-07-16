import pygame

class Food():
    def __init__(self, x, y, radius, color, type_food):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.type_food = type_food
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)



