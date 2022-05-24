from piece import Piece

class FENreader:
    def __init__(self, FENstring):
        squares = []
        files = [0,1,2,3,4,5,6,7]
        for i in range(8):
            squares.append(files)

        # squares is a 2D array of [ranks, [files]]
        counter = 0
        index = 0
        pieces = []
        castlingList = []

        # read pieces
        for i in range(len(FENstring)):
            if counter == 64:
                self.pieces = pieces
                index = i + 1
                break

            if counter < 64:
                pieceChar = FENstring[i]
                match pieceChar:
                    case ("r"|"R"|"n"|"N"|"b"|"B"|"k"|"K"|"q"|"Q"|"p"|"P"):
                        piece = Piece(counter%8, counter//8, pieceChar)
                        pieces.append(piece)
                        counter += 1

                    case "/":
                        assert(counter % 8 == 0)

                    case _: #a number
                        counter += int(pieceChar)

        # read player turn
        self.turn = FENstring[index]
        index += 2
        
        # read castling rights
        substring = FENstring[index:]
        for i in range(len(substring)):
            match substring[i]:
                case " ":
                    self.castling = castlingList
                    index += i + 1
                    break

                case _:
                    castlingList.append(substring[i])
        
        # read en passant rights
        substring = FENstring[index:]
        for i in range(len(substring)):
            match substring[i]:
                # no pawns can be en passanted
                case "-":
                    self.enPassant = "-"
                    index += 2
                    break
                # two chars describing a square
                case _:
                    self.enPassant = substring[i:i + 2]
                    index += 3
                    break
                
        # read halfmove clock
        substring = FENstring[index:]
        endIndex = 0
        for i in range(len(substring)):
            if substring[i] == " ":
                endIndex = i
                self.halfMoves = int(substring[:endIndex])
                index += i + 1
            
        # read fullmove number
        self.fullMoves = int(FENstring[index:])

    # returns a list of pieces parsed from the FEN string
    def getPieces(self) -> list:
        return self.pieces
    
    # keeps track of player turns; can be "w"(white) or "b"(black), 
    # depending on who can play the next move.
    def getTurn(self) -> str:
        return self.turn
    
    # keeps track of who can castle:
    # "K" and "Q" for white's kingside and queenside respectively,
    # "k" and "q" for black
    def getCastling(self) -> list:
        return self.castling
    
    # keeps track of a square on which a pawn that moved two spaces
    # can be captured. Non-empty even if the move cannot be played.
    def getEnPassant(self) -> str:
        return self.enPassant

    # keeps track of the number of halfmoves (moves without any
    # pawn moves or captures). If it reaches 100, the game is drawn.
    def getHalfMoves(self) -> int:
        return self.halfMoves 

    # keeps track of the number of full moves that have been played.
    def getFullMoves(self)  -> int:
        return self.fullMoves  




                



        



    
        


 
    
