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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.horse.move(dx=0, dy=-5)
                elif event.key == pygame.K_DOWN:
                    self.horse.move(dx=0, dy=5)
                elif event.key == pygame.K_LEFT:
                    self.horse.move(dx=-5, dy=0)
                elif event.key == pygame.K_RIGHT:
                    self.horse.move(dx=5, dy=0)

    def update(self):
        pass

    def render(self):
        self.screen.fill(settings.BLACK)
        self.horse.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(settings.FPS)


if __name__ == "__main__":
    game = Game()
    game.run()







