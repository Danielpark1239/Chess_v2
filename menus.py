from chess import Board
import pygame as pg
import pygame_menu as pgm
from constants import *

class MainMenu:
    def __init__(self):
        self.menu = pgm.Menu(
            title = "Chess v2.0",
            width = MENU_WIDTH,
            height = MENU_HEIGHT,
            theme = pgm.themes.THEME_DARK
        )

class OnePlayerMenu:
    def __init__(self):
        self.menu = pgm.Menu(
            title = "Select Difficulty",
            width = MENU_WIDTH,
            height = MENU_HEIGHT,
            theme = pgm.themes.THEME_DARK
        )
        self.menu.add.range_slider(
            title = "Computer elo rating:",
            default = DEFAULT_COMPUTER_ELO, 
            range_values = (MIN_COMPUTER_ELO, MAX_COMPUTER_ELO),
            increment = ELO_INCREMENT,
            onchange = self.selectDifficulty,
            value_format = lambda x: str(int(x))
        )
        self.difficulty = DEFAULT_COMPUTER_ELO
        self.menu.add.toggle_switch(
            title='Play as white?', 
            default=True,
            onchange=self.selectColor
        )
        self.color = True #Play as White for True, Black for False
    
    def selectDifficulty(self, range_value):
        self.difficulty = int(range_value)
    
    def selectColor(self, current_state_value):
        self.color = current_state_value

class GameGUI:
    def __init__(self):
        self.menu = pgm.Menu(
            "Settings", 
            GUI_WIDTH, 
            GUI_HEIGHT,
            position=(770, 80, False), 
            theme=pgm.themes.THEME_DARK
        )
        # self.menu.add.button("Offer draw?", ) 
        # self.menu.add.button('Resign?', )
    # add settings for:
    # flipping the Board
    # playing as white or black
    # timer?
    # draw button
    # resignation button
    # game over screen
    # back to main menu button
    # move undo button?

    # update gui and game loop


    

# takes a tuple board indices and a boolean color (True = white) as parameters
class PromotionMenu:
    def __init__(self, indices, color):
        self.promotion = None # "WQ", "WR", etc. Matches format in .png files
        xPos = SQUARE_CENTERS[indices[0]]
        yPos = SQUARE_CENTERS[indices[1]]
        size = MENU_WIDTH / 3
        self.menu = pgm.Menu(
            title = "Promote",
            width = size,
            height = size,
            theme = pgm.themes.THEME_DARK,
            position = (xPos - size/2, yPos - (size/2) - 15, False)
        )
        self.table = self.menu.add.table(table_id="promotion table", font_size=30)
        self.table.default_cell_padding = 5
        self.table.default_cell_align = pgm.locals.ALIGN_CENTER

        if (color):
            # add images
            WQ = self.menu.add.image("BoardWQ.png", scale=(0.1, 0.1))
            WR = self.menu.add.image("BoardWR.png", scale=(0.055, 0.05))
            WB = self.menu.add.image("BoardWB.png", scale=(0.05, 0.05))
            WN = self.menu.add.image("BoardWN.png", scale=(0.055, 0.05))
            
            # set up the table
            self.table.add_row([WQ, WR])
            self.table.add_row([WB, WN])
            
        else:
            # add images
            BQ = self.menu.add.image("BoardBQ.png", scale=(0.05, 0.05))
            BR = self.menu.add.image("BoardBR.png", scale=(0.055, 0.05))
            BB = self.menu.add.image("BoardBB.png", scale=(0.25, 0.25))
            BN = self.menu.add.image("BoardBN.png", scale=(0.055, 0.05))
            
            # set up the table
            self.table.add_row([BQ, BR])
            self.table.add_row([BB, BN])
   
            


    





    
