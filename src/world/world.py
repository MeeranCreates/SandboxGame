import pygame
import random
from noise import pnoise1

class World:
    def __init__(self, screen):
        self.screen = screen
        self.block_size = 32
        self.width = 200
        self.height = 50

        self.blocks = []
        self.biomes = []

        # textures
        self.grass = pygame.image.load("assets/images/grass_flat.png").convert_alpha()
        self.snow = pygame.image.load("assets/images/snow_flat.png").convert_alpha()
        self.sand = pygame.image.load("assets/images/sand_flat.png").convert_alpha()

        self.dirt = pygame.image.load("assets/images/dirt.png").convert_alpha()
        self.sand_fill = pygame.image.load("assets/images/sand.png").convert_alpha()
        self.stone = pygame.image.load("assets/images/stone.png").convert_alpha()

        self.grass_left = pygame.image.load("assets/images/grass_left_slope.png").convert_alpha()
        self.grass_right = pygame.image.load("assets/images/grass_right_slope.png").convert_alpha()
        self.snow_left = pygame.image.load("assets/images/snow_left_slope.png").convert_alpha()
        self.snow_right = pygame.image.load("assets/images/snow_right_slope.png").convert_alpha()
        self.sand_left = pygame.image.load("assets/images/sand_left_slope.png").convert_alpha()
        self.sand_right = pygame.image.load("assets/images/sand_right_slope.png").convert_alpha()

        self.generate()

    def generate(self):
        self.blocks = []
        self.biomes = []
        heights = []

        seed = random.randint(0, 9999)
        scale = 0.01
        amp = 4

        for x in range(self.width):
            if x < self.width * 0.33:
                base = 20
                biome = "snow"
            elif x < self.width * 0.66:
                base = 15
                biome = "forest"
            else:
                base = 10
                biome = "desert"

            self.biomes.append(biome)

            h = int(base + pnoise1(x * scale + seed) * amp)
            heights.append(max(5, min(self.height - 5, h)))

        # smooth
        for i in range(1, len(heights)):
            if heights[i] - heights[i-1] > 1:
                heights[i] = heights[i-1] + 1
            elif heights[i] - heights[i-1] < -1:
                heights[i] = heights[i-1] - 1

        # build
        for x in range(self.width):
            col = []
            for y in range(self.height):

                if y == heights[x] - 1:
                    # slope goes on upper block
                    left = heights[x-1] if x > 0 else heights[x]
                    right = heights[x+1] if x < self.width - 1 else heights[x]

                    if heights[x] - left == 1:
                        col.append(4)  # left slope (visual on top)
                    elif heights[x] - right == 1:
                        col.append(5)  # right slope
                    else:
                        col.append(0)

                elif y < heights[x]:
                    col.append(0)

                elif y == heights[x]:
                    col.append(1)  # normal ground block

                else:
                    if y > heights[x] + 5:
                        col.append(2)
                    else:
                        col.append(1)

            self.blocks.append(col)

    def draw(self, offset):
        for x in range(self.width):
            for y in range(self.height):

                block = self.blocks[x][y]
                if block == 0:
                    continue

                draw_x = int(x * self.block_size - offset.x)
                draw_y = int(y * self.block_size - offset.y)

                biome = self.biomes[x]

                if block == 1:
                    if y == 0 or self.blocks[x][y-1] == 0:
                        if biome == "snow":
                            self.screen.blit(self.snow, (draw_x, draw_y))
                        elif biome == "desert":
                            self.screen.blit(self.sand, (draw_x, draw_y))
                        else:
                            self.screen.blit(self.grass, (draw_x, draw_y))
                    else:
                        if biome == "desert":
                            self.screen.blit(self.sand_fill, (draw_x, draw_y))
                        else:
                            self.screen.blit(self.dirt, (draw_x, draw_y))

                elif block == 2:
                    self.screen.blit(self.stone, (draw_x, draw_y))

                elif block == 4:
                    if biome == "snow":
                        self.screen.blit(self.snow_left, (draw_x, draw_y))
                    elif biome == "desert":
                        self.screen.blit(self.sand_left, (draw_x, draw_y))
                    else:
                        self.screen.blit(self.grass_left, (draw_x, draw_y))

                elif block == 5:
                    if biome == "snow":
                        self.screen.blit(self.snow_right, (draw_x, draw_y))
                    elif biome == "desert":
                        self.screen.blit(self.sand_right, (draw_x, draw_y))
                    else:
                        self.screen.blit(self.grass_right, (draw_x, draw_y))

                # debug world boxes (green)
                if block in [1, 2, 4, 5]:
                    pygame.draw.rect(self.screen, (0, 255, 0),
                                     (draw_x, draw_y, self.block_size, self.block_size), 1)