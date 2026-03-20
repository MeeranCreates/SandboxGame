import pygame
import math
import random

# Placeholder Perlin noise function for hills
def perlin_noise(x, scale=20, octaves=1, persistence=0.5, lacunarity=2.0, seed=0):
    # This is a stub for Perlin noise. Replace with a real implementation for smooth hills.
    random.seed(int(x * scale + seed))
    return random.uniform(-1, 1)

class World:
    def __init__(self, screen):
        self.screen = screen
        self.block_size = 32
        self.width = 200
        self.height = 50
        self.blocks = []  # 2D list: self.blocks[x][y] = block type

        # Block images
        self.dirt = pygame.Surface((self.block_size, self.block_size))
        self.dirt.fill((139, 69, 19))  # brown
        # Placeholder slope textures (visual only)
        self.slope_left = pygame.Surface((self.block_size, self.block_size))
        self.slope_left.fill((120, 100, 80))
        self.slope_right = pygame.Surface((self.block_size, self.block_size))
        self.slope_right.fill((160, 120, 90))
        # Placeholder cave opening
        self.cave = pygame.Surface((self.block_size, self.block_size))
        self.cave.fill((40, 40, 40))

        self.generate()

    def generate(self):
        # Terrain generation parameters
        base_height = 12
        ground_slope = 0.2  # how quickly ground trends up/down
        hill_amplitude = 3
        cave_chance = 0.10  # chance for a cave opening at ground level
        slope_visual_range = 1  # how many blocks to look left/right for slope
        seed = random.randint(0, 10000)

        self.blocks = []
        heights = []
        current_height = base_height
        evaluation_counter = 0
        for x in range(self.width):
            # Every 10 blocks, adjust base height by ±1
            if evaluation_counter >= 10:
                current_height += random.choice([-1, 0, 1])
                current_height = max(3, min(self.height - 3, current_height))  # clamp
                evaluation_counter = 0
            heights.append(current_height)
            evaluation_counter += 1
        # Generate caves at ground level
        cave_openings = set()
        for x in range(self.width):
            if random.random() < cave_chance:
                cave_openings.add(x)
        # Build blocks
        for x in range(self.width):
            col = []
            for y in range(self.height):
                if y < heights[x]:
                    col.append(0)  # air
                elif y == heights[x]:
                    if x in cave_openings:
                        col.append(3)  # cave opening
                    else:
                        # Determine if this block is a visual slope
                        left = heights[x - 1] if x > 0 else heights[x]
                        right = heights[x + 1] if x < self.width - 1 else heights[x]
                        if left < heights[x]:
                            col.append(4)  # left slope (visual only)
                        elif right < heights[x]:
                            col.append(5)  # right slope (visual only)
                        else:
                            col.append(1)  # normal dirt
                else:
                    col.append(1)  # dirt block below ground
            self.blocks.append(col)

    def draw(self, offset=pygame.math.Vector2(0, 0)):
        for x, col in enumerate(self.blocks):
            for y, block_type in enumerate(col):
                block_pos = (x * self.block_size + offset.x, y * self.block_size + offset.y)
                if block_type == 1:
                    self.screen.blit(self.dirt, block_pos)
                elif block_type == 3:
                    self.screen.blit(self.cave, block_pos)
                elif block_type == 4:
                    self.screen.blit(self.slope_left, block_pos)
                elif block_type == 5:
                    self.screen.blit(self.slope_right, block_pos)
                # block_type 0 is air, draw nothing