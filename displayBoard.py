from piece import Piece
from FENreader import FENreader
from constants import *
import pygame as pg

# class that keeps track of the pieces on the board;
# used with pygame to display the board state
class DisplayBoard:
    def __init__(self, FENstring):
        pieceList = FENreader(FENstring).getPieces()

        # a dictionary that maps squares (tuple:(x,y)) to pieces on the board
        self.pieceMap = {
            (piece.getX(), piece.getY()): piece for piece in pieceList
        }

        # pygame rects for all board squares
        boardSq = []
        for i in range(8):
            column = []
            for j in range(8):
                column.append(pg.Rect(
                    SQUARE_LENGTHS[i], SQUARE_LENGTHS[j],
                    SQUARE_LENGTH, SQUARE_LENGTH
                ))
            boardSq.append(column)
        self.rects = boardSq

        # orientation of the board, add functionality later
        self.whiteOnBottom = True
    
    # method to convert string coordinates (ex. "a1") to indices 
    def strToIndices(self, coords) -> tuple:
        file = ord(coords[0])
        rank = int(coords[1])

        # assert that the coordinates are legal
        unicode_a = ord('a')
        assert(unicode_a <= file <= ord('h'))
        assert(1 <= rank <= 8)
        
        # all coords go from 0-7
        if self.whiteOnBottom: 
            return (file - unicode_a, 8 - rank)
        else:
            return (7 - file + unicode_a, rank - 1)

    # method to convert indices to string coordinates
    def indicesToStr(self, x, y) -> str:
        # assert that the coordinates are legal
        assert(0 <= x <= 7)
        assert(0 <= y <= 7)

        unicode_a = ord('a')
        if self.whiteOnBottom:
            return chr(unicode_a + x) + str(8 - y)
        else:
            return chr(unicode_a + 7 - x) + str(y + 1)

    # method to flip the screen (e.g. white on bottom -> black on bottom)
    # modifies pieceMap, updating both the keys and the pieces
    def flipBoard(self):
        self.whiteOnBottom = not self.whiteOnBottom
        newPieceMap = {}
        for key in self.pieceMap:
            newKey = (7 - key[0], 7 - key[1])
            piece = self.pieceMap[key]
            piece.update(newKey[0], newKey[1])
            newPieceMap[newKey] = piece
        self.pieceMap = newPieceMap


    
    # Assumes that all moves are legal.
    # Takes in two string coordinates ("ex. a5, b2") and executes
    # the given move on the board, updating the positions of the pieces.
    def movePiece(self, startSquare, endSquare, isPromotion=False,
                  isCastling=False, isEnPassant=False):
        startIndices = self.strToIndices(startSquare)
        endIndices = self.strToIndices(endSquare)
        piece = self.pieceMap[startIndices]
        piece.update(endIndices[0], endIndices[1])
        self.pieceMap[endIndices] = piece
        del self.pieceMap[startIndices]

# a bit of testing code
def main():
    testBoard = DisplayBoard(DEFAULT_FENSTRING)
    print(testBoard.pieceMap)
    testBoard.movePiece("e2", "e4")
    print(testBoard.pieceMap)
    testBoard.movePiece("a1", "a8")
    print(testBoard.pieceMap)
    return 0

if __name__ == "__main__":
    main()