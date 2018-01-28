import pygame, sys
from pygame.locals import *
from qwirkle.game import *
from qwirkle.tile import *
from qwirkle.board import *

FPS = 144 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 10 # number of columns of icons
BOARDHEIGHT = 7 # number of rows of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

TILE_COLOR_CODE = {
    Color.RED: RED,
    Color.ORANGE: ORANGE,
    Color.YELLOW: YELLOW,
    Color.GREEN: GREEN,
    Color.BLUE: BLUE,
    Color.PURPLE: PURPLE}

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

CIRCLE = 'circle'
X = 'X'
DIAMOND = 'diamond'
SQUARE = 'square'
STAR = 'star'
CLOVER = 'clover'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (CIRCLE, X, DIAMOND, SQUARE, STAR, CLOVER)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Memory Game')
    
    game = Game.make_new_game(1, 42)   
    mainBoard = game.board.tiles
    currentHand = game.current_player.hand.tiles

    DISPLAYSURF.fill(BGCOLOR)
    
    #for testing
    tiles_and_positions = [(Position(0, 0),
                               Tile(Color.RED, Shape.CLOVER))]
    game.make_move(tiles_and_positions)
    
    while True: # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the window

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                
        
        #Draw the hand tile the mouse is hovering over
        getHandTileAtPixel(mousex, mousey, currentHand)    
        
        #Draw the player hand
        space = 0
        for tile in currentHand:
            color_code = TILE_COLOR_CODE[tile.color]
            boxx = WINDOWWIDTH/2 - (BOXSIZE+GAPSIZE)*3 + space
            boxy = WINDOWHEIGHT - BOXSIZE*1.5
            drawTile(color_code, boxx, boxy, BOXSIZE)            
            space = space + 60
        
        #Draw the board
        for pos, tile in mainBoard:
            color_code = TILE_COLOR_CODE[tile.color]
            boxx = WINDOWWIDTH/2 - BOXSIZE/2 + pos.x*BOXSIZE + pos.x*GAPSIZE
            boxy = WINDOWHEIGHT/2 - BOXSIZE/2 + pos.y*BOXSIZE + pos.y*GAPSIZE
            drawTile(color_code, boxx, boxy, BOXSIZE)
            
        
        
        #pygame.draw.rect(DISPLAYSURF,WHITE, (mousex, mousey, 50, 50))
        
        
        
        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)
         
def drawTile(color, x, y, size):
    pygame.draw.rect(DISPLAYSURF,color, (x, y, size, size))
    #pygame.draw.
    
def getHandTileAtPixel(x, y, hand):
    space = 0
    for tile in hand:
        boxx = WINDOWWIDTH/2 - (BOXSIZE+GAPSIZE)*3 + space
        boxy = WINDOWHEIGHT - BOXSIZE*1.5
        boxRect = pygame.Rect(boxx, boxy, BOXSIZE, BOXSIZE)
        if boxRect.collidepoint(x, y):
            drawTile(WHITE, boxx - GAPSIZE/2, boxy - GAPSIZE/2, BOXSIZE + GAPSIZE)  
            return (boxx, boxy)
        space = space + 60 
    return (None, None)
    
if __name__ == '__main__':
    main()