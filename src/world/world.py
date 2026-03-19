import pygame

class World:
    def __init__(self, screen):
        self.screen = screen
        self.blocks = []

        # block image
        self.dirt = pygame.Surface((32, 32))
        self.dirt.fill((139, 69, 19))  # brown

        self.generate()

    def generate(self):
        for i in range(20):
            x = i * 32
            y = 500  # ground level
            self.blocks.append((self.dirt, (x, y)))

    def draw(self):
        for block, pos in self.blocks:
            self.screen.blit(block, pos)