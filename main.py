import pygame as pg
import pygame_menu as pgm
from constants import *
import game
import menus


pg.init()
menuScreen = pg.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
pg.display.set_caption("Play Chess")

# One-player mode submenu
onePlayer_menu = menus.OnePlayerMenu()

# Main menu
main_menu = menus.MainMenu()
main_menu.menu.add.button('1 Player', onePlayer_menu.menu)

# One-player mode game loop
def startOnePlayer():
    main_menu.menu.disable()
    activeGame = game.OnePlayer(
        onePlayer_menu.difficulty, 
        DEFAULT_FENSTRING,
        onePlayer_menu.color
    )
    activeGame.runGame()
    pg.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
    main_menu.menu.enable()

# Two-player mode game loop
def startTwoPlayer():
    main_menu.menu.disable()
    activeGame = game.TwoPlayer(
        ##### Add settings here
    )
    activeGame.runGame()
    pg.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
    main_menu.menu.enable()

onePlayer_menu.menu.add.button('Start game!', startOnePlayer)
onePlayer_menu.menu.add.button('Back', pgm.events.BACK)
main_menu.menu.add.button('2 Player (Local)', None)#twoPlayer)
main_menu.menu.add.button('Quit', pgm.events.EXIT)

while main_menu.menu.is_enabled:
    main_menu.menu.mainloop(menuScreen)









