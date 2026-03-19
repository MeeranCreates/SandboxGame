import pygame
from settings import Settings
from player.player import Player

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sandbox:2D")
        self.screen = pygame.display.set_mode((1024, 768))
        self.clock = pygame.time.Clock()
        self.running = True

        self.settings = Settings()
        self.player = Player(self.screen, (100, 100))

    def run(self):
        while self.running:
            self.clock.tick(self.settings.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.player.update()

            # draw
            self.screen.fill((0, 0, 0))
            self.player.draw()
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()