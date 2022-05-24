from tracemalloc import start
from piece import Piece
import pygame_menu as pgm
import menus
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

        # orientation of the board
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
    # Takes in two string coordinates ("ex. a5, b2") and special move
    # indicators and executes the given move on the board, 
    # updating the positions of the pieces.
    def movePiece(self, startSquare, endSquare, 
                  isPromotion, isCastling, isEnPassant):
        startIndices = self.strToIndices(startSquare)
        endIndices = self.strToIndices(endSquare)

        # Move is a pawn promotion
        if (isPromotion != ""):
            # Handle the promotion 
            piece = self.pieceMap[startIndices]
            piece.promote(isPromotion)
            piece.update(endIndices[0], endIndices[1])
            self.pieceMap[endIndices] = piece
            del self.pieceMap[startIndices]

        # Move is castling
        elif (isCastling):
            king = self.pieceMap[startIndices]
            del self.pieceMap[startIndices]
            # king is castling right
            if (startIndices[0] < endIndices[0]):
                king.update(startIndices[0] + 2, startIndices[1])
                self.pieceMap[(startIndices[0] + 2, startIndices[1])] = king
                rook = self.pieceMap[(7, startIndices[1])]
                del self.pieceMap[(7, startIndices[1])]
                rook.update(endIndices[0] - 1, startIndices[1])
                self.pieceMap[(endIndices[0] - 1, startIndices[1])] = rook
                
            # king is castling left
            else:
                king.update(startIndices[0] - 2, startIndices[1])
                self.pieceMap[(startIndices[0] - 2, startIndices[1])] = king
                rook = self.pieceMap[(0, startIndices[1])]
                del self.pieceMap[(0, startIndices[1])]

                rook.update(endIndices[0] + 1, startIndices[1])
                self.pieceMap[(endIndices[0] + 1, startIndices[1])] = rook

        # Move is en passant
        elif (isEnPassant):
            # assert that target square is empty
            assert(endIndices not in self.pieceMap)

            pawn = self.pieceMap[startIndices]
            pawn.update(endIndices[0], endIndices[1])

            # delete captured pawn
            if (endIndices[0] < startIndices[0]):
                del self.pieceMap[(startIndices[0] - 1, startIndices[1])]
            else:
                del self.pieceMap[(startIndices[0] + 1, startIndices[1])]

            self.pieceMap[endIndices] = pawn
            del self.pieceMap[startIndices]

        # Move is a normal move
        else:
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