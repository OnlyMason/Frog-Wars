import pygame

"""
The dragonfly sprite
Attributes:
    Attributes:
    window_size: the window size as a tuple
    size: size of the image
    x,y: the position of the dragonfly
    vx: the horizontal speed of the dragonfly
    vy: the vertical speed of the dragonfly
"""

# Derive your class from the Sprite super class


class Dragonfly(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy):
        """
        :param x,y: the position of the dragonfly
        :param vx: the speed of the dragonfly
        :return: void
        """
        super().__init__();
        self.image = pygame.image.load("dragonfly.png").convert_alpha()
        self.size = self.image.get_size()

        # Required for collision detection
        # HINT: You will need this for the lab
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        if x == 700:
            self.vx = -vx
            self.image = pygame.transform.rotate(self.image, 90)
        elif x == 0:
            self.vx = vx
            self.image = pygame.transform.rotate(self.image, -90)
        self.vy = vy

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        t_collide = self.rect.y + self.vy < 175
        b_collide = self.rect.y + self.image.get_height() + self.vy > 525

        # Check collision on top and bottom sides of screen
        if t_collide or b_collide:
            self.vy *= -1

        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.x > 750 or self.rect.x < -50:
            self.kill()

    def check_collide(self, group):
        collided = pygame.sprite.spritecollide(self, group, False)
        if len(collided) > 1:
            self.vx *= -1
            self.vy *= -1
