import pygame
import math
import random
from noise import pnoise1

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

        # Block images dirt
        self.grass_flat = pygame.image.load("assets/images/grass_flat.png").convert_alpha()
        self.grass = self.grass_flat
        self.dirt = pygame.image.load("assets/images/dirt.png").convert_alpha()
        # Placeholder slope textures (visual only)
        self.grass_left_slope = pygame.image.load("assets/images/grass_left_slope.png").convert_alpha()
        self.grass_right_slope = pygame.image.load("assets/images/grass_right_slope.png").convert_alpha()
        # Placeholder cave opening
        self.cave = pygame.Surface((self.block_size, self.block_size))
        self.cave.fill((40, 40, 40))
        

        self.generate()

    def generate(self):
        # Terrain generation parameters
        base_height = 12
        ground_slope = 0.2  # how quickly ground trends up/down
        hill_amplitude = 3
        cave_chance = 0
        slope_visual_range = 1  # how many blocks to look left/right for slope
        seed = random.randint(0, 10000)

        self.blocks = []
        heights = []
        current_height = base_height
        evaluation_counter = 0

        # --- BUILD HEIGHT MAP WITH PERLIN NOISE + BIOMES ---
        scale = 0.01  # much smoother terrain
        amplitude = 4

        for x in range(self.width):
            # base biome height
            if x < self.width * 0.33:
                base = 20  # snow higher
            elif x < self.width * 0.66:
                base = 15  # forest mid
            else:
                base = 10  # desert low

            # perlin noise gives smooth variation (-1 to 1)
            noise_val = pnoise1(x * scale + seed)

            height = int(base + noise_val * amplitude)
            height = max(5, min(self.height - 5, height))

            heights.append(height)

        # --- SMOOTH HEIGHT DIFFERENCE (max step = 1) ---
        for i in range(1, len(heights)):
            if heights[i] - heights[i-1] > 1:
                heights[i] = heights[i-1] + 1
            elif heights[i] - heights[i-1] < -1:
                heights[i] = heights[i-1] - 1

        # --- EXTRA SMOOTHING (moving average) ---
        smoothed = heights[:]
        for i in range(2, len(heights) - 2):
            smoothed[i] = int((heights[i-2] + heights[i-1] + heights[i] + heights[i+1] + heights[i+2]) / 5)
        heights = smoothed

        # Build blocks
        for x in range(self.width):
            col = []
            for y in range(self.height):
                if y < heights[x]:
                    # improved slope generation: slopes for multi-block height differences
                    left = heights[x - 1] if x > 0 else heights[x]
                    right = heights[x + 1] if x < self.width - 1 else heights[x]

                    diff_left = heights[x] - left
                    diff_right = heights[x] - right

                    # single block slope only (clean + stable)
                    if diff_left == 1 and y == heights[x] - 1:
                        col.append(4)
                    elif diff_right == 1 and y == heights[x] - 1:
                        col.append(5)
                    else:
                        col.append(0)  # air
                elif y == heights[x]:
                    col.append(1)  # always normal ground block
                else:
                    col.append(1)  # dirt block below ground
            self.blocks.append(col)

    def draw(self, offset=pygame.math.Vector2(0, 0)):
        for x, col in enumerate(self.blocks):
            for y, block_type in enumerate(col):
                block_pos = (x * self.block_size + offset.x, y * self.block_size + offset.y)
                if block_type == 1:
                    # check if this is surface block
                    if y == 0 or self.blocks[x][y-1] == 0:
                        self.screen.blit(self.grass, block_pos)
                    else:
                        self.screen.blit(self.dirt, block_pos)
                elif block_type == 4:
                    self.screen.blit(self.grass_left_slope, block_pos)
                elif block_type == 5:
                    self.screen.blit(self.grass_right_slope, block_pos)
                # block_type 0 is air, draw nothing