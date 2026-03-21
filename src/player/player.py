import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen,blocks, pos: tuple = (0, 0),):
        super().__init__()

        # args
        self.screen = screen
        self.position = pygame.math.Vector2(pos)

        # physics
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.touching_ground = False

        # player image
        self.image = pygame.Surface((32, 64))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)

        # collision 
        self.blocks = blocks  # list of [x[y]] for collision detection
        self.block_size = 32
    def is_solid(self, x, y):
        if 0 <= x < len(self.blocks) and 0 <= y < len(self.blocks[0]):
            return self.blocks[x][y] == 1
        return False

    def get_nearby_blocks(self):
        blocks = []

        start_x = int(self.rect.left // self.block_size)
        end_x = int(self.rect.right // self.block_size)
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
        print(self.position)
        keys = pygame.key.get_pressed()

        # horizontal movement
        if keys[pygame.K_a]:
            self.velocity.x = -self.speed
        elif keys[pygame.K_d]:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0

        # jump
        if keys[pygame.K_SPACE] and self.touching_ground:
            self.velocity.y = self.jump_power
            self.touching_ground = False

        # apply gravity
        self.velocity.y += self.gravity

        # --- HORIZONTAL ---
        self.position.x += self.velocity.x
        self.rect.x = int(self.position.x)
        self.check_collision("x")

        # --- VERTICAL ---
        self.position.y += self.velocity.y
        self.rect.y = int(self.position.y)
        self.touching_ground = False
        self.check_collision("y")

    def check_collision(self, direction):
        for block in self.get_nearby_blocks():
            if self.rect.colliderect(block):

                if direction == "y":
                    if self.velocity.y > 0:  # falling
                        self.rect.bottom = block.top
                        self.position.y = self.rect.y
                        self.velocity.y = 0
                        self.touching_ground = True

                    elif self.velocity.y < 0:  # jumping
                        self.rect.top = block.bottom
                        self.position.y = self.rect.y
                        self.velocity.y = 0

                elif direction == "x":
                    if self.velocity.x > 0:  # right
                        self.rect.right = block.left
                        self.position.x = self.rect.x

                    elif self.velocity.x < 0:  # left
                        self.rect.left = block.right
                        self.position.x = self.rect.x

    def draw(self, offset=pygame.math.Vector2(0, 0)):
        self.screen.blit(self.image, (
            int(self.rect.x - offset.x),
            int(self.rect.y - offset.y)
        ))
