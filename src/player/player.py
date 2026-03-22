import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, blocks, pos=(0, 0)):
        super().__init__()

        self.screen = screen
        self.position = pygame.math.Vector2(pos)

        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.touching_ground = False

        self.image = pygame.Surface((32, 64))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)

        self.blocks = blocks
        self.block_size = 32

    def is_solid(self, x, y):
        if 0 <= x < len(self.blocks) and 0 <= y < len(self.blocks[0]):
            return self.blocks[x][y] in [1, 2]
        return False

    def get_nearby_blocks(self):
        blocks = []

        start_x = int(self.rect.left // self.block_size) - 1
        end_x = int(self.rect.right // self.block_size) + 1
        start_y = int(self.rect.top // self.block_size)
        end_y = int(self.rect.bottom // self.block_size)

        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if self.is_solid(x, y):
                    blocks.append(pygame.Rect(
                        x * self.block_size,
                        y * self.block_size,
                        self.block_size,
                        self.block_size
                    ))
        return blocks

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.velocity.x = -self.speed
        elif keys[pygame.K_d]:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0

        if keys[pygame.K_SPACE] and self.touching_ground:
            self.velocity.y = self.jump_power
            self.touching_ground = False

        self.velocity.y += self.gravity

        # horizontal
        self.position.x += self.velocity.x
        self.rect.x = int(self.position.x)
        self.check_collision("x")

        # vertical
        self.position.y += self.velocity.y
        self.rect.y = int(self.position.y)
        self.touching_ground = False
        self.check_collision("y")

        # sync fix
        self.rect.topleft = (int(self.position.x), int(self.position.y))

    def check_collision(self, direction):
        for block in self.get_nearby_blocks():
            if self.rect.colliderect(block):

                if direction == "y":
                    if self.velocity.y > 0:
                        self.rect.bottom = block.top
                        self.position.y = self.rect.bottom - self.rect.height
                        self.velocity.y = 0
                        self.touching_ground = True

                    elif self.velocity.y < 0:
                        self.rect.top = block.bottom
                        self.position.y = self.rect.top
                        self.velocity.y = 0

                elif direction == "x":
                    if self.velocity.x > 0:
                        self.rect.right = block.left
                        self.position.x = self.rect.x

                    elif self.velocity.x < 0:
                        self.rect.left = block.right
                        self.position.x = self.rect.x

    def draw(self, offset):
        draw_x = int(self.rect.x - offset.x)
        draw_y = int(self.rect.y - offset.y)

        self.screen.blit(self.image, (draw_x, draw_y))

        # player box (red)
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (draw_x, draw_y, self.rect.width, self.rect.height), 2)

        # nearby blocks (blue)
        for block in self.get_nearby_blocks():
            pygame.draw.rect(
                self.screen,
                (0, 0, 255),
                (
                    int(block.x - offset.x),
                    int(block.y - offset.y),
                    block.width,
                    block.height
                ),
                1
            )