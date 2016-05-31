"""
Run the main.py file to execute the game
"""

import pygame
import sys
import random
from pygame.locals import *
from frog import Frog
from crosshair import Crosshair
from fly import Fly
from dragonfly import Dragonfly
from fireball import Fireball


def menu(screen, window_size):
    """
    :param screen: the surface object
    :param window_size: the window size as a tuple
    :return: void
    """
    background = pygame.image.load('background.jpg')
    black = (0, 0, 0)
    title_font = pygame.font.SysFont('jokerman', 50)
    options_font = pygame.font.SysFont('terminal', 20)
    pygame.mixer.music.load('menu.ogg')
    pygame.mixer.music.play(-1)
    title_height = 0
    while True:  # <--- main game loop
        SCREEN.blit(background, (0, 0))
        p1_help_text = 'P1: Left - Aim Left, Right - Aim Right, ' \
                       'Down - Charge Shot, Up - Shoot Fireball'
        p2_help_text = 'P2: A - Aim Left, D - Aim Right, S - Charge Shot, W - Shoot Fireball'
        SCREEN.blit(title_font.render('FROG WARS', True, black), (window_size[0]/4, title_height))
        if title_height >= window_size[1]/4:
            SCREEN.blit(options_font.render('Press ENTER to start game', True, black),
                        (window_size[0]/4, window_size[1]/4 + 65))
            SCREEN.blit(options_font.render(p1_help_text, True, black), (15, 25))
            SCREEN.blit(options_font.render(p2_help_text, True, black), (15, 50))
        if not title_height >= (window_size[1]/4):
            title_height += 0.75

        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def victory(screen, window_size, winner):
    """
    :param screen: the surface object
    :param window_size: the window size as a tuple
    :param winner: the winner of the game, which will change the display text
    :return: void
    """
    background = pygame.image.load('victory.jpg')
    black = (0, 0, 0)
    victory_font = pygame.font.SysFont('jokerman', 50)
    options_font = pygame.font.SysFont('berlinsansfb', 20)

    pygame.mixer.music.load('victory.ogg')
    pygame.mixer.music.play()

    while True:  # <--- main game loop
        SCREEN.blit(background, (0, 0))
        if winner == 3:
            SCREEN.blit(victory_font.render('TIE GAME!', True, black),
                (window_size[0]/4, window_size[1]/4 - 50))
        else:
            SCREEN.blit(victory_font.render('Player ' + str(winner) + ' has won!', True, black),
                (window_size[0]/4, window_size[1]/4 - 50))
        SCREEN.blit(options_font.render('Press ENTER to play again', True, black),
                    (window_size[0]/4 + 75, window_size[1]/4 + 30))

        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_1:
                    choice = 1
                    return choice
                if event.key == K_2:
                    choice = 2
                    return choice
                if event.key == K_RETURN:
                    return
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def draw_line(screen, mouth_pos, crosshair_pos):
    """
    :param screen: the surface object
    :param mouth_pos: the position of the frog's mouth as a tuple
    :param crosshair: the position of the crosshair as a tuple
    This will draw a line connecting the frog's mouth to the crosshair
    """
    dist = (mouth_pos[0] - crosshair_pos[0], mouth_pos[1] - crosshair_pos[1])
    pygame.draw.line(screen, (0, 0, 0), mouth_pos, ((mouth_pos[0] - dist[0]), (mouth_pos[1] - dist[1])), 2)


def main(screen, window_size):
    """
    :param screen: the surface object
    :param window_size: the window size as a tuple
    :return: void
    This is the main game loop
    """
    FPS = 30
    FPS_CLOCK = pygame.time.Clock()

    pygame.mixer.music.load('battle.ogg')
    pygame.mixer.music.play(-1)
    whip = pygame.mixer.Sound('whip.ogg')
    boom = pygame.mixer.Sound('boom.ogg')
    pond = pygame.image.load('pond.png')

    # Draw Frogs
    frog1 = Frog(1, window_size)
    crosshair1 = Crosshair(window_size, 1)

    frog2 = Frog(2, window_size)
    crosshair2 = Crosshair(window_size, 2)

    # Fly Setup
    fly_sprites = pygame.sprite.Group()
    FLY_SPAWN = pygame.USEREVENT + 1
    pygame.time.set_timer(FLY_SPAWN, 1000)

    # Dragonfly Setup
    dfly_sprites = pygame.sprite.Group()
    DFLY_SPAWN = pygame.USEREVENT + 2
    pygame.time.set_timer(DFLY_SPAWN, 5000)

    fireballs1 = pygame.sprite.Group()
    fireballs2 = pygame.sprite.Group()

    # Text
    start_ticks = pygame.time.get_ticks()
    timer = 61
    timer_font = pygame.font.SysFont('berlinsansfb', 50)
    score_font = pygame.font.SysFont('berlinsansfb', 30)

    p1_move_right = False
    p1_move_left = False
    p1_charge = 0
    p1_score = 0
    p1_fire = 0

    p2_move_right = False
    p2_move_left = False
    p2_charge = 0
    p2_score = 0
    p2_fire = 0
    while True:  # <--- main game loop

        seconds = (pygame.time.get_ticks() - start_ticks)/1000

        # render objects
        SCREEN.blit(pond, (0, 0))
        frog1.draw(SCREEN)
        frog2.draw(SCREEN)

        if len(dfly_sprites) > 0:
            dfly_sprites.update()
            dfly_sprites.draw(SCREEN)
        if len(fly_sprites) > 0:
            fly_sprites.update()
            fly_sprites.draw(SCREEN)
        if len(fireballs1) > 0:
            fireballs1.update()
            fireballs1.draw(SCREEN)
            frogs_stunned = pygame.sprite.spritecollide(frog2, fireballs1, True)
            if len(frogs_stunned) > 0:
                frog2.stunned = True
                p2_charge = 0
                crosshair2.charging = 0
                frog2.time_of_stun = timer - seconds
        if len(fireballs2) > 0:
            fireballs2.update()
            fireballs2.draw(SCREEN)
            frogs_stunned = pygame.sprite.spritecollide(frog1, fireballs2, True)
            if len(frogs_stunned) > 0:
                frog1.stunned = True
                p1_charge = 0
                crosshair1.charging = 0
                frog1.time_of_stun = timer - seconds

        # draw targeting line and charge meter for frog 1
        draw_line(screen, frog1.mouth, (crosshair1.x + crosshair1.size[0]/2, crosshair1.y + crosshair1.size[1]/2))
        crosshair1.draw(SCREEN, p1_charge * 5)

        # draw targeting line and charge meter for frog 2
        draw_line(screen, frog2.mouth,  (crosshair2.x + crosshair2.size[0]/2, crosshair2.y + crosshair2.size[1]/2))
        crosshair2.draw(SCREEN, p2_charge * 5)

        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()

            # Fly event timer
            if event.type == FLY_SPAWN:
                if len(fly_sprites) < 10:
                    if random.randrange(0, 2) == 0:
                        fly = Fly(0, random.randrange(175, 501), random.randrange(1, 11))
                        fly_sprites.add(fly)
                    else:
                        fly = Fly(700, random.randrange(175, 501), random.randrange(1, 11))
                        fly_sprites.add(fly)

            # Dragonfly event timer
            if event.type == DFLY_SPAWN:
                if len(dfly_sprites) < 1:
                    if random.randrange(0, 2) == 0:
                        dragonfly = Dragonfly(0, random.randrange(175, 450), random.randrange(5, 11), random.randrange(3,11))
                        dfly_sprites.add(dragonfly)
                    else:
                        dragonfly = Dragonfly(700, random.randrange(175, 450), random.randrange(5, 11), random.randrange(3,11))
                        dfly_sprites.add(dragonfly)

            # Input events
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 0
                # Player 1
                if event.key == K_LEFT:
                    p1_move_left = True
                if event.key == K_RIGHT:
                    p1_move_right = True
                if event.key == K_DOWN and not frog1.stunned:
                    crosshair1.charging = True

                # Player 2
                if event.key == K_a:
                    p2_move_left = True
                if event.key == K_d:
                    p2_move_right = True
                if event.key == K_s and not frog2.stunned:
                    crosshair2.charging = True

                # Quit
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == KEYUP:
                # Player 1
                if event.key == K_LEFT:
                    p1_move_left = False
                if event.key == K_RIGHT:
                    p1_move_right = False
                if event.key == K_DOWN and not frog1.stunned:
                    whip.play()
                    crosshair1.charging = False
                    xhair1 = (crosshair1.x + crosshair1.size[0]/2,crosshair1.y + crosshair1.size[1]/2)
                    hit_list, is_dragon = frog1.fire_tongue(SCREEN, p1_charge, xhair1[0], xhair1[1], fly_sprites, dfly_sprites)
                    p1_score += len(hit_list)
                    if len(hit_list) > 0 and p1_charge >= 10:
                        p1_score += 2
                    if is_dragon:
                        p1_fire += 1
                        p1_score += 1
                    p1_charge = 0
                if event.key == K_UP and not frog1.stunned:
                    if p1_fire > 0:
                        boom.play()
                        fireball = Fireball(1, frog1.x + 50, frog1.y)
                        fireballs1.add(fireball)
                        p1_fire -= 1

                # Player 2
                if event.key == K_a:
                    p2_move_left = False
                if event.key == K_d:
                    p2_move_right = False
                if event.key == K_s and not frog2.stunned:
                    whip.play()
                    crosshair2.charging = False
                    xhair2 = (crosshair2.x + crosshair2.size[0]/2, crosshair2.y + crosshair2.size[1]/2)
                    hit_list, is_dragon = frog2.fire_tongue(SCREEN, p2_charge, xhair2[0], xhair2[1], fly_sprites, dfly_sprites)
                    p2_score += len(hit_list)
                    if len(hit_list) > 0 and p2_charge >= 10:
                        p2_score += 2
                    if is_dragon:
                        p2_fire += 1
                        p2_score += 1
                    p2_charge = 0
                if event.key == K_w and not frog2.stunned:
                    if p2_fire > 0:
                        boom.play()
                        fireball = Fireball(2, frog2.x + 50, frog2.size[1] - 45)
                        fireballs2.add(fireball)
                        p2_fire -= 1

        # Player 1 crosshair events
        if p1_move_left and not crosshair1.x < 0:
            crosshair1.change_x(-15)
        if p1_move_right and not crosshair1.x > window_size[0] - crosshair1.size[0]:
            crosshair1.change_x(15)
        if crosshair1.charging:
            if p1_charge < 20:
                p1_charge += 0.5

        # Player 2 crosshair events
        if p2_move_left and not crosshair2.x < 0:
            crosshair2.change_x(-15)
        if p2_move_right and not crosshair2.x > window_size[0] - crosshair2.size[0]:
            crosshair2.change_x(15)
        if crosshair2.charging:
            if p2_charge < 20:
                p2_charge += 0.5

        # Calculate, render timers
        if timer - seconds > 0:
            timer_text = str(round(timer - seconds, 2))
        else:
            timer_text = 'GAME OVER'
        if frog1.stunned:
            if (timer - seconds) < frog1.time_of_stun - 2:
                frog1.stunned = False
        if frog2.stunned:
            if (timer - seconds) < frog2.time_of_stun - 2:
                frog2.stunned = False
        SCREEN.blit(timer_font.render(timer_text, False, (255, 0, 0)), (25, 25))
        if (timer - seconds) <= 0:
            if p1_score > p2_score:
                return 1
            elif p2_score > p1_score:
                return 2
            elif p1_score == p2_score:
                return 3

        # render HUD info
        p1_score_text = 'Player 1: ' + str(p1_score)
        p1_fire_text = 'Fireballs: ' + str(p1_fire)

        p2_score_text = 'Player 2: ' + str(p2_score)
        p2_fire_text = 'Fireballs: ' + str(p2_fire)

        SCREEN.blit(score_font.render(p1_score_text, True, (0, 0, 0)),
                    (window_size[0]/2 + frog1.size[0]/2 + 25, window_size[1] - 75))
        SCREEN.blit(score_font.render(p1_fire_text, True, (0, 0, 0)),
                    (window_size[0]/2 + frog1.size[0]/2 + 25, window_size[1] - 50))
        SCREEN.blit(score_font.render(p2_score_text, True, (0, 0, 0)),
                    (window_size[0]/2 + frog1.size[0]/2 + 25, 25))
        SCREEN.blit(score_font.render(p2_fire_text, True, (0, 0, 0)),
                    (window_size[0]/2 + frog1.size[0]/2 + 25, 50))

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

if __name__ == '__main__':
    pygame.init()

    # Code to create the initial window
    window_size = (700, 700)
    SCREEN = pygame.display.set_mode(window_size)

    # set the title of the window
    pygame.display.set_caption('Frog Wars')
    while True:
        menu(SCREEN, window_size)
        winner = main(SCREEN, window_size)
        if not winner == 0:
            victory(SCREEN, window_size, winner)

