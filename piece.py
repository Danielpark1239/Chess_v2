import pygame as pg
from constants import *

# Set up piece images
pg.init()
pg.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
WR = pg.image.load("assets/BoardWR.png").convert_alpha()
WR = pg.transform.smoothscale(WR, (54, 59))
BR = pg.image.load("assets/BoardBR.png").convert_alpha()
BR = pg.transform.smoothscale(BR, (54, 59))
WN = pg.image.load("assets/BoardWN.png").convert_alpha()
WN = pg.transform.smoothscale(WN, (55, 60))
BN = pg.image.load("assets/BoardBN.png").convert_alpha()
BN = pg.transform.smoothscale(BN, (55, 60))
WB = pg.image.load("assets/BoardWB.png").convert_alpha()
WB = pg.transform.smoothscale(WB, (60, 60))
BB = pg.image.load("assets/BoardBB.png").convert_alpha()
BB = pg.transform.smoothscale(BB, (60, 60))
WQ = pg.image.load("assets/BoardWQ.png").convert_alpha()
WQ = pg.transform.smoothscale(WQ, (60, 58))
BQ = pg.image.load("assets/BoardBQ.png").convert_alpha()
BQ = pg.transform.smoothscale(BQ, (60, 58))
WK = pg.image.load("assets/BoardWK.png").convert_alpha()
WK = pg.transform.smoothscale(WK, (60, 60))
BK = pg.image.load("assets/BoardBK.png").convert_alpha()
BK = pg.transform.smoothscale(BK, (60, 60))
WP = pg.image.load("assets/BoardWP.png").convert_alpha()
WP = pg.transform.smoothscale(WP, (45,60))
BP = pg.image.load("assets/BoardBP.png").convert_alpha()
BP = pg.transform.smoothscale(BP, (45,60))

# Define piece class
class Piece(pg.sprite.Sprite):
    # This class represents a piece, derived from the Sprite class in pg
    # the pieces have type R, N, B, K, Q, P, uppercase if white and 
    # lowercase for black
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.x = x
        self.y = y

        match type:
            case "P":
                self.image = WP
            case "R":
                self.image = WR
            case "N":
                self.image = WN
            case "B":
                self.image = WB
            case "Q":
                self.image = WQ
            case "K":
                self.image = WK
            case "p":
                self.image = BP
            case "r":
                self.image = BR
            case "n":
                self.image = BN
            case "b":
                self.image = BB
            case "q":
                self.image = BQ
            case "k":
                self.image = BK

        # centers the piece's rect on the square
        self.rect = pg.Rect(
            SQUARE_CENTERS[x]-self.image.get_width()/2,
            SQUARE_CENTERS[y]-self.image.get_height()/2, 
            self.image.get_width(),
            self.image.get_height()
        )

    def getX(self):
        return self.x

    def getY(self):
        return self.y
    
    # updates the parameters of the piece given board indices x, y
    def update(self, x, y):
        self.x = x
        self.y = y
        self.rect = pg.Rect(
            SQUARE_CENTERS[x]-self.image.get_width()/2, 
            SQUARE_CENTERS[y]-self.image.get_height()/2, 
            self.image.get_width(), 
            self.image.get_height()
        )
    
    # updates the piece rect given screen coordinates x, y
    def updateRect(self, x, y):
        self.rect = pg.Rect(
            x-self.image.get_width()/2,
            y-self.image.get_height()/2, 
            self.image.get_width(), 
            self.image.get_height()
        )

    # Returns True if the piece is white, False otherwise
    def isWhite(self):
        return True if self.type.isupper() else False
    
    # return the piece's type
    def getType(self):
        return self.type
    
    # given a piece, promote it to the piece specified by type.
    # "q" for queen, "b" for bishop, "r" for rook, "n" for knight.
    # Raise an exception if the piece is not a pawn or the type is not valid.
    def promote(self, type):
        assert(self.type == "P" or self.type == "p")
        if (type == "q"):
            if (self.type == "p"):
                self.type = "q"
                self.image = BQ
            else:
                self.type = "Q"
                self.image = WQ

        elif (type == "b"):
            if (self.type == "p"):
                self.type = "b"
                self.image = BB
            else:
                self.type = "B"
                self.image = WB

        elif (type == "r"):
            if (self.type == "p"):
                self.type = "r"
                self.image = BR
            else:
                self.type = "R"
                self.image = WR

        elif (type == "n"):
            if (self.type == "p"):
                self.type = "n"
                self.image = BN
            else:
                self.type = "N"
                self.image = WN

        else:
            raise ValueError("type is not valid.")

        
    