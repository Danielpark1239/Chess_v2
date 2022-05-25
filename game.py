import pygame as pg
import pygame_menu as pgm
import menus
from constants import *
from displayBoard import DisplayBoard
import chess
import chess.engine

#debugging
import random

class Game:
    def __init__(self, FENstring=DEFAULT_FENSTRING):
        self.running = False
        self.playing = False
        self.width = GAME_WIDTH
        self.height = GAME_HEIGHT
        self.window = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.displayBoard = DisplayBoard(FENstring)
        self.board = chess.Board(FENstring)
        self.heldPiece = None
        self.heldPieceX = None # board indices of the held piece
        self.heldPieceY = None

        self.gui = menus.GameGUI() # Game GUI

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
    
    # play the legal move, updating display, board, and state variables
    def playMove(self, move):
        # Indicators for special rules
        castling, enPassant = False, False
        if self.board.is_castling(move):
            castling = True
        if self.board.is_en_passant(move):
            enPassant = True
        promotion = move.uci()[4:]

        # push the move to the board
        self.board.push(move)

        # update display
        uci = move.uci()
        self.displayBoard.movePiece(
            uci[0:2], uci[2:4], promotion, castling, enPassant
        )

    # given a psuedo-legal player move, generate the move, displaying
    # a promotion menu if necessary.
    def generatePlayerMove(self,startCoords, endCoords):
        promotionMove = chess.Move.from_uci(startCoords+endCoords+"q")

        # if the promotion is legal, display the menu and get player input
        if promotionMove in self.board.legal_moves:
            promotedPiece = None
            startIndices = self.displayBoard.strToIndices(startCoords)
            endIndices = self.displayBoard.strToIndices(endCoords)

            # Set up a menu for user input
            promotion_menu = menus.PromotionMenu(
                endIndices, 
                self.displayBoard.pieceMap[startIndices].isWhite()
            )
            while (promotion_menu.menu.is_enabled()):
                # get mouse bounds
                xPos = SQUARE_CENTERS[endIndices[0]]
                yPos = SQUARE_CENTERS[endIndices[1]]

                # check for mouse movement
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        x, y = pg.mouse.get_pos()
                        if x < xPos and y < yPos:
                            promotedPiece = "q" # Queen                            
                        elif x > xPos and y < yPos:
                            promotedPiece = "r" # Rook
                        elif x < xPos and y > yPos:
                            promotedPiece = "b" # Bishop
                        elif x > xPos and y > yPos:
                            promotedPiece = "n" # Knight

                promotion_menu.menu.draw(pg.display.get_surface())
                pg.display.update()
                pg.time.Clock().tick(FPS)

                if (promotedPiece is not None):
                    promotion_menu.menu.disable()
            return chess.Move.from_uci(startCoords+endCoords+promotedPiece)

        # if the move is not a promotion, generate a normal UCI
        return chess.Move.from_uci(startCoords + endCoords)
    
    def checkEvents(self):
        # Computer turn
        if (self.turn == False):
            # DEBUGGING: make random moves
            if (self.debug is True):
                self.playMove(
                    random.choice([move for move in self.board.legal_moves])
                )
            # have stockfish make a move
            else:
                result = self.engine.play(
                    self.board, 
                    chess.engine.Limit(time=ENGINE_THINKING_TIME)
                )
                self.playMove(result.move)
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

                        # if the squares are distinct, 
                        if startCoords != endCoords:
                            # generate a move and play it if it's valid
                            move = self.generatePlayerMove(startCoords, endCoords)
                            if move in self.board.legal_moves:
                                self.heldPiece = None
                                self.heldPieceX = None
                                self.heldPiceY = None
                                self.playMove(move)
                                self.turn = False
                            else:
                                self.returnPiece()

                        # put down the piece otherwise
                        else:
                            self.returnPiece()
            
            # if a piece is held, it moves with the mouse cursor
            if event.type == pg.MOUSEMOTION:
                if self.heldPiece is not None:
                    x, y = pg.mouse.get_pos()
                    self.heldPiece.updateRect(x, y)

    # Check if the game terminated
    def checkTermination(self):
        outcome = self.board.outcome()
        if outcome is not None:
            winner = outcome.winner
            if (winner is False):
                print("Black won the game!")
            elif (winner is True):
                print("White won the game!")
            elif (winner is None):
                print("The game ended in a draw!")
            self.playing = False
            self.running = False # For now: exits to menu once game terminates

# Run the game against a computer
class OnePlayer(Game):
    def __init__(self, difficulty, FENstring, startColor):
        super().__init__(FENstring=FENstring)
        pg.display.set_caption("1p Chess Game")
        self.running = True
        self.playing = True
        self.player = startColor # True if the player is white, False for black
        if (self.player):
            self.turn = True # True if it's the player's turn
        else:
            self.turn = False # False if it's the computer's turn
            self.displayBoard.flipBoard()

        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        self.engine.configure({
            "UCI_LimitStrength": True,
            "UCI_Elo": difficulty
        })
        self.difficulty = difficulty
        self.debug = ONE_PLAYER_DEBUG # if true, computer plays random moves

        self.gui.menu.add.button(title="Main menu", action=pgm.events.EXIT)
    
    def resetGame(self):
        self.playing = False
    
    def resetToMenu(self):
        self.playing = False
        self.running = False
        self.gui.menu.disable()

    # game loop
    def runGame(self):
        while self.running:
            

            while self.playing:
                # check events
                self.checkEvents()

                # check termination
                self.checkTermination()

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

                # update GUI
                self.gui.menu.draw(self.window)

                pg.display.update()
                self.clock.tick(FPS)


