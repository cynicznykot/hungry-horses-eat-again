import pygame

class Food():
    # Main class Food for feature inheritance
    def __init__(self, x, y, food_types, radius, color):
        self.x = x
        self.y = y
        self.food_types = food_types
        self.radius = radius
        self.color = color
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Apple(Food):
    def __init__(self, x, y):
        super().__init__(x, y, 'apple', 12, (255, 50, 50))

class Carrot(Food):
    def __init__(self, x, y):
        super().__init__(x, y, 'carrot', 10, (255, 140, 0))

class Berry(Food):
    def __init__(self, x, y):
        super().__init__(x, y, 'berry', 8, (128, 0, 128))




