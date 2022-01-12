# PROGRAM DESCRIPTIONS =========================================================>

# Name: Maggie Liu
# Date: Friday, 21 January 2022 
# Course: ICS3U
# Title: Strooped!
# Description: Simulating the Stroop Effect through a game to discern colours of words rather than the word of the colour

# ==============================================================================>


""" Imports """
import pygame
import os
import time
from random import randint, uniform
from utils import *
from datetime import datetime, timedelta
from math import sin, cos, pi

pygame.font.init()


""" Game constants"""

FPS = 60
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Strooped!")


""" Border constants """

BORD_WIDTH = 10
# left
BORDER_L = pygame.Rect(0, 0, BORD_WIDTH, HEIGHT)
# right
BORDER_R = pygame.Rect(WIDTH - BORD_WIDTH, 0, BORD_WIDTH, HEIGHT)
# top
BORDER_T = pygame.Rect(0, 0, WIDTH, BORD_WIDTH)
# bottom
BORDER_B = pygame.Rect(0, HEIGHT - BORD_WIDTH, WIDTH, BORD_WIDTH)


""" RGB Colour Code Constants """

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BLUE = (0, 64, 255)
RED = (200, 30, 40)
GREEN = (0, 150, 30)
PURPLE = (150, 0, 205)
ORANGE = (255, 92, 0)
CYAN = (0, 180, 171)
PINK = (220, 40, 140)
GRAY = (72, 72, 72)
GOLD = (175, 130, 30)

# Colour word to rgb code dictionary
colour_rgb = {"BLUE": BLUE, "RED": RED, "GREEN": GREEN, "PURPLE": PURPLE, "ORANGE": ORANGE, "CYAN": CYAN, "PINK": PINK, "GRAY": GRAY, "GOLD": GOLD}
# Tuple of RGB values
rgb = tuple(colour_rgb.values())
# Tuple of strings of colours
letter = tuple(colour_rgb.keys())
# Num of colours
N = len(letter)


""" Fonts """
# intro title bg will be gray
font_h1 = pygame.font.SysFont("ptmono", 60)
font_info = pygame.font.SysFont("andalemono", 32)
font_mini = pygame.font.SysFont("ptmono", 18)

font_p = pygame.font.SysFont("sfnsmono", 36)


""" HEART IMG """
# Heart dimensions
HEART_D = 10
# Red heart 
LIFE_IMG = pygame.image.load(
    os.path.join('Assets', 'red.png')
)
LIFE = pygame.transform.scale(
    LIFE_IMG, (HEART_D, HEART_D)
)
# Grey heart
DEAD_IMG = pygame.image.load(
    os.path.join('Assets', 'grey.png')
)
DEAD = pygame.transform.scale(
    DEAD_IMG, (HEART_D, HEART_D)
)



# FUNCTIONS -----------------------------------------------------------------------------+

def out_of_bounds(left, top, w, h):
    if left <= BORD_WIDTH or top <= BORD_WIDTH or left + w >= WIDTH - BORD_WIDTH or top + h >= HEIGHT - BORD_WIDTH:
        return True
    return False


def in_bound(x, y, left, top, w, h):
    if left <= x <= left + w and top <= y <= top + h:
        return True
    return False


def draw_win(words, r, col, lives, clicked, x, y):
    """
    Draw game window
    :param words: (list) Colword objects
    :param r: (int) 
    """
    pygame.draw.rect(WIN, BLACK, BORDER_L)
    pygame.draw.rect(WIN, BLACK, BORDER_R)
    pygame.draw.rect(WIN, BLACK, BORDER_T)
    pygame.draw.rect(WIN, BLACK, BORDER_B)

    to_del = []

    for i in range(len(words)):
        # draw
        obj = words[i]
        text = font_p.render(obj.word, True, obj.colour)
        text_btn = pygame.Rect(obj.left, obj.top, text.get_width(), text.get_height())
        text_rect = text.get_rect()
        text_rect.center = text_btn.center
        pygame.draw.rect(WIN, WHITE, text_btn)
        WIN.blit(text, text_rect)
        words[i].left += int(cos(words[i].dir) * r)
        words[i].top += int(sin(words[i].dir) * r)
        out = out_of_bounds(words[i].left, words[i].top, text.get_width(), text.get_height())
        captured = clicked and in_bound(x, y, words[i].left, words[i].top, text.get_width(), text.get_height())
        if out or (captured and words[i].colour == col):
            to_del.append(i)
        if out and words[i].colour == col:
            lives -= 1

    for i in to_del[::-1]:
        words.pop(i)
    # DRAW LIVES
    pygame.display.update()
    

def draw_home(rand_col):
    """ Draw intro/title page """

    # Draw banner of colour boxes
    for i in range(len(rgb)):
        pygame.draw.rect(WIN, rgb[i], pygame.Rect(111 + i * 80, 30, 30, 30))

    # Draw title
    title = font_h1.render("STROOPED!", True, rand_col)
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3 - title.get_height() // 2))
    
    # Draw extra text
    mini = font_mini.render("How well can you distinguish your colours?", True, rand_col)
    WIN.blit(mini, (WIDTH // 2 - mini.get_width() // 2, HEIGHT * 3 // 4))
          
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    rand_num = randint(0, 6)
    # ^ randnum (randint(0, SOME VAR that might changes every round))
    rand_col = rgb[rand_num]  
    rand_word = letter[rand_num]
    run = True
    in_home = True
    in_man = False
    in_game = False
    curr_words = []
    # Rate of motion
    r = 3
    x, y = 0, 0
    lives = 3

    while run:
        clock.tick(FPS)
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            x, y, = 0, 0
            if in_game and event.type == pygame.MOUSEBUTTONUP:
                clicked = True
                x, y = pygame.mouse.get_pos()
                print(x, y)
            # elif in_home and event.type == pygame.MOUSEBUTTONUP

        WIN.fill(WHITE)

        if in_home:
            # Draw home win
            draw_home(rand_col)

            # Draw menu buttons
            menu_play = font_info.render("PLAY", True, GOLD)
            menu_play_btn = pygame.Rect((WIDTH//2 - menu_play.get_width() // 2, HEIGHT//2 - 25, menu_play.get_width(), menu_play.get_height()))
            menu_play_rect = menu_play.get_rect()
            menu_play_rect.center = menu_play_btn.center
            pygame.draw.rect(WIN, WHITE, menu_play_btn)
            WIN.blit(menu_play, menu_play_rect)

            menu_man = font_info.render("MANUAL", True, GOLD)
            menu_man_btn = pygame.Rect((WIDTH//2 - menu_man.get_width() // 2, HEIGHT//2 + 25, menu_man.get_width(), menu_man.get_height()))
            menu_man_rect = menu_man.get_rect()
            menu_man_rect.center = menu_man_btn.center
            pygame.draw.rect(WIN, WHITE, menu_man_btn)
            WIN.blit(menu_man, menu_man_rect)            
            
            # Check if button is clicked
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if menu_play_btn.collidepoint(mouse):
                    time.sleep(0.2)
                    in_home = False
                    in_game = True
                    WIN.fill(WHITE)
                    play = font_h1.render(f"CLICK FOR {rand_word}!", True, rand_col)
                    WIN.blit(play, (WIDTH // 2 - play.get_width() // 2, HEIGHT // 2 - play.get_height() // 2))
                    pygame.display.update()
                    time.sleep(3)

                elif menu_man_btn.collidepoint(mouse):
                    time.sleep(0.2)
                    in_home = False
                    in_man = True


        elif in_game:
            draw_win(curr_words, r, rand_col, lives, clicked, x, y)
            now = datetime.now()

            # Create new Colword and add btn on the screen
            if len(curr_words) == 0 or curr_words[-1].birth < now - timedelta(seconds=1):
                
                word = letter[randint(0, N - 1)]
                col = rgb[randint(0, N - 1)]
                
                text = font_p.render(word, True, col)
                w = randint(0, WIDTH - text.get_width())
                h = randint(0, HEIGHT - text.get_height())
                curr_words.append(Colword(word, col, now, w, h, uniform(0, 2 * pi)))
                text_btn = pygame.Rect(w, h, text.get_width(), text.get_height())
                text_rect = text.get_rect()
                text_rect.center = text_btn.center
                pygame.draw.rect(WIN, WHITE, text_btn)
                WIN.blit(text, text_rect)
                pygame.display.update()
            # if lives <= 0:
            #     game_over()

        elif in_man:
            draw_win()
            # TO-DO

        
      

    pygame.quit()

if __name__ == "__main__":
    main()


"""

add text btn into a list

list for levels and dict for each val in list to speed of words

as leveling up, fewer colours, more words at same time
"""
