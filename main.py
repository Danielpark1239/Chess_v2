import pygame as pg
import pygame_menu as pgm
from constants import *
import game

pg.init()
menuScreen = pg.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
pg.display.set_caption("Play Chess")

difficulty = DEFAULT_COMPUTER_ELO
def selectDifficulty(range_value):
    global difficulty
    difficulty = int(range_value)

# Main menu
main_menu = pgm.Menu(
    title = "Chess v2.0",
    width = MENU_WIDTH,
    height = MENU_HEIGHT,
    theme = pgm.themes.THEME_DARK,
)

# One-player mode submenu
onePlayer_menu = pgm.Menu(
    title = "Select Difficulty",
    width = MENU_WIDTH,
    height = MENU_HEIGHT,
    theme = pgm.themes.THEME_DARK,
)
main_menu.add.button('1 Player', onePlayer_menu)
onePlayer_menu.add.range_slider(
    title = "Computer elo rating:",
    default = DEFAULT_COMPUTER_ELO, 
    range_values = (MIN_COMPUTER_ELO, MAX_COMPUTER_ELO),
    increment = ELO_INCREMENT,
    onchange = selectDifficulty,
    value_format = lambda x: str(int(x))
)

# One-player mode game loop
def startOnePlayer():
    main_menu.disable()
    activeGame = game.OnePlayer(difficulty)
    activeGame.runGame()

onePlayer_menu.add.button('Start game!', startOnePlayer)
onePlayer_menu.add.button('Back', pgm.events.BACK)
main_menu.add.button('2 Player (Local)', None)#twoPlayer)
main_menu.add.button('Quit', pgm.events.EXIT)

while main_menu.is_enabled:
    main_menu.mainloop(menuScreen)








