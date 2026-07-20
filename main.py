"""
Main game module for Hungry Horses Eat Again.

Handles game initialization, main loop, events and game logic.
"""

import pygame
import os
import random

from src.entities.horse import Horse
import src.settings as settings
from src.entities.food import Food, RedApple, OrangeCarrot, PurpleBerry
from src.entities.obstacle import Obstacle


class Game():
    """Main game class."""

    def __init__(self):
        """Initialize the game window, objects and resources."""

        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Hungry Horses Eat Again")
        self.clock = pygame.time.Clock()
        self.running = True

        self.keys_pressed = set()

        # === HERD (SNAKE) =====
        start_x = settings.SCREEN_WIDTH // 2
        start_y = settings.SCREEN_HEIGHT // 2
        self.herd = [Horse(start_x, start_y, 40, 40, settings.BROWN)]

        self.head_positions = []  # Maybe we need to rewrite the logic

        # === GAME PARAMETERS ===
        self.score = 0
        self.target_score = 50
        self.next_horse_score = 5
        self.level_completed = False

        # === FOOD SYSTEM ===
        self.foods = []
        self.food_values = {'red_apple': 5, 'orange_carrot': 4, 'purple_berry': 3}
        self.spawn_food_set(3)

        # === LOAD RESOURCES ===
        self.load_background()
        self.load_music()
        self.load_sound_effects()

        self.spawn_obstacles(5)

        # ---------- RESOURCE LOADING ----------

    def load_background(self):
        """Load and scale the background image with a dark overlay."""

        grass_path = os.path.join("src", "assets", "images", "bg_green_grass.jpg")
        self.bg_green_grass = pygame.image.load(grass_path)
        self.bg_green_grass = pygame.transform.scale(self.bg_green_grass,
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        # Dark overlay for better visibility
        dark_overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        dark_overlay.fill((0, 0, 0))
        dark_overlay.set_alpha(80)
        self.bg_green_grass.blit(dark_overlay, (0, 0))

    def load_music(self):
        """Load and play background music."""

        music_path = os.path.join("src", "assets", "sounds", "FoamRubber.mp3")
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except pygame.error:
            print("Don't load music file.")

    def load_sound_effects(self):
        """Load sound effects."""

        eat_sound_path = os.path.join("src", "assets", "sounds", "eat_food.mp3")
        self.eat_sound = pygame.mixer.Sound(eat_sound_path)

    # ---------- EVENT HANDLING ----------

    def handle_events(self):
        """Process all input events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # === Arrow Keys ===
                if event.key == pygame.K_UP:
                    self.keys_pressed.add(pygame.K_UP)
                elif event.key == pygame.K_DOWN:
                    self.keys_pressed.add(pygame.K_DOWN)
                elif event.key == pygame.K_LEFT:
                    self.keys_pressed.add(pygame.K_LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.keys_pressed.add(pygame.K_RIGHT)

                # === WASD ===
                elif event.key == pygame.K_w:
                    self.keys_pressed.add(pygame.K_UP)
                elif event.key == pygame.K_s:
                    self.keys_pressed.add(pygame.K_DOWN)
                elif event.key == pygame.K_a:
                    self.keys_pressed.add(pygame.K_LEFT)
                elif event.key == pygame.K_d:
                    self.keys_pressed.add(pygame.K_RIGHT)

            if event.type == pygame.KEYUP:
                # === Arrow Keys ===
                if event.key == pygame.K_UP:
                    self.keys_pressed.discard(pygame.K_UP)
                elif event.key == pygame.K_DOWN:
                    self.keys_pressed.discard(pygame.K_DOWN)
                elif event.key == pygame.K_LEFT:
                    self.keys_pressed.discard(pygame.K_LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.keys_pressed.discard(pygame.K_RIGHT)

                # === WASD ===
                elif event.key == pygame.K_w:
                    self.keys_pressed.discard(pygame.K_UP)
                elif event.key == pygame.K_s:
                    self.keys_pressed.discard(pygame.K_DOWN)
                elif event.key == pygame.K_a:
                    self.keys_pressed.discard(pygame.K_LEFT)
                elif event.key == pygame.K_d:
                    self.keys_pressed.discard(pygame.K_RIGHT)

    # ---------- GAME LOGIC ----------

    def update(self):
        """Update all game logic each frame"""

        # --- 1. Head Movement ---
        dx, dy = 0, 0
        if pygame.K_UP in self.keys_pressed:
            dy = -3
        if pygame.K_DOWN in self.keys_pressed:
            dy = 3
        if pygame.K_LEFT in self.keys_pressed:
            dx = -3
        if pygame.K_RIGHT in self.keys_pressed:
            dx = 3

        self.herd[0].move(dx, dy)

        # --- 2. Screen Boundaries for Head ---
        if self.herd[0].rect.x < 0:
            self.herd[0].rect.x = 0
        elif self.herd[0].rect.x > settings.SCREEN_WIDTH - self.herd[0].rect.width:
            self.herd[0].rect.x = settings.SCREEN_WIDTH - self.herd[0].rect.width

        if self.herd[0].rect.y < 0:
            self.herd[0].rect.y = 0
        elif self.herd[0].rect.y > settings.SCREEN_HEIGHT - self.herd[0].rect.height:
            self.herd[0].rect.y = settings.SCREEN_HEIGHT - self.herd[0].rect.height

        # --- 3. Save Head Positions History ---
        current_pos = (self.herd[0].rect.x, self.herd[0].rect.y)

        if not self.head_positions or self.head_positions[0] != current_pos:
            self.head_positions.insert(0, current_pos)

        # Limit history length to prevent unlimited growth
        max_history = len(self.herd) * 20 + 20
        if len(self.head_positions) > max_history:
            self.head_positions = self.head_positions[:max_history]

        # --- 4. Move Tail ---
        step = 15
        for i in range(1, len(self.herd)):
            position_index = i * step
            if position_index < len(self.head_positions):
                self.herd[i].rect.x = self.head_positions[position_index][0]
                self.herd[i].rect.y = self.head_positions[position_index][1]

        # --- 5. Food Collection
        # Check head collision with food
        i = 0
        while i < len(self.foods):
            food = self.foods[i]
            if self.herd[0].rect.colliderect(food.rect):
                self.eat_sound.play()
                self.foods.pop(i)
                self.score += self.food_values[food.food_types]

                # Check if level is complete
                if self.score >= self.target_score:
                    self.level_completed = True
                    self.running = False
                else:
                    # Spawn a new food of random type
                    new_type = random.choice(['red_apple', 'orange_carrot', 'purple_berry'])
                    self.spawn_single_food(new_type)

                break
            else:
                i += 1

        # --- 6. Add New Horse ---
        # Every 5 points a new horse is added to the herd
        if self.score >= self.next_horse_score:
            last_horse = self.herd[-1]
            new_horse = Horse(
                last_horse.rect.x,
                last_horse.rect.y,
                40,
                40,
                settings.BROWN)
            self.herd.append(new_horse)
            self.next_horse_score += 5

        for obstacle in self.obstacles:
            if self.herd[0].rect.colliderect(obstacle.rect):
                self.herd[0].move(-dx, -dy)
                return

    # ---------- RENDERING ----------

    def render(self):
        """Render all game objects to the screen"""

        # 1. Background (grass)
        self.screen.blit(self.bg_green_grass, (0, 0))

        # 2. Food items
        for food in self.foods:
            food.draw(self.screen)

        # 3. Herd (head and tail)
        for horse in self.herd:
            horse.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # 4. Score display (UI)
        font_small = pygame.font.Font(None, 36)
        score_text = font_small.render(f"Score: {self.score} / {self.target_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # 5. Level completion message
        if self.level_completed:
            font = pygame.font.Font(None, 74)
            text = font.render("Level completed!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)


        pygame.display.flip()


    def run(self):
        """Main game loop"""

        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(settings.FPS)

        # Delay before closing so the player can see the message
        pygame.time.wait(2000)
        pygame.quit()


    def spawn_single_food(self, food_types):
        """Spawn one food item of the specified type at a random position"""

        # Define radii for each food type (affects collision detection size)
        radii = {'red_apple': 20, 'orange': 18, 'purple_berry': 16}

        # Get radius for the specified food type, default to 18 if not found
        food_radius = radii.get(food_types, 18)

        # Keep trying until we find a valid position
        while True:
            x = random.randint(food_radius, settings.SCREEN_WIDTH - food_radius)
            y = random.randint(food_radius, settings.SCREEN_HEIGHT - food_radius)
            temp_rect = pygame.Rect(x - food_radius, y - food_radius, food_radius * 2, food_radius * 2)

            # Check if the food overlaps with any horse in the herd
            collision = False
            for horse in self.herd:
                if temp_rect.colliderect(horse.rect):
                    collision = True
                    break

            # If no collision found, exit the loop
            if not collision:
                break

        # Create the appropriate food object based on the type
        if food_types == 'red_apple':
            food = RedApple(x, y)
        elif food_types == 'orange_carrot':
            food = OrangeCarrot(x, y)
        elif food_types == 'purple_berry':
            food = PurpleBerry(x, y)
        else:
            return

        # Add the food to the game's food list
        self.foods.append(food)


    def spawn_food_set(self, count):
        """Spawn a set of food items (one of each type)."""

        self.foods = []
        food_types = ['red_apple', 'orange_carrot', 'purple_berry']
        for i in range(min(count, len(food_types))):
            self.spawn_single_food(food_types[i])


    def spawn_obstacles(self, level):
        """Spawn all obstacles based on the current level"""

        self.obstacles = []

        count = level + 1

        colors = [(0, 255, 0), (128, 128, 128)]

        for _ in range(count):
            attempts = 0
            while attempts < 50:
                width = random.randint(30, 100)
                height = random.randint(30, 100)

                x = random.randint(0, settings.SCREEN_WIDTH - width)
                y = random.randint(0, settings.SCREEN_HEIGHT - height)

                temp_rect = pygame.Rect(x, y, width, height)

                collision = False
                for horse in self.herd:
                    if temp_rect.colliderect(horse.rect):
                        collision = True
                        break

                for obs in self.obstacles:
                    if temp_rect.colliderect(obs.rect):
                        collision = True
                        break

                if not collision:
                    color = random.choice(colors)
                    self.obstacles.append(Obstacle(x, y, width, height, color))
                    break
                attempts += 1


if __name__ == "__main__":
    game = Game()
    game.run()







