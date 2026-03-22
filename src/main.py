import pygame
from player.player import Player
from world.world import World

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Sandbox 2D")

        self.clock = pygame.time.Clock()
        self.running = True

        self.world = World(self.screen)
        self.player = Player(self.screen, self.world.blocks, (100, 100))

        self.offset = pygame.math.Vector2(0, 0)

    def run(self):
        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.player.update()

            # camera follow
            self.offset.x = self.player.rect.centerx - self.screen.get_width() // 2
            self.offset.y = self.player.rect.centery - self.screen.get_height() // 2

            self.screen.fill((0, 0, 0))

            self.world.draw(self.offset)
            self.player.draw(self.offset)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    Game().run()