import pygame

"""
The tongue hitbox sprite, which will let us check collision
"""

class Hitbox(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Draws the tongue hitbox
        self.hitbox = pygame.Surface([60, 60])
        self.hitbox.fill(pygame.Color(255, 255, 255))
        self.hitbox.set_colorkey(pygame.Color(255, 255, 255))
        self.size = self.hitbox.get_size()
        pygame.draw.circle(self.hitbox, (212, 144, 198), [30, 30], 30)
        self.rect = self.hitbox.get_rect()

    def draw(self, screen, x, y):
        self.rect.x = x - self.size[0]/2
        self.rect.y = y - self.size[1]/2
        screen.blit(self.hitbox, (x - self.size[0]/2, y - self.size[1]/2))
