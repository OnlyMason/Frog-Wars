import pygame

"""
The fireball sprite that will be drawn when the player shoots
Attributes:
    x, y (int): the position of the fireball
    player (int): the player that shot the fireball
"""

class Fireball(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        """
        :param player: the player that shot the fireball
        :param x: the x position of the fireball
        :param y: the y position of the fireball
        :return: void
        """
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.image.load("fireball.png")
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player

        if self.player == 1:
            self.image = pygame.transform.rotate(self.image, -90)
            self.vy = -25
        else:
            self.image = pygame.transform.rotate(self.image, 90)
            self.vy = 25

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.rect.y += self.vy

