import pygame as p
from Assets import Engine

WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
CHESSCOMWHITE = (238, 238, 210)
CHESSCOMGREEN = (118, 150, 86)
CHESSCOMYELLOW = (186,202,43)

MAX_FPS = 30
IMAGES = {}

#Load in images as a global dictionary
def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR", "bp", "bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("../resources/Pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

#main game loop
def main():
    p.init()
    p.display.set_caption('Chess')
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = Engine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    sqMovedTo = ()
    sqFrom = ()
    sqClicked = ()
    while running:

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                p.quit()
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                file = location[0] // SQ_SIZE
                rank = location[1] // SQ_SIZE
                if sqSelected == (rank, file):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (rank, file)
                    playerClicks.append(sqSelected)
                    if gs.board[sqSelected[0]][sqSelected[1]] != "--":
                        sqClicked = sqSelected
                if len(playerClicks) == 2:
                    move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getAlgebraicNotation() + " (" + move.getSquareNotation()+ ")")

                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True

                    if move.pieceMoved != "--":
                        #gs.makeMove(move)
                        sqMovedTo = playerClicks[1]
                        sqFrom = playerClicks[0]
                    sqSelected = ()
                    playerClicks = []

            elif e.type == p.KEYDOWN:
                key = p.key.get_pressed()
                if key[p.K_r]:
                    gs = Engine.GameState()
                    print("Game restarted! ")
                    sqMovedTo = ()
                    sqFrom = ()
                    sqClicked = ()
                if key[p.K_LEFT]:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False


        drawGameState(screen, gs, CHESSCOMWHITE, CHESSCOMGREEN, sqFrom, sqMovedTo, sqClicked)
        clock.tick(MAX_FPS)
        p.display.flip()


#Responsible for all graphics within a current game state
def drawGameState(screen, gs, lightColour, darkColour, sqFrom, sqMovedTo, sqClicked):
    drawBoard(screen, lightColour, darkColour)
    drawHighlight(screen, CHESSCOMYELLOW, sqFrom, sqMovedTo, sqClicked)
    drawPieces(screen, gs.board)


#draws the squares on the board
def drawBoard(screen, lightColour, darkColour):
    colours = [lightColour, darkColour]
    for rank in range(DIMENSION):
        for file in range(DIMENSION):
            colour = colours[((rank+file)%2)]
            p.draw.rect(screen, colour, p.Rect(file*SQ_SIZE, rank*SQ_SIZE, SQ_SIZE, SQ_SIZE))


#draw pieces on the board
def drawPieces(screen, board):
    for rank in range(DIMENSION):
        for file in range(DIMENSION):
            piece = board[rank][file]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(file*SQ_SIZE, rank*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawHighlight(screen, colour, sqFrom, sqMovedTo, sqClicked):
    if len(sqFrom) != 0:
        p.draw.rect(screen, colour, p.Rect(sqFrom[1] * SQ_SIZE, sqFrom[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if len(sqMovedTo) != 0:
        p.draw.rect(screen, colour, p.Rect(sqMovedTo[1] * SQ_SIZE, sqMovedTo[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if len(sqClicked) != 0:
        p.draw.rect(screen, colour, p.Rect(sqClicked[1] * SQ_SIZE, sqClicked[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))



if __name__ == "__main__":
    main()


















main()