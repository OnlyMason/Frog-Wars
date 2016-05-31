import pygame

"""
This draws the crosshair for each player and the accompanying charge bar if the player is currently charging a shot
Attributes:
    window_size: the window size as a tuple
    size: size of the image
    player (int): the player that the crosshair belongs to
    charging (boolean): whether or not the player is charging a shot, which will determine if the meter will be drawn
    x,y: the position of the crosshair
"""


class Crosshair:
    def __init__(self, window_size, player):
        """
        :param window_size: the window size as a tuple
        :param player: the player that the crosshair belongs to
        :return: void
        """
        self.window_size = window_size
        self.image = pygame.image.load("crosshair.png").convert_alpha()
        self.size = self.image.get_size()
        self.player = player
        if self.player == 1:
            self.x = window_size[0]/2 - self.size[0]/2
            self.y = window_size[1] - self.size[1] - 150
        else:
            self.x = window_size[0]/2 - self.size[0]/2
            self.y = 150
        self.charging = False

    def draw(self, screen, power):
        """ 
        :param screen: the surface object
        :param power: power charged by player
        :return: void
        Draws the crosshair, and passes power to draw_bar if the player is charging their tongue
        """
        screen.blit(self.image, (self.x, self.y))
        if self.charging:
            if self.player == 1:
                self.draw_bar(screen, power)
            else:
                self.draw_bar(screen, power)

    def draw_bar(self, screen, power):
        """
        :param screen: the surface object
        :param power: power charged by player
        :return: void
        Draws the charge meter if the player is charging
        """
        if self.player == 1:
            if self.x < self.window_size[0] / 2:
                if power >= 50:
                    pygame.draw.rect(screen, (255, 255, 0), [self.x + self.size[0], self.y + 5, power, 25], 0)
                else:
                    pygame.draw.rect(screen, (255, 100, 0), [self.x + self.size[0], self.y + 5, power, 25], 0)
                pygame.draw.rect(screen, (0, 0, 0), [self.x + self.size[0], self.y + 5, 100, 25], 3)
            else:
                if power >= 50:
                    pygame.draw.rect(screen, (255, 255, 0), [self.x - self.size[0] * 2.5, self.y + 5, power, 25], 0)
                else:
                    pygame.draw.rect(screen, (255, 100, 0), [self.x - self.size[0] * 2.5, self.y + 5, power, 25], 0)
                pygame.draw.rect(screen, (0, 0, 0), [self.x - self.size[0] * 2.5, self.y + 5, 100, 25], 3)
        else:
            if self.x < self.window_size[0] / 2:
                if power >= 50:
                    pygame.draw.rect(screen, (255, 255, 0), [self.x + self.size[0], self.y + 5, power, 25], 0)
                else:
                    pygame.draw.rect(screen, (255, 100, 0), [self.x + self.size[0], self.y + 5, power, 25], 0)
                pygame.draw.rect(screen, (0, 0, 0), [self.x + self.size[0], self.y + 5, 100, 25], 3)
            else:
                if power >= 50:
                    pygame.draw.rect(screen, (255, 255, 0), [self.x - self.size[0] * 2.5, self.y + 5, power, 25], 0)
                else:
                    pygame.draw.rect(screen, (255, 100, 0), [self.x - self.size[0] * 2.5, self.y + 5, power, 25], 0)
                pygame.draw.rect(screen, (0, 0, 0), [self.x - self.size[0] * 2.5, self.y + 5, 100, 25], 3)

    def change_x(self, inc):
        self.x += inc

