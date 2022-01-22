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
from random import randint, uniform, shuffle
from datetime import datetime, timedelta
from math import sin, cos, pi

pygame.init()



""" Game constants"""

# Normal FPS
FPS = 60

# Slower FPS
DELAYED = 30


WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Strooped!")



""" Border constants """

BORD_WIDTH = 10

# Left
BORDER_L = pygame.Rect(0, 0, BORD_WIDTH, HEIGHT)

# Right
BORDER_R = pygame.Rect(WIDTH - BORD_WIDTH, 0, BORD_WIDTH, HEIGHT)

# Top
BORDER_T = pygame.Rect(0, 0, WIDTH, BORD_WIDTH)

# Bottom
BORDER_B = pygame.Rect(0, HEIGHT - BORD_WIDTH, WIDTH, BORD_WIDTH)



""" HEART IMAGES """

# Heart dimensions
HEART_D = 30


# Load red heart image 
LIFE_IMG = pygame.image.load(os.path.join('Assets', 'red.png'))

# Resize red heart image
LIFE = pygame.transform.scale(LIFE_IMG, (HEART_D, HEART_D))


# Load grey heart image
DEAD_IMG = pygame.image.load(os.path.join('Assets', 'grey.png'))

# Resize grey heart image
DEAD = pygame.transform.scale(DEAD_IMG, (HEART_D, HEART_D))



""" RGB Colour Code Constants """

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GRAY = (211, 211, 211)
GOLD = (175, 130, 30)
BROWN = (150, 75, 0)

BLUE = (0, 64, 255)
RED = (200, 30, 40)
GREEN = (0, 150, 30)
PURPLE = (150, 0, 205)
ORANGE = (255, 92, 0)
CYAN = (0, 180, 171)
PINK = (255, 105, 180)


"""
Level #     # of colours    # of seconds before new word appears  
Level 0:    2 colours,      2 sec  
Level 1:    2 colours,      1.5 sec
Level 2:    4 colours,      1.5 sec
Level 3:    4 colours,      1 sec
Level 4:    7 colours,      1 sec
Level 5:    7 colours,      0.5 sec
Level --    ^               ^
"""

levels = ((1, 2), (1, 1.5), (3, 1.5), (3, 1), (6, 1), (6, 0.5))


# Word to rgb code pairs 
colour_rgb = {"BLUE": BLUE, "RED": RED, "GREEN": GREEN, "PURPLE": PURPLE, "ORANGE": ORANGE, "CYAN": CYAN, "PINK": PINK}


# List of words
keys = list(colour_rgb.keys())

# Reorder list
shuffle(keys)

# Remake dictionary
shuffled_rgb = {key: colour_rgb[key] for key in keys}


# Make tuple of colours in words
letter = tuple(keys)

# Make tuple of colours in rgb
rgb = tuple(shuffled_rgb.values())



""" Fonts """

# Game title font
font_title = pygame.font.SysFont("ptmono", 60)

# Game menu options & game banner stats font
font_info = pygame.font.SysFont("andalemono", 28)

# Game results font
font_res = pygame.font.SysFont("andalemono", 18)

# More info font (small-sized)
font_mini = pygame.font.SysFont("ptmono", 18)

# Game colour words font
font_game = pygame.font.SysFont("sfnsmono", 36)

# Game manual font
font_man = pygame.font.SysFont("futura", 17)



""" Data Struct """

class Colword:

    def __init__(self, word, colour, birth, left, top, dir):

        # (str) Colour word 
        self.word = word

        # (tuple) RGB value
        self.colour = colour

        # (datetime) Time of birth
        self.birth = birth

        # (int) Left position
        self.left = left

        # (int) Top position
        self.top = top

        # (float) Direction of motion in radians
        self.dir = dir



# FUNCTIONS -----------------------------------------------------------------------------+

def get_rad(x, y):

    """ 
    Get random direction of travel in radians based on current coordinate to ensure Colword travels AWAY from its closest borders
    :param x: (int) current x position; horizontal position; how right it is on the screen
    :param y: (int) current y position; vertical position; how down it is on the screen
    :return: (float) random direction of travel in radians
    """

    # If coordinate is above the horizontal
    if y < HEIGHT / 2:

        # If coordinate is right of the vertical
        if x > WIDTH / 2:

            # Q1 (top-right quadrant) => let the range of direction be left to down
            return uniform(pi, 3 * pi / 2)    

        # Q2 (top-left quadrant) => let the range of direction be down to right
        return uniform(3 * pi / 2, 2 * pi)

    # If coordinate is left of the vertical (has been established that it is not above the horizontal)
    if x < WIDTH / 2:

        # Q3 (bottom-left) => let the range of dir. be right to up
        return uniform(0, pi / 2)

    # Q4 (bottom-right) => let the range of dir. be up to left
    return uniform(pi / 2, pi)



def out_of_bounds(left, top, w, h):

    """
    If text touched the game boundaries
    :param left: (int) coordinate of the left of text
    :param top: (int) coordinate of the top of text
    :param w: (int) width of text
    :param h: (int) height of text
    :return: (bool) True for out of bounds, False for in bounds
    """

    if left <= BORD_WIDTH or top <= BORD_WIDTH + HEART_D or left + w >= WIDTH - BORD_WIDTH or top + h >= HEIGHT - BORD_WIDTH:
        return True
    return False



def in_bound(x, y, left, top, w, h):

    """
    If mouse is within the boundaries of a text/obj
    :param x: (int) x coord of mouse
    :param y: (int) y xoord of mouse
    :param left: (int) left coordinate of text
    :param top: (int) top coordinate of text
    :param w: (int) width of text
    :param h: (int) height of text
    :return: (bool) whether the mouse is within the boundaries of a text/obj
    """

    if left <= x <= left + w and top <= y <= top + h:
        return True
    return False


def draw_backboard():

    """ Draw white board as a background for text & buttons """

    # Draw background box with rounded corners
    pygame.draw.rect(WIN, WHITE, pygame.Rect(WIDTH // 5, HEIGHT//3 - 60, WIDTH - 2 * (WIDTH // 5), HEIGHT - 2 * (HEIGHT//3 - 70)), 200, 50)
    
    # Draw light shadowy borders to the box
    pygame.draw.rect(WIN, (245, 245, 245), pygame.Rect(WIDTH // 5, HEIGHT//3 - 60, WIDTH - 2 * (WIDTH // 5), HEIGHT - 2 * (HEIGHT//3 - 70)), 10, 50)




def draw_home(rand_col):

    """ 
    Draw intro/title page 
    :param rand_col: (RGB tuple) random colour
    """

    WIN.fill(WHITE)


    # Max index in the letter tuple
    n = len(letter) - 1

    # Initialize left and top positions 
    w, h = 0, 0

    while h < HEIGHT:
        while w < WIDTH:

            # Add a colour word in the background
            bg = font_game.render(letter[randint(0, n)], True, GRAY)
            WIN.blit(bg, (w, h))

            # Increment left position
            w += bg.get_width() + 4

        # Increment top position (as h increases, the position becomes more down as pygame's (0,0) is top-left corner)
        h += bg.get_height()

        # Reinitialize w to the very left of the screen
        w = 0

    draw_backboard()

    # Draw title name 
    title = font_title.render("STROOPED!", True, rand_col, WHITE)
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3 - title.get_height() // 2))
    
    # Draw extra text
    mini = font_mini.render("How well can you distinguish your colours?", True, rand_col, WHITE)
    WIN.blit(mini, (WIDTH // 2 - mini.get_width() // 2, HEIGHT * 3 // 4 - mini.get_height()))



def draw_game(words, r, n, lives, clock, clicked, x, y, congruent, incongruent):

    """
    Draw game window
    :param words: (list) Colword objects
    :param r: (int) rate of motion
    :param n: (int) chosen randum number 
    :param lives: (int) number of lives left
    :param clock: (clock) pygame clock obj
    :param clicked: (bool) if there was a click
    :param x: (int) x position of the mouse
    :param y: (int) y position of the mouse
    :param congruent: (list) times for congruent words (words correspond to colour)
    :param incongruent: (list) times for incongruent words (words different from colour)
    :return: number of lives left, captured bool
    """

    # Draw borders
    pygame.draw.rect(WIN, BLACK, BORDER_L)
    pygame.draw.rect(WIN, BLACK, BORDER_R)
    pygame.draw.rect(WIN, BLACK, BORDER_T)
    pygame.draw.rect(WIN, BLACK, BORDER_B)


    # Initialize col as the current focus colour (physical colour to be clicked)
    col = rgb[n]

    # Stores number of lost lives
    lost = 0

    # Whether a word has been captured
    captured = False

    # Loops backwards through words list by index
    for i in range(len(words) - 1, -1, -1):

        obj = words[i]

        # Draw word onto the screen
        text = font_game.render(obj.word, True, obj.colour)
        WIN.blit(text, (obj.left, obj.top))

        # Update coordinates
        words[i].left += int(cos(obj.dir) * r)
        words[i].top -= int(sin(obj.dir) * r)

        # Check for hitting the borders
        out = out_of_bounds(words[i].left, words[i].top, text.get_width(), text.get_height())
        # If captured words[i]
        capt = (clicked and in_bound(x, y, obj.left, obj.top, text.get_width(), text.get_height()) and obj.colour == col)
        
        # If lost a heart
        if out and obj.colour == col:
            lost += 1

        # If captured
        if capt:
            captured = True

            # time_diff stored as a float
            time_diff = datetime.now() - obj.birth
            time_diff = float(str(time_diff.seconds) + "." + str(time_diff.microseconds))

            # If word matches the colour
            if obj.word == letter[n]:
                congruent.append(time_diff)
            else:
                incongruent.append(time_diff)

        # Remove current word from the list if captured or out
        if capt or out:
            words.pop(i)
    

    # Initialize left position
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
            clock.tick(DELAYED)
            WIN.blit(pygame.transform.scale(LIFE_IMG, (HEART_D + j, HEART_D + j)), (int(w - j/2), int(20 - j/2)))
            pygame.display.update()

        # Change colour and reduce size
        for j in range(10, 0, -1):
            clock.tick(DELAYED)
            pygame.draw.rect(WIN, WHITE, pygame.Rect(w - 5, 15, 40, 40))
            WIN.blit(pygame.transform.scale(DEAD_IMG, (HEART_D + j, HEART_D + j)), (int(w - j/2), int(20 - j/2)))
            pygame.display.update()
        
        # Increment left position
        w += 50
        
    
    return lives - lost, captured



def draw_text(text):

    """
    Draw text on the screen
    :param text: text that would be shown on the screen
    """

    WIN.fill(WHITE)

    # Split text into list of words
    text = text.split()
    
    # String index
    i = 0

    # Number of words
    n = len(text)

    # Initialized left and top positions
    w, h = 60, 75

    while h < HEIGHT - 60 and i < n:
        while w < WIDTH - 60 and i < n:

            currWord = font_man.render(text[i], False, BLACK)

            # Go to newline if max-width of text has been reached
            if currWord.get_width() + w >= WIDTH - 60:
                break

            # Add to the screen
            WIN.blit(currWord, (w, h))

            # Increment index and left position
            i += 1
            w += currWord.get_width() + 10

        # Increment top to the next line and move position to the very left
        h += currWord.get_height() + 5
        w = 60



def draw_res(same, diff, captures, l):

    """
    Draw results page
    :param same: (float) average time to click words that correspond to their colours
    :param diff: (float) average time to click words that differ from their colours
    :param captures: (int) number of captures
    :param l: (int) highest level achieved
    """

    # Thanks & check for results text
    thanks = "Thank you for playing Strooped! You captured " + str(captures) + " word(s) and achieved level " + str(l) + ". The Stroop effect is our tendency to experience difficulty naming a physical colour when it is used to spell the name of a different colour. Were you affected by the incongruency of the word to the colour in the game? Here are your results!"
    draw_text(thanks)

    # Round to 3 decimal places
    same = "Avg. time to click a word congruent to its colour (s): " + "{:.3f}".format(round(same, 3))
    diff = "Avg. time to click a word incongruent to its colour (s): " + "{:.3f}".format(round(diff, 3))

    # Draw congruent results
    time_s = font_res.render(same, True, BROWN)
    WIN.blit(time_s, (WIDTH//2 - time_s.get_width() // 2, HEIGHT//2 - 15))

    # Draw incongruent results
    time_d = font_res.render(diff, True, BROWN)
    WIN.blit(time_d, (WIDTH//2 - time_d.get_width() // 2, HEIGHT//2 + 35))
 


def main():

    """ 
    MAIN FUNCTION 
    :return: (int) 0 for rerunning the main function again after return and 1 for quitting the game
    """

    # LOCAL VARIABLES --------------------------------------------------->

    clock = pygame.time.Clock()
    run = True

    # Game states
    in_home = True
    in_man = False
    in_game = False
    in_pause = False
    gameover = False


    # List of Colwords that are active in the game screen
    curr_words = []

    # Rate of motion of the colour words in the game -- increases linearly as capture increases
    r = 1.4


    # Initialize mouse (x, y) position
    x, y = 0, 0

    # Max number of lives
    lives = 3

    # Initialize number of captures
    captures = 0


    # Current level
    l = 0

    # Variety of colours (number of types that may appear at the current level)
    col_variety = 1

    # Random focus colour
    rand_num = randint(0, col_variety)


    # List of times to capture words congruent to colours 
    congruent = []

    # List of times to capture words incongrruent to colours
    incongruent = []

    # Average of congruent, average of incongruent
    avg_same, avg_diff = 0, 0


    # Background change rate in the home screen
    bg_rate = 330

    # Datetime of last background change
    last_bg_change = datetime.now() - timedelta(milliseconds=bg_rate)


    # -------------------------------------------------------------------------->


    while run:

        clock.tick(FPS)
        clicked = False
        
        # Check for events
        for event in pygame.event.get():

            # Stop running the game
            if event.type == pygame.QUIT:
                run = False
            
            # Get (x, y) coordinate of the mouse in the window
            x, y, = pygame.mouse.get_pos()

            # Check for clicks in the game
            if in_game and event.type == pygame.MOUSEBUTTONUP:
                clicked = True


        if in_home:

            # Check if the words background need to be updated
            now = datetime.now()
            if last_bg_change < now - timedelta(milliseconds=bg_rate):
                last_bg_change = now
                draw_home(rgb[rand_num])
            

            """ Draw play option button """

            menu_play = font_info.render("[PLAY]", True, GOLD)

            # If hovering on btn
            if in_bound(x, y, WIDTH//2 - menu_play.get_width() // 2, HEIGHT//2 - 25, menu_play.get_width(), menu_play.get_height()):
                menu_play = font_info.render("[PLAY]", True, BROWN)

            menu_play_btn = pygame.Rect((WIDTH//2 - menu_play.get_width() // 2, HEIGHT//2 - 25, menu_play.get_width(), menu_play.get_height()))
            menu_play_rect = menu_play.get_rect()
            menu_play_rect.center = menu_play_btn.center
            pygame.draw.rect(WIN, WHITE, menu_play_btn)
            WIN.blit(menu_play, menu_play_rect)


            """ Draw manual option button """

            menu_man = font_info.render("[MANUAL]", True, GOLD)

            # If hovering on btn
            if in_bound(x, y, WIDTH//2 - menu_man.get_width() // 2, HEIGHT//2 + 25, menu_man.get_width(), menu_man.get_height()):
                menu_man = font_info.render("[MANUAL]", True, BROWN)

            menu_man_btn = pygame.Rect((WIDTH//2 - menu_man.get_width() // 2, HEIGHT//2 + 25, menu_man.get_width(), menu_man.get_height()))
            menu_man_rect = menu_man.get_rect()
            menu_man_rect.center = menu_man_btn.center
            pygame.draw.rect(WIN, WHITE, menu_man_btn)
            WIN.blit(menu_man, menu_man_rect)   


            # Update changes onto the screen
            pygame.display.update()
         
            
            # Check if button is clicked
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()

                # Play game
                if menu_play_btn.collidepoint(mouse):

                    # Update game states
                    in_home = False
                    in_game = True

                    # Pre-game screen - showing first colour
                    WIN.fill(WHITE)
                    play = font_title.render(f"CLICK FOR {letter[rand_num]}!", True, rgb[rand_num])
                    WIN.blit(play, (WIDTH // 2 - play.get_width() // 2, HEIGHT // 2 - play.get_height() // 2))
                    pygame.display.update()
                    time.sleep(0.5)

                # How to play
                elif menu_man_btn.collidepoint(mouse):

                    # Update game states
                    in_home = False
                    in_man = True
                    WIN.fill(WHITE)


        elif in_game:

            WIN.fill(WHITE)

            # Get current level conditions
            col_variety, birth_rate = levels[l]

            # Update rate of motion
            r = 1.4 + captures * 0.1


            # Print the current game stats bar
            if captures < 30:    
                # Still on a level
                count_info = font_info.render("LEVEL: " + str(l) + "  CAPTURES: " + str(captures) + "  FOCUS: " + str(letter[rand_num]), True, GOLD, WHITE)
            else:
                # All levels have been passed
                count_info = font_info.render("LEVEL:--  CAPTURES: " + str(captures) + "  FOCUS: " + str(letter[rand_num]), True, GOLD, WHITE)
            WIN.blit(count_info, (20, 20))


            """ Pause option button """

            pause = font_info.render("[PAUSE]", True, GOLD)

            # If hovering on btn
            if in_bound(x, y, WIDTH - 20 - pause.get_width(), HEIGHT - pause.get_height() - 20, pause.get_width(), pause.get_height()):
                pause = font_info.render("[PAUSE]", True, BROWN)

            pause_btn = pygame.Rect(WIDTH - 20 - pause.get_width(), HEIGHT - pause.get_height() - 20, pause.get_width(), pause.get_height())
            pause_rect = pause.get_rect()
            pause_rect.center = pause_btn.center
            pygame.draw.rect(WIN, WHITE, pause_btn)
            WIN.blit(pause, pause_rect)


            # Draw game and update lives & captures number
            lives, captured = draw_game(curr_words, r, rand_num, lives, clock, clicked, x, y, congruent, incongruent)
            
            if captured:
                captures += 1


            """ If leveled up! """

            if l != captures // 5 and captures < 30:

                # Update level
                l = captures // 5

                # Renew words list
                curr_words = []

                # New focus colour
                rand_num = randint(0, col_variety)

                # Stats bar
                info = "LEVEL: " + str(l) + "  CAPTURES: " + str(captures) + "  FOCUS: " + str(letter[rand_num]) 

                # Initial font weight
                font_weight = 28
                

                # Enlarge stats bar in new colour
                for j in range(3):
                    clock.tick(DELAYED)
                    count_info = pygame.font.SysFont("andalemono", font_weight + j).render(info, True, rgb[rand_num], WHITE)
                    WIN.blit(count_info, (int(20 - j/2), int(20 - j/2)))
                    pygame.display.update()

                # Reduce size of stats bar in new colour
                for j in range(3, 0, -1):
                    clock.tick(DELAYED)
                    count_info = pygame.font.SysFont("andalemono", font_weight + j).render(info, True, rgb[rand_num], WHITE)
                    WIN.blit(count_info, (int(20 - j/2), int(20 - j/2)))
                    pygame.display.update()


            # Check for click for pause
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if pause_btn.collidepoint(mouse):

                    # Update game stats
                    in_pause = True
                    in_game = False
                    draw_backboard()


            # Current datetime
            now = datetime.now()

            # If it's time, create new Colword, save in curr_words, and add onto the screen
            if len(curr_words) == 0 or curr_words[-1].birth < now - timedelta(seconds=birth_rate):
                
                # Get random physical colour
                col = rgb[randint(0, col_variety)]

                # If chosen colour is the focus colour
                if col == rgb[rand_num]:

                    # Allow 50% chance of random congruency to make average results more accurate
                    if randint(0, 1):
                        word = letter[rand_num]
                    else:
                        # Choose random incongruent colour
                        letter_cpy = [letter[i] for i in range(col_variety + 1) if i != rand_num]
                        word = letter_cpy[randint(0, len(letter_cpy) - 1)]
                else:
                    word = letter[randint(0, col_variety)]
                
                # Render the new word onto the screen
                text = font_game.render(word, True, col)
                w = randint(BORD_WIDTH, WIDTH - text.get_width() - BORD_WIDTH)
                h = randint(BORD_WIDTH + HEART_D, HEIGHT - text.get_height() - BORD_WIDTH)
                curr_words.append(Colword(word, col, now, w, h, get_rad(w, h)))
                WIN.blit(text, (w, h))

                # Update
                pygame.display.update()

            
            # If dead
            if lives <= 0:

                """ Check for zero division """

                # Get avg time to capture words congruent to colour
                if len(congruent) == 0:
                    avg_same = 0
                else:
                    avg_same = sum(congruent) / len(congruent)

                # Get avg time to capture words incongruent to colour
                if len(incongruent) == 0:
                    avg_diff = 0
                else:
                    avg_diff = sum(incongruent) / len(incongruent)

                # Update game stats
                gameover = True
                in_game = False


        elif in_pause:

            """ Draw menu option buttons """

            # Continue
            cont = font_info.render("[CONTINUE]", True, GOLD)

            # If hovering on btn
            if in_bound(x, y, WIDTH//2 - cont.get_width() // 2, HEIGHT//2 - 75, cont.get_width(), cont.get_height()):
                cont = font_info.render("[CONTINUE]", True, BROWN)

            cont_btn = pygame.Rect((WIDTH//2 - cont.get_width() // 2, HEIGHT//2 - 75, cont.get_width(), cont.get_height()))
            cont_rect = cont.get_rect()
            cont_rect.center = cont_btn.center
            pygame.draw.rect(WIN, WHITE, cont_btn)
            WIN.blit(cont, cont_rect)


            # Go to manual
            to_man = font_info.render("[MANUAL]", True, GOLD)

            # If hovering on btn
            if in_bound(x, y, WIDTH//2 - to_man.get_width() // 2, HEIGHT//2, to_man.get_width(), to_man.get_height()):
                to_man = font_info.render("[MANUAL]", True, BROWN)

            to_man_btn = pygame.Rect((WIDTH//2 - to_man.get_width() // 2, HEIGHT//2, to_man.get_width(), to_man.get_height()))
            to_man_rect = to_man.get_rect()
            to_man_rect.center = to_man_btn.center
            pygame.draw.rect(WIN, WHITE, to_man_btn)
            WIN.blit(to_man, to_man_rect)


            # Quit game and go to home
            to_quit = font_info.render("[QUIT]", True, GOLD)

            # If hovering on btn
            if in_bound(x, y, WIDTH//2 - to_quit.get_width() // 2, HEIGHT//2 + 75, to_quit.get_width(), to_quit.get_height()):
                to_quit = font_info.render("[QUIT]", True, BROWN)

            to_quit_btn = pygame.Rect((WIDTH//2 - to_quit.get_width() // 2, HEIGHT//2 + 75, to_quit.get_width(), to_quit.get_height()))
            to_quit_rect = to_quit.get_rect()
            to_quit_rect.center = to_quit_btn.center
            pygame.draw.rect(WIN, WHITE, to_quit_btn)
            WIN.blit(to_quit, to_quit_rect)

            # Update
            pygame.display.update()


            # Check for clicks
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()

                # If continue game, update stats
                if cont_btn.collidepoint(mouse):
                    in_pause = False
                    in_game = True

                # If go to manual, update stats
                elif to_man_btn.collidepoint(mouse):
                    in_man = True
                    in_pause = False

                # If quit to home, update stats
                elif to_quit_btn.collidepoint(mouse):
                    return 0


        else:
            WIN.fill(WHITE)


            # Draw results page if game over
            if gameover:
                draw_res(avg_same, avg_diff, captures, l)


            # Explain how to play if in manual
            if in_man:
                text = """
After clicking `Play` in the home page, the window will display the first colour for the user to click for. Clicking the right coloured words will increase the `Captures` score and missing the right coloured words will result in a loss of life, indicated by a quick pause in the game in which a red heart pops into a gray one. A word will be considered to be missed when it hits one of the borders of the game. 

After every 5 captures, there will be a level up and a new physical colour to be clicked for. The event of a level up will be also be indicated by a quick pause in the game in which the game info banner at the top of the window will enlarge in size and change into the new focus colour to be clicked. The screen will also be entirely cleared. After the banner returns to the normal size, the game resumes and the user must click for the new colour. The colour to be clicked for will always be displayed in the banner.

There are no penalties for clicking or missing a coloured word that is not in focus for the current level. After reaching 30 captures, the levels are considered completed and the game runs infinitely, while increasing in speed.
"""
                draw_text(text)

                play_from_man = font_info.render("[PLAY]", True, GOLD, WHITE)

                # Hovering to play
                if in_bound(x, y, 165, 20, play_from_man.get_width(), play_from_man.get_height()):
                    play_from_man = font_info.render("[PLAY]", True, BROWN, WHITE)

                play_from_man_btn = pygame.Rect(165, 20, play_from_man.get_width(), play_from_man.get_height())
                play_from_man_rect = menu_play.get_rect()
                play_from_man_rect.center = play_from_man_btn.center
                pygame.draw.rect(WIN, WHITE, play_from_man_btn)
                WIN.blit(play_from_man, play_from_man_rect)


            # Make back to home button
            back = font_info.render("[HOME]", True, GOLD, WHITE)

            # If hovering on button
            if in_bound(x, y, 55, 20, back.get_width(), back.get_height()):
                back = font_info.render("[HOME]", True, BROWN, WHITE)

            back_btn = pygame.Rect(55, 20, back.get_width(), back.get_height())
            back_rect = menu_play.get_rect()
            back_rect.center = back_btn.center
            pygame.draw.rect(WIN, WHITE, back_btn)
            WIN.blit(back, back_rect)
            pygame.display.update()


            # Check for clicks
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()

                # If going back to home, restart main
                if back_btn.collidepoint(mouse):
                    return 0

                # If going to play from manual, update stats
                if in_man and play_from_man_btn.collidepoint(mouse):
                    in_man = False
                    in_game = True
                
    pygame.quit()
    return 1


if __name__ == "__main__":

    # Unless returns True to quit from main, keep checking
    while not main():
        continue


""" 
PSEUDO-CODE =========================================================================================================>

FUNCTIONS

get_rad(x, y)
out_of_bounds(left, top, w, h)
in_bound(x, y, left, top, w, h)
draw_backboard()
draw_home(rand_col)
draw_game(words, r, n, lives, clock, clicked, x, y, congruent, incongruent)
draw_text(text)
draw_res(same, diff, captures, l)
main()


import pygame
import os
import time
from random import randint, uniform, shuffle
from datetime import datetime, timedelta
from math import sin, cos, pi

pygame.init()

FPS = 60
DELAYED = 30
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Strooped!")

BORD_WIDTH = 10
BORDER_L = pygame.Rect(0, 0, BORD_WIDTH, HEIGHT)
BORDER_R = pygame.Rect(WIDTH - BORD_WIDTH, 0, BORD_WIDTH, HEIGHT)
BORDER_T = pygame.Rect(0, 0, WIDTH, BORD_WIDTH)
BORDER_B = pygame.Rect(0, HEIGHT - BORD_WIDTH, WIDTH, BORD_WIDTH)

HEART_D = 30
LIFE_IMG = pygame.image.load(os.path.join('Assets', 'red.png'))
LIFE = pygame.transform.scale(LIFE_IMG, (HEART_D, HEART_D))
DEAD_IMG = pygame.image.load(os.path.join('Assets', 'grey.png'))
DEAD = pygame.transform.scale(DEAD_IMG, (HEART_D, HEART_D))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (211, 211, 211)
GOLD = (175, 130, 30)
BROWN = (150, 75, 0)
BLUE = (0, 64, 255)
RED = (200, 30, 40)
GREEN = (0, 150, 30)
PURPLE = (150, 0, 205)
ORANGE = (255, 92, 0)
CYAN = (0, 180, 171)
PINK = (255, 105, 180)

levels = ((1, 2), (1, 1.5), (3, 1.5), (3, 1), (6, 1), (6, 0.5))
colour_rgb = {"BLUE": BLUE, "RED": RED, "GREEN": GREEN, "PURPLE": PURPLE, "ORANGE": ORANGE, "CYAN": CYAN, "PINK": PINK}
keys = list(colour_rgb.keys())
shuffle(keys)
shuffled_rgb = {key: colour_rgb[key] for key in keys}
letter = tuple(keys)
rgb = tuple(shuffled_rgb.values())

font_title = pygame.font.SysFont("ptmono", 60)
font_info = pygame.font.SysFont("andalemono", 28)
font_res = pygame.font.SysFont("andalemono", 18)
font_mini = pygame.font.SysFont("ptmono", 18)
font_game = pygame.font.SysFont("sfnsmono", 36)
font_man = pygame.font.SysFont("futura", 17)

class Colword:
    def __init__(self, word, colour, birth, left, top, dir):
        self.word = word
        self.colour = colour
        self.birth = birth
        self.left = left
        self.top = top
        self.dir = dir


function get_rad(x, y):
    if y < HEIGHT / 2:
        if x > WIDTH / 2:
            return uniform(pi, 3 * pi / 2)    
        return uniform(3 * pi / 2, 2 * pi)
    if x < WIDTH / 2:
        return uniform(0, pi / 2)
    return uniform(pi / 2, pi)
end get_rad


function out_of_bounds(left, top, w, h):
    if left <= BORD_WIDTH or top <= BORD_WIDTH + HEART_D or left + w >= WIDTH - BORD_WIDTH or top + h >= HEIGHT - BORD_WIDTH:
        return True
    return False
end out_of_bounds


function in_bound(x, y, left, top, w, h):
    if left <= x <= left + w and top <= y <= top + h:
        return True
    return False
end in_bound


function draw_backboard():
    pygame.draw.rect(WIN, WHITE, pygame.Rect(WIDTH // 5, HEIGHT//3 - 60, WIDTH - 2 * (WIDTH // 5), HEIGHT - 2 * (HEIGHT//3 - 70)), 200, 50)
    pygame.draw.rect(WIN, (245, 245, 245), pygame.Rect(WIDTH // 5, HEIGHT//3 - 60, WIDTH - 2 * (WIDTH // 5), HEIGHT - 2 * (HEIGHT//3 - 70)), 10, 50)
end draw_backboard


function draw_home(rand_col):
    WIN.fill(WHITE)
    n = len(letter) - 1
    w, h = 0, 0
    while h < HEIGHT:
        while w < WIDTH:
            bg = font_game.render(letter[randint(0, n)], True, GRAY)
            WIN.blit(bg, (w, h))
            w += bg.get_width() + 4
        h += bg.get_height()
        w = 0
    draw_backboard()
    title = font_title.render("STROOPED!", True, rand_col, WHITE)
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3 - title.get_height() // 2))
    mini = font_mini.render("How well can you distinguish your colours?", True, rand_col, WHITE)
    WIN.blit(mini, (WIDTH // 2 - mini.get_width() // 2, HEIGHT * 3 // 4 - mini.get_height()))
end draw_home


function draw_game(words, r, n, lives, clock, clicked, x, y, congruent, incongruent):
    pygame.draw.rect(WIN, BLACK, BORDER_L)
    pygame.draw.rect(WIN, BLACK, BORDER_R)
    pygame.draw.rect(WIN, BLACK, BORDER_T)
    pygame.draw.rect(WIN, BLACK, BORDER_B)
    col = rgb[n]
    lost = 0
    captured = False
    for i in range(len(words) - 1, -1, -1):
        obj = words[i]
        text = font_game.render(obj.word, True, obj.colour)
        WIN.blit(text, (obj.left, obj.top))
        words[i].left += int(cos(obj.dir) * r)
        words[i].top -= int(sin(obj.dir) * r)
        out = out_of_bounds(words[i].left, words[i].top, text.get_width(), text.get_height())
        capt = (clicked and in_bound(x, y, obj.left, obj.top, text.get_width(), text.get_height()) and obj.colour == col)
        if out and obj.colour == col:
            lost += 1
        if capt:
            captured = True
            time_diff = datetime.now() - obj.birth
            time_diff = float(str(time_diff.seconds) + "." + str(time_diff.microseconds))
            if obj.word == letter[n]:
                congruent.append(time_diff)
            else:
                incongruent.append(time_diff)
        if capt or out:
            words.pop(i)
    w = WIDTH - 60
    for i in range(lives):
        WIN.blit(LIFE, (w, 20))
        w -= 50
    for i in range(3 - lives):
        WIN.blit(DEAD, (w, 20))
        w -= 50
    w += 50 * (3 - lives + 1)

    pygame.display.update()

    for i in range(lost):
        for j in range(10):
            clock.tick(DELAYED)
            WIN.blit(pygame.transform.scale(LIFE_IMG, (HEART_D + j, HEART_D + j)), (int(w - j/2), int(20 - j/2)))
            pygame.display.update()
        for j in range(10, 0, -1):
            clock.tick(DELAYED)
            pygame.draw.rect(WIN, WHITE, pygame.Rect(w - 5, 15, 40, 40))
            WIN.blit(pygame.transform.scale(DEAD_IMG, (HEART_D + j, HEART_D + j)), (int(w - j/2), int(20 - j/2)))
            pygame.display.update()
        w += 50
    return lives - lost, captured
end draw_game


function draw_text(text):
    WIN.fill(WHITE)
    text = text.split()
    i = 0
    n = len(text)
    w, h = 60, 75
    while h < HEIGHT - 60 and i < n:
        while w < WIDTH - 60 and i < n:
            currWord = font_man.render(text[i], False, BLACK)
            if currWord.get_width() + w >= WIDTH - 60:
                break
            WIN.blit(currWord, (w, h))
            i += 1
            w += currWord.get_width() + 10
        h += currWord.get_height() + 5
        w = 60
end draw_text


function draw_res(same, diff, captures, l):
    thanks = "Thank you for playing Strooped! You captured " + str(captures) + " word(s) and achieved level " + str(l) + ". The Stroop effect is our tendency to experience difficulty naming a physical colour when it is used to spell the name of a different colour. Were you affected by the incongruency of the word to the colour in the game? Here are your results!"
    draw_text(thanks)
    same = "Avg. time to click a word congruent to its colour (s): " + "{:.3f}".format(round(same, 3))
    diff = "Avg. time to click a word incongruent to its colour (s): " + "{:.3f}".format(round(diff, 3))
    time_s = font_res.render(same, True, BROWN)
    WIN.blit(time_s, (WIDTH//2 - time_s.get_width() // 2, HEIGHT//2 - 15))
    time_d = font_res.render(diff, True, BROWN)
    WIN.blit(time_d, (WIDTH//2 - time_d.get_width() // 2, HEIGHT//2 + 35))
end draw_res


function main():
    clock = pygame.time.Clock()
    run = True
    in_home = True
    in_man = False
    in_game = False
    in_pause = False
    gameover = False
    curr_words = []
    r = 1.4
    x, y = 0, 0
    lives = 3
    captures = 0
    l = 0
    col_variety = 1
    rand_num = randint(0, col_variety)
    congruent = []
    incongruent = []
    avg_same, avg_diff = 0, 0
    bg_rate = 330
    last_bg_change = datetime.now() - timedelta(milliseconds=bg_rate)
    while run:
        clock.tick(FPS)
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            x, y, = pygame.mouse.get_pos()
            if in_game and event.type == pygame.MOUSEBUTTONUP:
                clicked = True
        if in_home:
            now = datetime.now()
            if last_bg_change < now - timedelta(milliseconds=bg_rate):
                last_bg_change = now
                draw_home(rgb[rand_num])
            menu_play = font_info.render("[PLAY]", True, GOLD)
            if in_bound(x, y, WIDTH//2 - menu_play.get_width() // 2, HEIGHT//2 - 25, menu_play.get_width(), menu_play.get_height()):
                menu_play = font_info.render("[PLAY]", True, BROWN)
            menu_play_btn = pygame.Rect((WIDTH//2 - menu_play.get_width() // 2, HEIGHT//2 - 25, menu_play.get_width(), menu_play.get_height()))
            menu_play_rect = menu_play.get_rect()
            menu_play_rect.center = menu_play_btn.center
            pygame.draw.rect(WIN, WHITE, menu_play_btn)
            WIN.blit(menu_play, menu_play_rect)

            menu_man = font_info.render("[MANUAL]", True, GOLD)
            if in_bound(x, y, WIDTH//2 - menu_man.get_width() // 2, HEIGHT//2 + 25, menu_man.get_width(), menu_man.get_height()):
                menu_man = font_info.render("[MANUAL]", True, BROWN)
            menu_man_btn = pygame.Rect((WIDTH//2 - menu_man.get_width() // 2, HEIGHT//2 + 25, menu_man.get_width(), menu_man.get_height()))
            menu_man_rect = menu_man.get_rect()
            menu_man_rect.center = menu_man_btn.center
            pygame.draw.rect(WIN, WHITE, menu_man_btn)
            WIN.blit(menu_man, menu_man_rect)   

            pygame.display.update()
         
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if menu_play_btn.collidepoint(mouse):
                    in_home = False
                    in_game = True
                    WIN.fill(WHITE)
                    play = font_title.render(f"CLICK FOR {letter[rand_num]}!", True, rgb[rand_num])
                    WIN.blit(play, (WIDTH // 2 - play.get_width() // 2, HEIGHT // 2 - play.get_height() // 2))
                    pygame.display.update()
                    time.sleep(0.5)
                elif menu_man_btn.collidepoint(mouse):
                    in_home = False
                    in_man = True
                    WIN.fill(WHITE)

        elif in_game:
            WIN.fill(WHITE)
            col_variety, birth_rate = levels[l]
            r = 1.4 + captures * 0.1
            if captures < 30:    
                count_info = font_info.render("LEVEL: " + str(l) + "  CAPTURES: " + str(captures) + "  FOCUS: " + str(letter[rand_num]), True, GOLD, WHITE)
            else:
                count_info = font_info.render("LEVEL:--  CAPTURES: " + str(captures) + "  FOCUS: " + str(letter[rand_num]), True, GOLD, WHITE)
            WIN.blit(count_info, (20, 20))
            pause = font_info.render("[PAUSE]", True, GOLD)
            if in_bound(x, y, WIDTH - 20 - pause.get_width(), HEIGHT - pause.get_height() - 20, pause.get_width(), pause.get_height()):
                pause = font_info.render("[PAUSE]", True, BROWN)
            pause_btn = pygame.Rect(WIDTH - 20 - pause.get_width(), HEIGHT - pause.get_height() - 20, pause.get_width(), pause.get_height())
            pause_rect = pause.get_rect()
            pause_rect.center = pause_btn.center
            pygame.draw.rect(WIN, WHITE, pause_btn)
            WIN.blit(pause, pause_rect)

            lives, captured = draw_game(curr_words, r, rand_num, lives, clock, clicked, x, y, congruent, incongruent)
            if captured:
                captures += 1

            if l != captures // 5 and captures < 30:
                l = captures // 5
                curr_words = []
                rand_num = randint(0, col_variety)
                info = "LEVEL: " + str(l) + "  CAPTURES: " + str(captures) + "  FOCUS: " + str(letter[rand_num]) 
                font_weight = 28
                
                for j in range(3):
                    clock.tick(DELAYED)
                    count_info = pygame.font.SysFont("andalemono", font_weight + j).render(info, True, rgb[rand_num], WHITE)
                    WIN.blit(count_info, (int(20 - j/2), int(20 - j/2)))
                    pygame.display.update()

                for j in range(3, 0, -1):
                    clock.tick(DELAYED)
                    count_info = pygame.font.SysFont("andalemono", font_weight + j).render(info, True, rgb[rand_num], WHITE)
                    WIN.blit(count_info, (int(20 - j/2), int(20 - j/2)))
                    pygame.display.update()

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if pause_btn.collidepoint(mouse):
                    in_pause = True
                    in_game = False
                    draw_backboard()

            now = datetime.now()
            if len(curr_words) == 0 or curr_words[-1].birth < now - timedelta(seconds=birth_rate):
                col = rgb[randint(0, col_variety)]
                if col == rgb[rand_num]:
                    if randint(0, 1):
                        word = letter[rand_num]
                    else:
                        letter_cpy = [letter[i] for i in range(col_variety + 1) if i != rand_num]
                        word = letter_cpy[randint(0, len(letter_cpy) - 1)]
                else:
                    word = letter[randint(0, col_variety)]
                text = font_game.render(word, True, col)
                w = randint(BORD_WIDTH, WIDTH - text.get_width() - BORD_WIDTH)
                h = randint(BORD_WIDTH + HEART_D, HEIGHT - text.get_height() - BORD_WIDTH)
                curr_words.append(Colword(word, col, now, w, h, get_rad(w, h)))
                WIN.blit(text, (w, h))
                pygame.display.update()

            if lives <= 0:
                if len(congruent) == 0:
                    avg_same = 0
                else:
                    avg_same = sum(congruent) / len(congruent)
                if len(incongruent) == 0:
                    avg_diff = 0
                else:
                    avg_diff = sum(incongruent) / len(incongruent)
                gameover = True
                in_game = False


        elif in_pause:
            cont = font_info.render("[CONTINUE]", True, GOLD)
            if in_bound(x, y, WIDTH//2 - cont.get_width() // 2, HEIGHT//2 - 75, cont.get_width(), cont.get_height()):
                cont = font_info.render("[CONTINUE]", True, BROWN)
            cont_btn = pygame.Rect((WIDTH//2 - cont.get_width() // 2, HEIGHT//2 - 75, cont.get_width(), cont.get_height()))
            cont_rect = cont.get_rect()
            cont_rect.center = cont_btn.center
            pygame.draw.rect(WIN, WHITE, cont_btn)
            WIN.blit(cont, cont_rect)

            to_man = font_info.render("[MANUAL]", True, GOLD)

            if in_bound(x, y, WIDTH//2 - to_man.get_width() // 2, HEIGHT//2, to_man.get_width(), to_man.get_height()):
                to_man = font_info.render("[MANUAL]", True, BROWN)
            to_man_btn = pygame.Rect((WIDTH//2 - to_man.get_width() // 2, HEIGHT//2, to_man.get_width(), to_man.get_height()))
            to_man_rect = to_man.get_rect()
            to_man_rect.center = to_man_btn.center
            pygame.draw.rect(WIN, WHITE, to_man_btn)
            WIN.blit(to_man, to_man_rect)

            to_quit = font_info.render("[QUIT]", True, GOLD)
            if in_bound(x, y, WIDTH//2 - to_quit.get_width() // 2, HEIGHT//2 + 75, to_quit.get_width(), to_quit.get_height()):
                to_quit = font_info.render("[QUIT]", True, BROWN)
            to_quit_btn = pygame.Rect((WIDTH//2 - to_quit.get_width() // 2, HEIGHT//2 + 75, to_quit.get_width(), to_quit.get_height()))
            to_quit_rect = to_quit.get_rect()
            to_quit_rect.center = to_quit_btn.center
            pygame.draw.rect(WIN, WHITE, to_quit_btn)
            WIN.blit(to_quit, to_quit_rect)

            pygame.display.update()

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if cont_btn.collidepoint(mouse):
                    in_pause = False
                    in_game = True
                elif to_man_btn.collidepoint(mouse):
                    in_man = True
                    in_pause = False
                elif to_quit_btn.collidepoint(mouse):
                    return 0
        else:
            WIN.fill(WHITE)
            if gameover:
                draw_res(avg_same, avg_diff, captures, l)
            if in_man:
                text = '''
After clicking `Play` in the home page, the window will display the first colour for the user to click for. Clicking the right coloured words will increase the `Captures` score and missing the right coloured words will result in a loss of life, indicated by a quick pause in the game in which a red heart pops into a gray one. A word will be considered to be missed when it hits one of the borders of the game. 

After every 5 captures, there will be a level up and a new colour to be clicked for. The event of a level up will be also be indicated by a quick pause in the game in which the game info banner at the top of the window will enlarge in size and change into the new colour to be clicked. The screen will also be entirely cleared. After the banner returns to the normal size, the game resumes and the user must click for the new colour. The colour to be clicked for will always be displayed in the banner.

There are no penalties for clicking or missing a coloured word that is not in focus for the current level. After reaching 30 captures, the levels are completed and the game runs infinitely, while increasing in speed.
'''
                draw_text(text)

                play_from_man = font_info.render("[PLAY]", True, GOLD, WHITE)
                if in_bound(x, y, 165, 20, play_from_man.get_width(), play_from_man.get_height()):
                    play_from_man = font_info.render("[PLAY]", True, BROWN, WHITE)
                play_from_man_btn = pygame.Rect(165, 20, play_from_man.get_width(), play_from_man.get_height())
                play_from_man_rect = menu_play.get_rect()
                play_from_man_rect.center = play_from_man_btn.center
                pygame.draw.rect(WIN, WHITE, play_from_man_btn)
                WIN.blit(play_from_man, play_from_man_rect)

            back = font_info.render("[HOME]", True, GOLD, WHITE)
            if in_bound(x, y, 55, 20, back.get_width(), back.get_height()):
                back = font_info.render("[HOME]", True, BROWN, WHITE)
            back_btn = pygame.Rect(55, 20, back.get_width(), back.get_height())
            back_rect = menu_play.get_rect()
            back_rect.center = back_btn.center
            pygame.draw.rect(WIN, WHITE, back_btn)
            WIN.blit(back, back_rect)
            pygame.display.update()

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if back_btn.collidepoint(mouse):
                    return 0
                if in_man and play_from_man_btn.collidepoint(mouse):
                    in_man = False
                    in_game = True
                
    pygame.quit()
    return 1
end main 


MAIN PROGRAM
if __name__ == "__main__":
    while not main():
        continue

=============================================>

"""


