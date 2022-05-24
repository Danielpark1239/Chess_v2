import pygame as pg
from constants import *
from displayBoard import DisplayBoard
import chess
import chess.engine

class Game:
    def __init__(self, FENstring=DEFAULT_FENSTRING):
        self.running = False
        self.width = GAME_WIDTH
        self.height = GAME_HEIGHT
        self.window = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.displayBoard = DisplayBoard(FENstring)
        self.board = chess.Board(FENstring)
        self.heldPiece = None
        self.heldPieceX = None # board indices of the held piece
        self.heldPieceY = None
        self.turn = True # True for white, False for black
    
    # helper function that returns the indices of the board square 
    # at the coordinates x, y. Assumes that the coordinates are inside
    # the board.
    def getSquareIndices(self, x, y) -> tuple:
        # UNIVERSAL convention: top left is (0,0), top middle is (4,0), bottom
        # right is (7,7)
        return ((x // SQUARE_LENGTH) - 1, (y // SQUARE_LENGTH) - 1)

    # return the piece to its original square
    def returnPiece(self):
        self.heldPiece.update(self.heldPieceX, self.heldPieceY)
        self.heldPiece = None
        self.heldPieceX = None
        self.heldPieceY = None
    
    def checkEvents(self):
        # have stockfish make a move
        if (self.turn == False):
            result = self.engine.play(self.board, chess.engine.Limit(time=1))
            self.board.push(result.move)
            move = result.move.uci()
            self.displayBoard.movePiece(move[0:2], move[2:4])
            self.turn = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()

            # while testing: keydown flips the board
            if event.type == pg.KEYDOWN:
                self.displayBoard.flipBoard()
            
            # can be used to: pick up a piece, place down a piece at a diff sq,
            # place down a piece at the same square (if invalid),
            # interact with menus if outside the board
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                # mouse is inside the board
                if (x >= SQUARE_LENGTHS[0] and 
                    x <= SQUARE_LENGTHS[7] + SQUARE_LENGTH):
                    squareIndices = self.getSquareIndices(x, y)
                    
                    # pick up a piece if none held
                    if self.heldPiece == None:
                        # piece exists
                        if squareIndices in self.displayBoard.pieceMap:
                            piece = self.displayBoard.pieceMap[squareIndices]
                            # it's your turn and your color piece
                            if self.turn and piece.isWhite() == self.player:
                                self.heldPiece = piece
                                self.heldPieceX = squareIndices[0]
                                self.heldPieceY = squareIndices[1]
                    
                    # if a piece is held, either:
                    else:
                        startCoords = self.displayBoard.indicesToStr(
                            self.heldPieceX, self.heldPieceY)
                        endCoords = self.displayBoard.indicesToStr(
                            squareIndices[0], squareIndices[1])

                        # if startSq = endSq, put down the piece
                        if startCoords != endCoords:
                            move = chess.Move.from_uci(startCoords + endCoords)
                            # play a move if destination square is valid
                            if move in self.board.legal_moves:
                                self.heldPiece = None
                                self.heldPieceX = None
                                self.heldPiceY = None
                                self.displayBoard.movePiece(startCoords, endCoords)
                                self.board.push(move)
                                self.turn = False
                            else:
                                self.returnPiece()

                        # put down the piece otherwise
                        else:
                            self.returnPiece()
            
            # if a piece is held, it moves with the mouse cursor
            if event.type == pg.MOUSEMOTION:
                if (self.heldPiece != None):
                    x, y = pg.mouse.get_pos()
                    self.heldPiece.updateRect(x, y)
                        

# Run the game against a computer
class OnePlayer(Game):
    def __init__(self, difficulty):
        super().__init__()
        pg.display.set_caption("1p Chess Game")
        self.running = True

        # game logic board
        self.player = True # True for white, False for black

        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        self.engineMove = None


    # game loop
    def runGame(self):

        while self.running:
            # check events
            self.checkEvents()
    
            # draw background
            self.window.fill((32, 32, 32))
            # draw board
            for i in range(8):
                for j in range(8):
                    if i % 2 == j % 2:
                        pg.draw.rect(self.window, 
                                     LIGHT_GRAY, 
                                     self.displayBoard.rects[i][j])
                    else:
                        pg.draw.rect(self.window,
                                     LIGHT_BLUE,
                                     self.displayBoard.rects[i][j])
            
            # draw piece sprites
            pieceList = list(self.displayBoard.pieceMap.values())
            boardPieces = pg.sprite.Group(pieceList)
            boardPieces.draw(self.window)

            pg.display.update()
            self.clock.tick(FPS)
        return 0