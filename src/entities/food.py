"""
Food classes for the Hungry Horses Eat Again.

Contains base Food class and specific food types (buff and debuff)
"""

import pygame


class Food:
    """Base class for all food items."""

    def __init__(self, x, y, food_types, radius, color):
        self.x = x
        self.y = y
        self.food_types = food_types
        self.radius = radius
        self.color = color
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


# ===== BUFF FOOD (GIVE POSITIVE EFFECTS) =====


class RedApple(Food):
    """Red apple food item. Gives 5 points"""

    def __init__(self, x, y):
        super().__init__(x, y, food_types='red_apple', radius=20, color=(255, 50, 50))


class OrangeCarrot(Food):
    """Orange carrot food item. Gives 4 points"""

    def __init__(self, x, y):
        super().__init__(x, y, food_types='orange_carrot', radius=18, color=(255, 140, 0))


class PurpleBerry(Food):
    """Purple berry food item. Gives 3 points"""

    def __init__(self, x, y):
        super().__init__(x, y, food_types='purple_berry', radius=16, color=(128, 0, 128))


# ===== DEBUFF FOOD (GIVE NEGATIVE EFFECTS) =====


class RottenApple(Food):
    """Rotten apple food item. Currently not used yet"""

    def __init__(self, x, y):
        super().__init__(x, y, food_types='rotten_apple', radius=18, color=(100, 50, 50))


class PoisonBerry(Food):
    """Poison berry food item. Currently not used yet"""

    def __init__(self, x, y):
        super().__init__(x, y, food_types='poison_berry', radius=18, color=(80, 0, 80))





