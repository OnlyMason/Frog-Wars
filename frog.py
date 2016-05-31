import pygame
from hitbox import Hitbox

"""
 Render each frog
 Player 1 is rendered on the bottom
 Player 2 is rendered on top
 Lilypads are rendered underneath each frog
 Attributes:
        hitbox (obj): the hitbox object for the tip of the frog's tongue, which will allow us to check collisions
        player (int): the player (1 or x), which will determine how the frog is created
        stunned (bool): whether or not the frog is currently stunned
        time_of_stun (float): the time that the frog has been stunned, which we need to calculate stun duration
        swirl (obj): a swirl sprite to display a frog's stunned status
        size (int): image size
        x, y (int): position of the frog
        mouth (int, tuple): position of the frog's mouth
        lily (obj): the lilypad sprite, and accompanying attributes to determine how and where it is drawn
"""

class Frog(pygame.sprite.Sprite):
    def __init__(self, player, window_size):
        """
        :param player: Which player the frog is
        :param window_size: the size of the window
        """
        super().__init__()

        self.hitbox = Hitbox()
        self.player = player
        self.stunned = False
        self.time_of_stun = 0
        self.swirl = pygame.image.load("swirl.png").convert_alpha()
        if player == 1:
            self.image = pygame.image.load("frog1.png").convert_alpha()
            self.size = self.image.get_size()
            self.x = window_size[0]/2 - self.size[0]/2
            self.y = window_size[1] - self.size[1]
            self.mouth = (self.x + self.size[0]/2, self.y)
            self.lily = pygame.image.load("lily1.png")
            self.lily_size = self.lily.get_size()
            self.lily_x = window_size[0]/2 - self.size[0]/2 - 15
            self.lily_y = window_size[1] - self.size[1] - 50
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        else:
            self.image = pygame.image.load("frog2.png").convert_alpha()
            self.size = self.image.get_size()
            self.x = window_size[0]/2 - self.size[0]/2
            self.y = 0
            self.mouth = (self.x + self.size[0]/2, self.size[1])
            self.lily = pygame.image.load("lily1.png")
            self.lily = pygame.transform.rotate(self.lily, 180)
            self.lily_size = self.lily.get_size()
            self.lily_x = window_size[0]/2 - self.size[0]/2 - 15
            self.lily_y = -15
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    def draw(self, screen):
        """
        :param screen: the surface object
        :return: void
        """
        screen.blit(self.lily, (self.lily_x, self.lily_y))
        screen.blit(self.image, (self.x, self.y))
        if self.stunned and self.player == 1:
            screen.blit(self.swirl, (self.x + 35, self.y))
        elif self.stunned and self.player == 2:
            screen.blit(self.swirl, (self.x + 35, self.y + 40))


    def fire_tongue(self, screen, power, x, y, fly_sprites, dfly_sprites):
        """
        :param screen: the surface object
        :param power: the power of the tongue shot
        :param x: the x position of the ending position
        :param y: the y position of the ending position
        :param fly_sprites: fly sprite group
        :param dfly_sprites: dragonfly sprite group
        :return: a list of collisions, and a boolean to determine whether or not it was a dragonfly,
                which is prioritized
        This function makes a calculation between starting position and ending positions to determine
        how far the tongue will be launched depending on the power of the charge
        """
        power /= 3.4
        tongue_color = (212, 144, 198)
        if self.player == 1:
            start = (self.x + self.size[0]/2, self.y)
            dist = (power * (start[0] - x), power * (y - start[1]))
            pygame.draw.line(screen, tongue_color, start, ((start[0] - dist[0]), (start[1] + dist[1])), 20)
            self.hitbox.draw(screen, int(start[0] - dist[0]),
                             int(start[1] + dist[1]))
            dfly_hit_list = pygame.sprite.spritecollide(self.hitbox, dfly_sprites, True)
            if len(dfly_hit_list) > 0:
                return dfly_hit_list, True
            else:
                fly_hit_list = pygame.sprite.spritecollide(self.hitbox, fly_sprites, True)
                return fly_hit_list, False

        else:
            start = (self.x + self.size[0]/2, self.size[1])
            dist = (power * (start[0] - x), power * (y - start[1]))
            pygame.draw.line(screen, tongue_color, start, ((start[0] - dist[0]), (start[1] + dist[1])), 20)
            pygame.draw.circle(screen, tongue_color, (int(start[0] - dist[0]), int(start[1] + dist[1])), 30, 0)
            self.hitbox.draw(screen, int(start[0] - dist[0]),
                             int(start[1] + dist[1]))
            dfly_hit_list = pygame.sprite.spritecollide(self.hitbox, dfly_sprites, True)
            if len(dfly_hit_list) > 0:
                return dfly_hit_list, True
            else:
                fly_hit_list = pygame.sprite.spritecollide(self.hitbox, fly_sprites, True)
                return fly_hit_list, False

