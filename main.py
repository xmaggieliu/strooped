import pygame
import time
from random import randint
# from queue import Queue
from features import *
from datetime import datetime, timedelta

pygame.font.init()

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


def draw_win(words):
    pygame.draw.rect(WIN, BLACK, BORDER_L)
    pygame.draw.rect(WIN, BLACK, BORDER_R)
    pygame.draw.rect(WIN, BLACK, BORDER_T)
    pygame.draw.rect(WIN, BLACK, BORDER_B)

    for obj in words:
        # draw
        text = font_p.render(obj.word, True, obj.colour)
        text_btn = pygame.Rect(obj.left, obj.top, text.get_width(), text.get_height())
        text_rect = text.get_rect()
        text_rect.center = text_btn.center
        pygame.draw.rect(WIN, WHITE, text_btn)
        WIN.blit(text, text_rect)

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    rand_num = randint(0, 6)
    rand_col = rgb[rand_num]  
    rand_word = letter[rand_num]
    run = True
    in_home = True
    in_man = False
    in_game = False
    curr_words = []

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # if event.type == pygame.MOUSEBUTTONUP:
            #     pos = pygame.mouse.get_pos()

        WIN.fill(WHITE)

        if in_home:

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

            pygame.display.update()
            
            # Check if button is clicked
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if menu_play_btn.collidepoint(mouse):
                    time.sleep(0.2)
                    # TO-DO: Change bg 
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
            draw_win(curr_words)
            now = datetime.now()

            # click, _, _ = pygame.mouse.get_pressed()
            # if click == 1:
            #     mouse = pygame.mouse.get_pos()
            #     if menu_play_btn.collidepoint(mouse):

            # check state of first to see if it should disappear
            # check state of last to see if another should be added 
            if len(curr_words) == 0 or curr_words[-1].birth < now - timedelta(seconds=1):
                
                word = letter[randint(0, N - 1)]
                col = rgb[randint(0, N - 1)]
                
                # print(add.word, add.colour)
                text = font_p.render(word, True, col)
                w = randint(0, WIDTH - text.get_width())
                h = randint(0, HEIGHT - text.get_height())
                curr_words.append(Colword(word, col, now, w, h))
                text_btn = pygame.Rect(w, h, text.get_width(), text.get_height())
                text_rect = text.get_rect()
                text_rect.center = text_btn.center
                pygame.draw.rect(WIN, WHITE, text_btn)
                WIN.blit(text, text_rect)
                pygame.display.update()
            while len(curr_words) > 0 and curr_words[0].birth < now - timedelta(seconds=4):
                curr_words.pop(0)




        elif in_man:
            draw_win()
            # TO-DO

        
      

    pygame.quit()

if __name__ == "__main__":
    main()


"""

add text btn into a list

list for levels and dict for each val in list to speed of words

lowering opacity, moving
using keys as remote than mouse??? idk whatz the point of th sy tho

global val
- vel of words
"""
