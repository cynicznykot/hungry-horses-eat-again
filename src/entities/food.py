import pygame

class Food():
    # Main class Food for feature inheritance
    def __init__(self, x, y, food_types):
        self.x = x
        self.y = y
        self.food_types = food_types
        self.rect = pygame.Rect(x - 10, y - 10, 20, 20)

        if food_types == 'apple':
            self.color = (255, 50, 50)
            self.radius = 10
        elif food_types == 'carrot':
            self.color = (255, 140, 0)
            self.radius = 12
        elif food_types == 'berry':
            self.color = (128, 0, 128)
            self.radius = 8
        else:
            self.color = (255, 255, 255)  # white if food_types is None.
            self.radius = 10

        self.rect = pygame.Rect(
            x - self.radius,
            y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)



