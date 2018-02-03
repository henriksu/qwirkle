import pygame, sys
from pygame.locals import *
from qwirkle.game import *
from qwirkle.tile import *
from qwirkle.board import *
from builtins import range

FPS = 144 # frames per second, the general speed of the program
WINDOWWIDTH = 1080 # size of window's width in pixels
WINDOWHEIGHT = 720 # size of windows' height in pixels
#WINDOWWIDTH = 640 # size of window's width in pixels
#WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 50 # size of box height & width in pixels
GAPSIZE = 5 # size of gap between boxes in pixels
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
BLACK    = (  0,   0,   0)

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
    global FPSCLOCK, DISPLAYSURF, BASICFONT, MOVE_SURF, MOVE_RECT
    
    pygame.init()
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    BUTTONCOLOR = WHITE
    BUTTONCOLOR_HOVER = BLACK
    BUTTONTEXTCOLOR = BLACK
    BUTTONTEXTCOLOR_HOVER = GRAY
    MESSAGECOLOR = WHITE
    TEXTCOLOR = BLACK
    BASICFONTSIZE = 20
    
    #Buttons
    MOVE_SURF, MOVE_RECT = makeText('End Move', BUTTONTEXTCOLOR, BUTTONTEXTCOLOR, WINDOWWIDTH - 150, WINDOWHEIGHT - 75)
    REGRET_SURF, REGRET_RECT = makeText('Regret', BUTTONTEXTCOLOR, BUTTONCOLOR, WINDOWWIDTH - 150, WINDOWHEIGHT - 50)
    SWAP_SURF, SWAP_RECT = makeText('Swap', BUTTONTEXTCOLOR, BUTTONCOLOR, WINDOWWIDTH - 150, WINDOWHEIGHT - 25)

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Qwirkle')
    
    game = Game.make_new_game(4, 42)   
    mainBoard = game.board.tiles
    
    currentSelectedTiles = []
    currentPlacedTiles = []

    DISPLAYSURF.fill(BGCOLOR)    
    
    while True: # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        
        #Update the Statistics
        playernr = 1
        for player in game.players:
            scoreText = 'Player ' + str(playernr) + ': ' + str(player.total_score())
            if player == game.current_player:
                txtColor = GREEN
            else:
                txtColor = TEXTCOLOR
            
            SCORE_SURF, SCORE_RECT = makeText(scoreText, txtColor, MESSAGECOLOR, WINDOWWIDTH - 125, 25 * playernr)
            DISPLAYSURF.blit(SCORE_SURF, SCORE_RECT) #Draw statistics of names and scores on top right corner
            playernr += 1
    
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        
        #Update the current hand of the current player
        currentHand = game.current_player.hand.tiles
                
        #Draw the player hand area
        boxx = WINDOWWIDTH/2 - (BOXSIZE*3 + GAPSIZE*4)
        boxy = WINDOWHEIGHT - BOXSIZE*1.1 - GAPSIZE
        pygame.draw.rect(DISPLAYSURF,WHITE, (boxx, boxy, (BOXSIZE+GAPSIZE)*6+ GAPSIZE, BOXSIZE*2))
        
        #Highlight the hand tile the mouse is hovering over and select if mousebutton is selected
        hoverTile = getHandTileAtPixel(mousex, mousey, currentHand)
        tileSelected = False
        if mouseClicked:
            if hoverTile != None:
                for tile, x, y in currentSelectedTiles:
                    if hoverTile == (tile, x, y):
                        tileSelected = True
                        currentSelectedTiles.remove((tile, x, y))
                if not tileSelected:
                        currentSelectedTiles.append(hoverTile)
        
        #Highlight the currently selected tile in the hand
        if currentSelectedTiles:
            for tile, x, y in currentSelectedTiles:
                pygame.draw.rect(DISPLAYSURF,BLUE, (x - GAPSIZE/2, y - GAPSIZE/2, BOXSIZE + GAPSIZE, BOXSIZE + GAPSIZE))
        
        #Draw the player hand
        space = 0
        for tile in currentHand:
            x = WINDOWWIDTH/2 - (BOXSIZE+GAPSIZE)*3 + space
            y = WINDOWHEIGHT - BOXSIZE*1.1
            drawTile(tile, x, y, BOXSIZE)            
            space = space + BOXSIZE + GAPSIZE
        
        #Hide the currently placed tiles from the hand
        for pos, (currentPlacedTile, x, y) in currentPlacedTiles:
            space = 0
            for tile in currentHand:
                if tile == currentPlacedTile:
                    x = WINDOWWIDTH/2 - (BOXSIZE+GAPSIZE)*3 + space
                    y = WINDOWHEIGHT - BOXSIZE*1.1
                    pygame.draw.rect(DISPLAYSURF,WHITE, (x, y, BOXSIZE, BOXSIZE)) 
                space = space + BOXSIZE + GAPSIZE    
        
        #Draw the board
        for pos, tile in mainBoard:
            tilex, tiley = pos
            drawBoardTile(tile, tilex, tiley)
            
        #Highlight the possible next move when mouse is hovering over it and mark it as possible move
        possibleMove = False
        if not mainBoard and not currentPlacedTiles: #if there are no Tiles in mainBoard yet, highlight the first possible move
            x = WINDOWWIDTH/2 - BOXSIZE/2 
            y = WINDOWHEIGHT/2 - BOXSIZE/2
            boxRect = pygame.Rect(x, y, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(mousex, mousey):
                possibleMove = True        
                pygame.draw.rect(DISPLAYSURF,WHITE, (x, y, BOXSIZE, BOXSIZE))
        else:
            #Check if there is an empty tile spot next to a real tile
            boxx, boxy = getTileAtPixel(mousex, mousey)
            
            if boxx != None:
                if currentPlacedTiles:
                    for pos, placedTile in  currentPlacedTiles:
                        if pos == (boxx, boxy):
                            possibleMove = False
                            break
                        elif pos[0] == boxx and pos[1] == boxy+1:
                            possibleMove = True
                        elif pos[0] == boxx and pos[1] == boxy-1:
                            possibleMove = True
                        elif pos[0] == boxx+1 and pos[1] == boxy:
                            possibleMove = True
                        elif pos[0] == boxx-1 and pos[1] == boxy:
                            possibleMove = True
                else:
                    for pos, tile in mainBoard:
                        if pos == (boxx, boxy):
                            possibleMove = False
                            break
                        elif pos[0] == boxx and pos[1] == boxy+1:
                            possibleMove = True
                        elif pos[0] == boxx and pos[1] == boxy-1:
                            possibleMove = True
                        elif pos[0] == boxx+1 and pos[1] == boxy:
                            possibleMove = True
                        elif pos[0] == boxx-1 and pos[1] == boxy:
                            possibleMove = True
                
                
                if possibleMove:
                    x = WINDOWWIDTH/2 - BOXSIZE/2 + boxx*BOXSIZE + boxx*GAPSIZE
                    y = WINDOWHEIGHT/2 - BOXSIZE/2 + boxy*BOXSIZE + boxy*GAPSIZE
                    if y < (WINDOWHEIGHT - BOXSIZE*3):  #This is so that it is not possible to make a move 
                                                        #across the hadn area
                        pygame.draw.rect(DISPLAYSURF,WHITE, (x, y, BOXSIZE, BOXSIZE))
            
        #if a possible move is selected, and a tile is selected, draw the current tile there
        if possibleMove and mouseClicked and currentSelectedTiles:
            for tile, x, y in currentSelectedTiles:
                currentPlacedTiles.append([getTileAtPixel(mousex, mousey), (tile, x, y)])
                currentSelectedTiles.remove((tile, x, y))
                break
                
            
        if currentPlacedTiles:
            for (tilex, tiley), (tile, x, y)  in currentPlacedTiles:
                #This is to highlight the newly placed tile
                x, y = leftTopCoordsOfBox(tilex, tiley)
                pygame.draw.rect(DISPLAYSURF,YELLOW, (x - GAPSIZE/2 , y - GAPSIZE/2, BOXSIZE + GAPSIZE, BOXSIZE + GAPSIZE)) #Draw the highlight around the tile
                drawBoardTile(tile, tilex,  tiley) #Draw the actual tile
                    
            
        #Draw current player name by the hand selection
        
        #Draw buttons
        DISPLAYSURF.blit(MOVE_SURF, MOVE_RECT)
        
        #Highlight button if mouse is over it
        if MOVE_RECT.collidepoint(mousex, mousey):
            moveButtonTextColor = BUTTONTEXTCOLOR_HOVER
            moveButtonColor = BUTTONCOLOR_HOVER
        else:
            moveButtonTextColor = BUTTONTEXTCOLOR
            moveButtonColor = BUTTONCOLOR 
        
        if REGRET_RECT.collidepoint(mousex, mousey):
            regretButtonTextColor = BUTTONTEXTCOLOR_HOVER
            regretButtonColor = BUTTONCOLOR_HOVER
        else:
            regretButtonTextColor = BUTTONTEXTCOLOR
            regretButtonColor = BUTTONCOLOR 
            
        if SWAP_RECT.collidepoint(mousex, mousey):
            swapButtonTextColor = BUTTONTEXTCOLOR_HOVER
            swapButtonColor = BUTTONCOLOR_HOVER
        else:
            swapButtonTextColor = BUTTONTEXTCOLOR
            swapButtonColor = BUTTONCOLOR 
        
        
        #Update Buttons
        MOVE_SURF, MOVE_RECT = makeText('End Move', moveButtonTextColor, moveButtonColor, WINDOWWIDTH - 150, WINDOWHEIGHT - 75)
        REGRET_SURF, REGRET_RECT = makeText('Regret', regretButtonTextColor, regretButtonColor, WINDOWWIDTH - 150, WINDOWHEIGHT - 50)
        SWAP_SURF, SWAP_RECT = makeText('Swap', swapButtonTextColor, swapButtonColor, WINDOWWIDTH - 150, WINDOWHEIGHT - 25)
        
        #Draw Buttons
        DISPLAYSURF.blit(MOVE_SURF, MOVE_RECT)
        DISPLAYSURF.blit(REGRET_SURF, REGRET_RECT)
        DISPLAYSURF.blit(SWAP_SURF, SWAP_RECT)
       
        
        #Swap selected tile when pressing on SWAP button
        if SWAP_RECT.collidepoint(mousex, mousey) and mouseClicked and currentSelectedTiles:
            tiles = []
            for tile, x, y in currentSelectedTiles:
                tiles.append(tile)
            game.exchange_tiles(tiles)
            currentSelectedTiles = []
        
        #Empty the currentPlacedTiles list when you press Regret
        if REGRET_RECT.collidepoint(mousex, mousey) and mouseClicked and currentPlacedTiles:
            currentPlacedTiles = []
            currentSelectedTiles = []
        
        #Finish the move when pressing on MOVE button
        tiles_and_positions = []
        if MOVE_RECT.collidepoint(mousex, mousey) and mouseClicked:
            if currentPlacedTiles:
                for (tilex, tiley), (tile, x, y)  in currentPlacedTiles:
                    tiles_and_positions.append([Position(tilex, tiley), tile])
                try:
                    game.make_move(tiles_and_positions)
                except ValueError:
                    pass
                currentPlacedTiles = []
                currentSelectedTiles = []
                
        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawBoardTile(tile, tilex, tiley): #new method to use on board instead of just drawTile
    x = WINDOWWIDTH/2 - BOXSIZE/2 + tilex*BOXSIZE + tilex*GAPSIZE
    y = WINDOWHEIGHT/2 - BOXSIZE/2 + tiley*BOXSIZE + tiley*GAPSIZE
    drawTile(tile, x, y, BOXSIZE)
         
def drawTile(tile, x, y, size):
    color_code = TILE_COLOR_CODE[tile.color]
    shape_code = tile.shape
    pygame.draw.rect(DISPLAYSURF,BLACK, (x, y, size, size))
    
    shapex = x + size/4
    shapey = y + size/4
    shapeSize = size/2
   
    if shape_code == Shape.CIRCLE:
        pygame.draw.circle(DISPLAYSURF, color_code, (int(x + size/2), int(y + size/2)), int(size/4))
    
    elif shape_code == Shape.X:
        pygame.draw.line(DISPLAYSURF, color_code, (shapex, shapey), (shapex + shapeSize, shapey + shapeSize), 5)
        pygame.draw.line(DISPLAYSURF, color_code, (shapex, shapey + shapeSize), (shapex + shapeSize, shapey), 5)
    
    elif shape_code == Shape.DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color_code, ((shapex, shapey + size/4),
                                                      (shapex + size/4, shapey),
                                                      (shapex + size/2, shapey + size/4),
                                                      (shapex + size/4, shapey + size/2)))
    
    elif shape_code == Shape.SQUARE:
        pygame.draw.rect(DISPLAYSURF,color_code, (shapex, shapey, shapeSize, shapeSize))
        
    elif shape_code == Shape.STAR:
        num_points = 4
        point_list = []
        center_x = x + size/2
        center_y = y + size/2
        for i in range(num_points * 2):
                radius = size/4
                if i % 2 == 0:
                        radius = radius // 2
                ang = i * 3.14159 / num_points + 10 * 3.14159 / 60
                x = center_x + int(math.cos(ang) * radius)
                y = center_y + int(math.sin(ang) * radius)
                point_list.append((x, y))
        pygame.draw.polygon(DISPLAYSURF, color_code, point_list)
        
    elif shape_code == Shape.CLOVER:
        pygame.draw.circle(DISPLAYSURF, color_code, ((int(shapex), int(shapey + size/4))), int(size/6))
        pygame.draw.circle(DISPLAYSURF, color_code, ((int(shapex + size/4), int(shapey))), int(size/6))
        pygame.draw.circle(DISPLAYSURF, color_code, ((int(shapex + size/2), int(shapey + size/4))), int(size/6))
        pygame.draw.circle(DISPLAYSURF, color_code, ((int(shapex + size/4), int(shapey + size/2))), int(size/6))
        pygame.draw.circle(DISPLAYSURF, color_code, ((int(shapex + size/4), int(shapey + size/4))), int(size/6))
    
def getHandTileAtPixel(x, y, hand):
    space = 0
    for tile in hand:
        boxx = WINDOWWIDTH/2 - (BOXSIZE+GAPSIZE)*3 + space
        boxy = WINDOWHEIGHT - BOXSIZE*1.1
        boxRect = pygame.Rect(boxx, boxy, BOXSIZE, BOXSIZE)
        if boxRect.collidepoint(x, y):
            pygame.draw.rect(DISPLAYSURF,BLACK, (boxx - GAPSIZE/2, boxy - GAPSIZE/2, BOXSIZE + GAPSIZE, BOXSIZE + GAPSIZE))  
            return tile, boxx, boxy
        space = space + BOXSIZE+GAPSIZE 
    return None

def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + WINDOWWIDTH/2 - BOXSIZE/2
    top = boxy * (BOXSIZE + GAPSIZE) + WINDOWHEIGHT/2 - BOXSIZE/2
    return (left, top)
   
def getTileAtPixel(x, y):
    for boxx in range(-100, 100):
        for boxy in range(-100, 100):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

if __name__ == '__main__':
    main()