# Strooped!
A python game to test the Stroop effect - the delay in reaction time between congruent (same word and colour) and incongruent (different word and colour) stimuli. Developed as an ICS3U final project.

# Usage
Run:
`python3 main.py`

# How to play
After clicking `Play` in the home page, the window will display the first colour for the user to click for. Clicking the right coloured words will increase the `Captures` score and missing the right coloured words will result in a loss of life, indicated by a quick pause in the game in which a red heart pops into a gray one. A word will be considered to be missed when it hits one of the borders of the game. 

After every 5 captures, there will be a level up and a new physical colour to be clicked for. The event of a level up will be also be indicated by a quick pause in the game in which the game info banner at the top of the window will enlarge in size and change into the new focus colour to be clicked. The screen will also be entirely cleared. After the banner returns to the normal size, the game resumes and the user must click for the new colour. The colour to be clicked for will always be displayed in the banner.

There are no penalties for clicking or missing a coloured word that is not in focus for the current level. After reaching 30 captures, the levels are considered completed and the game runs infinitely, while increasing in speed.


# Features

# Advanced concepts used

