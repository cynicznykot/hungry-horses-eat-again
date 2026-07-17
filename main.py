import pygame
import os
import random
from src.entities.horse import Horse
import src.settings as settings
from src.entities.food import Food, Apple, Carrot, Berry


class Game():
    # Main Class Game
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Hungry Horses Eat Again")
        self.clock = pygame.time.Clock()
        self.running = True
        self.herd = [Horse(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2, 40, 40, settings.BROWN)]
        self.next_horse_score = 5
        self.head_positions = []
        self.direction = (0, 0)
        self.keys_pressed = set()
        self.foods = []
        self.total_food_to_collect = 10
        self.score = 0
        self.target_score = 50
        self.food_values = {
            'apple': 5,
            'carrot': 4,
            'berry': 3
        }
        self.spawn_food_set(3)
        self.level_completed = False

        grass_path = os.path.join("src", "assets", "images", "bg_green_grass.jpg")
        self.bg_green_grass = pygame.image.load(grass_path)
        self.bg_green_grass = pygame.transform.scale(self.bg_green_grass, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        music_path = os.path.join("src", "assets", "sounds", "FoamRubber.mp3")
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except pygame.error:
            print("Don't load music file.")

        eat_sound_path = os.path.join("src", "assets", "sounds", "eat_food.mp3")
        self.eat_sound = pygame.mixer.Sound(eat_sound_path)


        dark_overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        dark_overlay.fill((0, 0, 0))
        dark_overlay.set_alpha(80)
        self.bg_green_grass.blit(dark_overlay, (0, 0))


    def handle_events(self):
        # Player control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.keys_pressed.add(pygame.K_UP)
                elif event.key == pygame.K_DOWN:
                    self.keys_pressed.add(pygame.K_DOWN)
                elif event.key == pygame.K_LEFT:
                    self.keys_pressed.add(pygame.K_LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.keys_pressed.add(pygame.K_RIGHT)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.keys_pressed.discard(pygame.K_UP)
                elif event.key == pygame.K_DOWN:
                    self.keys_pressed.discard(pygame.K_DOWN)
                elif event.key == pygame.K_LEFT:
                    self.keys_pressed.discard(pygame.K_LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.keys_pressed.discard(pygame.K_RIGHT)


    def update(self):
        # Move head
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

        # Bounds for x-coordinates
        if self.herd[0].rect.x < 0:
            self.herd[0].rect.x = 0
        elif self.herd[0].rect.x > settings.SCREEN_WIDTH - self.herd[0].rect.width:
            self.herd[0].rect.x = settings.SCREEN_WIDTH - self.herd[0].rect.width
        # Bounds for y-coordinates
        if self.herd[0].rect.y < 0:
            self.herd[0].rect.y = 0
        elif self.herd[0].rect.y > settings.SCREEN_HEIGHT - self.herd[0].rect.height:
            self.herd[0].rect.y = settings.SCREEN_HEIGHT - self.herd[0].rect.height

        # Save head positions in history
        self.head_positions.insert(0, (self.herd[0].rect.x, self.herd[0].rect.y))

        # Limiting the history lenght
        max_history = len(self.herd) * 20 + 20
        if len(self.head_positions) > max_history:
            self.head_positions = self.head_positions[:max_history]

        # Move tail
        step = 15
        for i in range(1, len(self.herd)):
            position_index = i * step
            if position_index < len(self.head_positions):
                self.herd[i].rect.x = self.head_positions[position_index][0]
                self.herd[i].rect.y = self.head_positions[position_index][1]

        # The arrival of the food at the right level
        i = 0
        while i < len(self.foods):
            food = self.foods[i]
            if self.herd[0].rect.colliderect(food.rect):
                self.eat_sound.play()
                self.foods.pop(i)
                self.score += self.food_values[food.food_types]

                if self.score >= self.target_score:
                    self.level_completed = True
                    self.running = False
                else:
                    new_type = random.choice(['apple', 'carrot', 'berry'])
                    self.spawn_single_food(new_type)

                break
            else:
                i += 1

        # Add new horses when reaching 5, 10, 15 points etc
        if self.score >= self.next_horse_score:
            last_horse = self.herd[-1]
            new_horse = Horse(last_horse.rect.x, last_horse.rect.y, 40, 40, settings.BROWN)
            self.herd.append(new_horse)
            self.next_horse_score += 5

    def render(self):
        # Clear screen and draw all game objects
        self.screen.blit(self.bg_green_grass, (0, 0))

        # Render foods
        for food in self.foods:
            food.draw(self.screen)

        # Render horses (head and tail)
        for horse in self.herd:
            horse.draw(self.screen)

        # Score text
        font_small = pygame.font.Font(None, 36)
        score_text = font_small.render(f"Score: {self.score} / {self.target_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # Level completion notification
        if self.level_completed:
            font = pygame.font.Font(None, 74)
            text = font.render("Level completed!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

        pygame.display.flip()


    def run(self):
        # Main game loop
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(settings.FPS)

        pygame.time.wait(2000)
        pygame.quit()


    def spawn_single_food(self, food_type):
        x = random.randint(0, settings.SCREEN_WIDTH)
        y = random.randint(0, settings.SCREEN_HEIGHT)

        temp_rect = pygame.Rect(x - 10, y - 10, 20, 20)
        while temp_rect.colliderect(self.herd[0].rect):
            x = random.randint(0, settings.SCREEN_WIDTH)
            y = random.randint(0, settings.SCREEN_HEIGHT)
            temp_rect = pygame.Rect(x - 10, y - 10, 20, 20)

        if food_type == 'apple':
            food = Apple(x, y)
        elif food_type == 'carrot':
            food = Carrot(x, y)
        elif food_type == 'berry':
            food = Berry(x, y)
        else:
            return

        self.foods.append(food)

    def spawn_food_set(self, count):
        self.foods = []

        food_types = ['apple', 'carrot', 'berry']
        for i in range(min(count, len(food_types))):
            self.spawn_single_food(food_types[i])


if __name__ == "__main__":
    game = Game()
    game.run()







