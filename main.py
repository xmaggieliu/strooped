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
from datetime import datetime, timedelta
from math import sin, cos, pi

from pygame.font import Font

pygame.font.init()
pygame.init()


""" Game constants"""

FPS = 60
DYING = 30
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


""" HEART IMG """

# Heart dimensions
HEART_D = 30

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
GRAY = (211, 211, 211)
GOLD = (175, 130, 30)


levels = ((1, 2), (1, 1.5), (3, 1.5), (3, 1), (6, 1), (6, 0.5))

# Tuple of RGB values
rgb = (BLUE, RED, GREEN, PURPLE, ORANGE, CYAN, PINK, GRAY, GOLD)
# Tuple of strings of colours
letter = ("BLUE", "RED", "GREEN", "PURPLE", "ORANGE", "CYAN", "PINK")


""" Fonts """
# intro title bg will be gray
font_h1 = pygame.font.SysFont("ptmono", 60)
font_info = pygame.font.SysFont("andalemono", 28)
font_mini = pygame.font.SysFont("ptmono", 18)
font_p = pygame.font.SysFont("sfnsmono", 36)
font_man = pygame.font.SysFont("worksans", 20)


""" Data Struct """
class Colword:
    def __init__(self, word, colour, birth, left, top, dir):
        # (str) Colour word 
        self.word = word
        # RGB code
        self.colour = colour
        # Time of birth
        self.birth = birth
        # Left pos
        self.left = left
        # Top pos
        self.top = top
        # Direction of motion in degrees
        self.dir = dir



# FUNCTIONS -----------------------------------------------------------------------------+

def get_rad(x, y):
    """ 
    Get direction of travel in radians
    :param x: (int) current x position; horizontal position; how right it is on the screen
    :param y: (int) current y position; vertical position; how down it is on the screen
    :return: (float) direction of travel in radian
    """

    if y < HEIGHT / 2:
        # If coord in first quadrant
        if x > WIDTH / 2:
            return uniform(pi / 2, pi)
        # => coord in second quad
        return uniform(0, pi / 2)

    # => coord is Q3 or Q4
    # If Q3
    if x < WIDTH / 2:
        return uniform(3 * pi / 2, 2 * pi)
    # Then Q4
    return uniform(pi, 3 * pi / 2)



def out_of_bounds(left, top, w, h):
    """
    If text touched the boundary
    :param left: (int) coord of the left of text
    :param top: (int) coord of the top of text
    :param w: (int) width of text
    :pram h: (int) height of text
    """
    if left <= BORD_WIDTH or top <= BORD_WIDTH + HEART_D or left + w >= WIDTH - BORD_WIDTH or top + h >= HEIGHT - BORD_WIDTH:
        return True
    return False



def in_bound(x, y, left, top, w, h):
    """
    If mouse click is on the text
    :param x: (int) x coord of mouse
    :param y: (int) y xoord of mouse
    :param left: (int) left coord of text
    :param top: (int) top coord of text
    :param w: (int) width of text
    :param h: (int) height of text
    :return: (bool) whether the mouse clicked inside the text's boundary 
    """
    if left <= x <= left + w and top <= y <= top + h:
        return True
    return False



def draw_home(rand_col):
    """ Draw intro/title page """
    n = len(letter) - 1
    w, h = 0, 0
    while h < HEIGHT:
        while w < WIDTH:
            bg = font_p.render(letter[randint(0, n)], True, GRAY)
            WIN.blit(bg, (w, h))
            w += bg.get_width()
        h += bg.get_height()
        w = 0

    # Draw background box
    pygame.draw.rect(WIN, WHITE, pygame.Rect(WIDTH // 5, HEIGHT//3 - 60, WIDTH - 2 * (WIDTH // 5), HEIGHT - 2 * (HEIGHT//3 - 70)), 200, 50)

    # Draw title
    title = font_h1.render("STROOPED!", True, rand_col, WHITE)
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3 - title.get_height() // 2))
    
    # Draw extra text
    mini = font_mini.render("How well can you distinguish your colours?", True, rand_col, WHITE)
    WIN.blit(mini, (WIDTH // 2 - mini.get_width() // 2, HEIGHT * 3 // 4))
 


def draw_game(words, r, col, lives, clock, clicked, x, y):
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
    lost = 0
    captured = False

    for i in range(len(words)):
        # draw
        obj = words[i]
        text = font_p.render(obj.word, True, obj.colour)
        WIN.blit(text, (obj.left, obj.top))
        words[i].left += int(cos(words[i].dir) * r)
        words[i].top += int(sin(words[i].dir) * r)
        out = out_of_bounds(words[i].left, words[i].top, text.get_width(), text.get_height())
        captured = captured or (clicked and in_bound(x, y, words[i].left, words[i].top, text.get_width(), text.get_height()) and words[i].colour == col)
        if captured or out:
            to_del.append(i)
        if out and words[i].colour == col:
            to_del.append(i)
            lost += 1

    for i in to_del[::-1]:
        words.pop(i)
    
    w = WIDTH - 60
    # Draw red hearts
    for i in range(lives):
        WIN.blit(LIFE, (w, 20))
        w -= 50
    # Draw lost hearts
    for i in range(3 - lives):
        WIN.blit(DEAD, (w, 20))
        w -= 50
    # Move blit cursor back to most left red heart
    w += 50 * (3 - lives + 1)
    pygame.display.update()
    # Transition red to lost hearts
    for i in range(lost):
        # Enlarge red heart
        for j in range(10):
            clock.tick(DYING)
            WIN.blit(pygame.transform.scale(LIFE_IMG, (HEART_D + j, HEART_D + j)), (int(w - j/2), int(20 - j/2)))
            pygame.display.update()
        # Change colour and reduce size
        for j in range(10, 0, -1):
            clock.tick(DYING)
            pygame.draw.rect(WIN, WHITE, pygame.Rect(w - 5, 15, 40, 40))
            WIN.blit(pygame.transform.scale(DEAD_IMG, (HEART_D + j, HEART_D + j)), (int(w - j/2), int(20 - j/2)))
            pygame.display.update()
        w += 50
        
    return lives - lost, captured


def draw_man():
    man = """
After clicking `Play` in the home page, the window 
will display the first colour for the user to click for. 
Clicking the right coloured words will increase the 
`Captures` score and missing the right coloured words 
will result in a loss of life, indicated by a quick pause 
in the game in which a red heart pops into a gray one. A word 
will be considered to be missed when it hits one of the borders 
of the game. 

After every 5 captures, there will be a level up and a new 
colour to be clicked for. The event of a level up will be also 
be indicated by a quick pause in the game in which the game info 
banner at the top of the window will enlarge in size and change 
into the new colour to be clicked. After the banner returns to 
the normal size, the game resumes and the user must click for 
the new colour. 

There are no penalties for clicking or missing a coloured word 
that is not in focus for the current level. After reaching 30 
captures, the levels are completed and the game runs 
infinitely, while increasing in speed.
"""
    paraSize = (450, 250)
    WIN.fill(WHITE)
    man = man.splitlines()
    h = font_man.get_height()
    offset = (paraSize[1] - len(man) * (h + 1) // 2)
    for i, line in enumerate(man):
        currLine = font_man.render(line, False, BLACK)
        currPos = (paraSize[0] - currLine.get_width() // 2, i * h + offset)
        WIN.blit(currLine, currPos)


def main():
    clock = pygame.time.Clock()
    run = True
    in_home = True
    in_man = False
    in_game = False
    curr_words = []
    # Rate of motion
    r = 1.4

    x, y = 0, 0
    lives = 3
    captures = 0
    # Current level
    l = 0
    col_variety = 1
    rand_num = randint(0, col_variety)
    rand_col = rgb[rand_num] 
    

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

        WIN.fill(WHITE)

        if in_home:
            # Draw home win
            clock.tick(3)
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

            pygame.display.update()
         
            
            # Check if button is clicked
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if menu_play_btn.collidepoint(mouse):
                    # time.sleep(0.2)
                    in_home = False
                    in_game = True
                    WIN.fill(WHITE)
                    play = font_h1.render(f"CLICK FOR {letter[rand_num]}!", True, rand_col)
                    WIN.blit(play, (WIDTH // 2 - play.get_width() // 2, HEIGHT // 2 - play.get_height() // 2))
                    pygame.display.update()
                    time.sleep(0.5)

                elif menu_man_btn.collidepoint(mouse):
                    # time.sleep(0.2)
                    in_home = False
                    in_man = True
                    WIN.fill(WHITE)

        elif in_game:
            col_variety, birth_rate = levels[l]
            r = 1.4 + captures * 0.1
            count_info = font_info.render("LEVEL: " + str(l) + "  CAPTURES: " + str(captures) + "  COLOUR: " + str(letter[rand_num]), True, GOLD, WHITE)
            WIN.blit(count_info, (20, 20))
            # pygame.display.update()
            lives, captured = draw_game(curr_words, r, rand_col, lives, clock, clicked, x, y)
            
            if captured:
                captures += 1
            # If level up!


            
            if l != captures // 5:
                # level cannot surpass 5
                l = min(captures // 5, 5)
                # New colours
                rand_num = randint(0, col_variety)
                rand_col = rgb[rand_num]
                info = "LEVEL: " + str(l) + "  CAPTURES: " + str(captures) + "  COLOUR: " + str(letter[rand_num]) 
                font_weight = 28
                for j in range(3):
                    clock.tick(DYING)
                    count_info = pygame.font.SysFont("andalemono", font_weight + j).render(info, True, rand_col, WHITE)
                    WIN.blit(count_info, (int(20 - j/2), int(20 - j/2)))
                    pygame.display.update()
                # Change colour and reduce size
                for j in range(3, 0, -1):
                    clock.tick(DYING)
                    count_info = pygame.font.SysFont("andalemono", font_weight + j).render(info, True, rand_col, WHITE)
                    WIN.blit(count_info, (int(20 - j/2), int(20 - j/2)))
                    pygame.display.update()

            now = datetime.now()

            # Create new Colword and add btn on the screen
            if len(curr_words) == 0 or curr_words[-1].birth < now - timedelta(seconds=birth_rate):
                
                word = letter[randint(0, col_variety)]
                col = rgb[randint(0, col_variety)]
                
                text = font_p.render(word, True, col)
                w = randint(BORD_WIDTH, WIDTH - text.get_width() - BORD_WIDTH)
                h = randint(BORD_WIDTH + HEART_D, HEIGHT - text.get_height() - BORD_WIDTH)
                curr_words.append(Colword(word, col, now, w, h, get_rad(w, h)))
                WIN.blit(text, (w, h))
                pygame.display.update()
            if lives <= 0 or captures >= 30:
                # PRINT RESULTS
                return 0

        elif in_man:
            draw_man()
            back = font_info.render("[HOME]", True, GOLD, WHITE)
            back_btn = pygame.Rect(5, 20, back.get_width(), back.get_height())
            back_rect = menu_play.get_rect()
            back_rect.center = back_btn.center
            pygame.draw.rect(WIN, WHITE, back_btn)
            WIN.blit(back, back_rect)
            pygame.display.update()

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if back_btn.collidepoint(mouse):
                    # time.sleep(0.2)
                    in_home = True
                    in_man = False
            

        
      

    pygame.quit()

if __name__ == "__main__":
    main()


"""
list for levels and dict for each val in list to speed of words

as leveling up, fewer colours, more words at same time

5 captures for leveling up in total 6 levels for 30 for central lim th
Level 0: red + bleu, 2 sec
Level 1: red + bleu, 1.5 seconds
Level 2: red + blue + green + purple, 1.5 seconds
Level 3: red + blue + green + purple 1 second
Level 4: orange + cyan + pink
Level 5: 0.5 seconds

"""

