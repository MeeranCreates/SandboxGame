import pygame

class World:
    def __init__(self, screen):
        self.screen = screen
        self.block_size = 32
        self.blocks = []

        # block image
        self.dirt = pygame.Surface((32, 32))
        self.dirt.fill((139, 69, 19))  # brown

        self.generate()

    def generate(self):
        for x in range(25):
            cloumb = []
            for y in range (20):
                if y > 10:  # simple ground layer        
                    cloumb.append(1) # 1 represents dirt block
            self.blocks.append(cloumb)
            

        print(f"Generated world with {len(self.blocks)} blocks.")
        print(self.blocks)

    def draw(self,offset=pygame.math.Vector2(0, 0)):
        for x, row in enumerate(self.blocks):
            for y, block_type in enumerate(row):
                if block_type == 1:  # dirt block
                    block_pos = (x * self.block_size + offset.x, y * self.block_size + offset.y)
                    self.screen.blit(self.dirt, block_pos)