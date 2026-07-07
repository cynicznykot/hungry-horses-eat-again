import pygame
from src.entities.horse import Horse
import src.settings as settings


class Game(): # main class Game
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Hungry Horses Eat Again")
        self.clock = pygame.time.Clock()
        self.running = True
        self.horse = Horse(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2, 40, 40, settings.YELLOW)
        self.direction = (0, 0)
        self.keys_pressed = set()


    def handle_events(self): # Player control
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


    def update(self): # Smoothness of movement
        dx, dy = 0, 0
        if pygame.K_UP in self.keys_pressed:
            dy = -5
        if pygame.K_DOWN in self.keys_pressed:
            dy = 5
        if pygame.K_LEFT in self.keys_pressed:
            dx = -5
        if pygame.K_RIGHT in self.keys_pressed:
            dx = 5

        self.horse.move(dx, dy)

        # Bounds for x-coordinates
        if self.horse.rect.x < 0:
            self.horse.rect.x = 0
        elif self.horse.rect.x > settings.SCREEN_WIDTH - self.horse.rect.width:
            self.horse.rect.x = settings.SCREEN_WIDTH - self.horse.rect.width

        # Bounds for y-coordinates
        if self.horse.rect.y < 0:
            self.horse.rect.y = 0
        elif self.horse.rect.y > settings.SCREEN_HEIGHT - self.horse.rect.height:
            self.horse.rect.y = settings.SCREEN_HEIGHT - self.horse.rect.height

    def render(self):
        # Clear screen and draw all game objects
        self.screen.fill(settings.BLACK)
        self.horse.draw(self.screen)
        pygame.display.flip()


    def run(self):
        # Main game loop
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(settings.FPS)


if __name__ == "__main__":
    game = Game()
    game.run()







