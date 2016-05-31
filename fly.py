import pygame

"""
The fly sprite
Attributes:
    Attributes:
    window_size: the window size as a tuple
    size: size of the image
    x,y: the position of the fly
    vx: the speed of the fly
"""


class Fly(pygame.sprite.Sprite):
    def __init__(self, x, y, vx):
        """
        :param x,y: the position of the fly
        :param vx: the speed of the fly
        :return: void
        """
        super().__init__()
        self.image = pygame.image.load("fly.png").convert_alpha()
        self.size = self.image.get_size()

        # Required for collision detection
        # HINT: You will need this for the lab
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if x == 700:
            self.vx = -vx
        elif x == 0:
            self.vx = vx

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        """
        :return: void
        Draws the fly, kills it if it flies off the screen
        """
        self.rect.x += self.vx
        if self.rect.x > 750 or self.rect.x < -50:
            self.kill()

