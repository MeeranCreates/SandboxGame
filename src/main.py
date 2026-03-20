import pygame
from settings import Settings
from player.player import Player
from world.world import World

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sandbox:2D")
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

        self.settings = Settings()
        self.world = World(self.screen)
        self.player = Player(self.screen, pos=(100, 100), blocks=self.world.blocks)

    def run(self):
        self.world.generate()
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
            self.world.draw()
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()