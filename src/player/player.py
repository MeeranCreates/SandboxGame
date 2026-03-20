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

        # collision object
        #self.blocks = blocks



    def update(self):
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

        # apply movement
        self.position += self.velocity

        # update rect
        self.rect.topleft = (int(self.position.x), int(self.position.y))

        # collision check
        # ----   self.check_collision() ------

    def check_collision(self):
        self.touching_ground = False

        for block_surface, block_pos in self.blocks:
            block_rect = pygame.Rect(block_pos[0], block_pos[1], 32, 32)

            if self.rect.colliderect(block_rect):
                if self.velocity.y > 0:  # falling
                    self.rect.bottom = block_rect.top
                    self.position.y = self.rect.y
                    self.velocity.y = 0
                    self.touching_ground = True

    def draw(self):
        self.screen.blit(self.image, self.rect)
