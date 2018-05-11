import sys

import pygame
from pygame.locals import *
from qwirkle.game_logic.game import *
from qwirkle.game_logic.tile import *
from qwirkle.game_logic.board import *
from qwirkle.gui.color_palette import (
    BGCOLOR, LIGHTBGCOLOR, BOXCOLOR, HIGHLIGHTCOLOR,
    BUTTONCOLOR, BUTTONCOLOR_HOVER, BUTTONTEXTCOLOR, BUTTONTEXTCOLOR_HOVER,
    MESSAGECOLOR, TEXTCOLOR, ALLCOLORS, WHITE, GREEN, BLACK, BLUE, YELLOW)
from qwirkle.gui.tile_art import TileDrawer

FPS = 144  # frames per second, the general speed of the program
WINDOWWIDTH = 1080  # size of window's width in pixels
WINDOWHEIGHT = 720  # size of windows' height in pixels
# WINDOWWIDTH = 640 # size of window's width in pixels
# WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8  # speed boxes' sliding reveals and covers
BOXSIZE = 50  # size of box height & width in pixels
GAPSIZE = 5  # size of gap between boxes in pixels
BOARDWIDTH = 10  # number of columns of icons
BOARDHEIGHT = 7  # number of rows of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

BASICFONTSIZE = 20


len_all_shapes = 6

assert len(ALLCOLORS) * len_all_shapes * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."


def draw_board(mainBoard):
    '''Draw the tiles already placed on the board.'''
    for pos, tile in mainBoard:
        tilex, tiley = pos
        drawBoardTile(tile, tilex, tiley)


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, MOVE_SURF, \
        MOVE_RECT, BOXSIZE, GAPSIZE, tile_drawer

    pygame.init()

    tile_drawer = TileDrawer(BOXSIZE)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    pygame.display.set_caption('Qwirkle')

    # Buttons
    MOVE_SURF, MOVE_RECT = makeText('End Move', BUTTONTEXTCOLOR, BUTTONTEXTCOLOR, WINDOWWIDTH - 150, WINDOWHEIGHT - 75)
    REGRET_SURF, REGRET_RECT = makeText('Regret', BUTTONTEXTCOLOR, BUTTONCOLOR, WINDOWWIDTH - 150, WINDOWHEIGHT - 50)
    SWAP_SURF, SWAP_RECT = makeText('Swap', BUTTONTEXTCOLOR, BUTTONCOLOR, WINDOWWIDTH - 150, WINDOWHEIGHT - 25)

    mousex = 0  # used to store x coordinate of mouse event
    mousey = 0  # used to store y coordinate of mouse event

    game = Game.make_new_game(2, 42)
    mainBoard = game.board.tiles

    currentSelectedTiles = []
    currentPlacedTiles = []

    DISPLAYSURF.fill(BGCOLOR)

    while True:  # main game loop

        mouseClicked = False
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        mouse_state = dict(x=mousex,
                           y=mousey,
                           clicked=mouseClicked)

        DISPLAYSURF.fill(BGCOLOR)  # drawing the window

        # Update the current hand of the current player
        currentHand = game.current_player.hand.tiles

        draw_hand(currentHand, mouse_state, currentSelectedTiles,
                  currentPlacedTiles)
        draw_score(DISPLAYSURF, game)
        draw_board(mainBoard)
        highlight_possible_placement(mainBoard, mouse_state,
                                     currentSelectedTiles,
                                     currentPlacedTiles,
                                     BOXSIZE, GAPSIZE)

        # Draw current player name by the hand selection

        # Draw buttons
        DISPLAYSURF.blit(MOVE_SURF, MOVE_RECT)

        # Highlight button if mouse is over it
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

        # Update Buttons
        MOVE_SURF, MOVE_RECT = makeText('End Move', moveButtonTextColor, moveButtonColor, WINDOWWIDTH - 150, WINDOWHEIGHT - 75)
        REGRET_SURF, REGRET_RECT = makeText('Regret', regretButtonTextColor, regretButtonColor, WINDOWWIDTH - 150, WINDOWHEIGHT - 50)
        SWAP_SURF, SWAP_RECT = makeText('Swap', swapButtonTextColor, swapButtonColor, WINDOWWIDTH - 150, WINDOWHEIGHT - 25)

        # Draw Buttons
        DISPLAYSURF.blit(MOVE_SURF, MOVE_RECT)
        DISPLAYSURF.blit(REGRET_SURF, REGRET_RECT)
        DISPLAYSURF.blit(SWAP_SURF, SWAP_RECT)

        # Swap selected tile when pressing on SWAP button
        if SWAP_RECT.collidepoint(mousex, mousey) and mouseClicked and currentSelectedTiles:
            tiles = []
            for tile, x, y in currentSelectedTiles:
                tiles.append(tile)
            game.exchange_tiles(tiles)
            currentSelectedTiles = []

        # Empty the currentPlacedTiles list when you press Regret
        if REGRET_RECT.collidepoint(mousex, mousey) and mouseClicked and currentPlacedTiles:
            currentPlacedTiles = []
            currentSelectedTiles = []

        # Finish the move when pressing on MOVE button
        tiles_and_positions = []
        if MOVE_RECT.collidepoint(mousex, mousey) and mouseClicked:
            if currentPlacedTiles:
                for (tilex, tiley), (tile, x, y) in currentPlacedTiles:
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


def check_possible_placement(tiles, tile_x, tile_y):
    possibleMove = False
    for pos, _ in tiles:
        if pos == (tile_x, tile_y):
            possibleMove = False
            break
        elif pos[0] == tile_x and pos[1] == tile_y + 1:
            possibleMove = True
        elif pos[0] == tile_x and pos[1] == tile_y - 1:
            possibleMove = True
        elif pos[0] == tile_x + 1 and pos[1] == tile_y:
            possibleMove = True
        elif pos[0] == tile_x - 1 and pos[1] == tile_y:
            possibleMove = True
    return possibleMove


def highlight_possible_placement(mainBoard, mouse_state, current_selected_tiles, current_placed_tiles, BOXSIZE, GAPSIZE):
    '''Highlight the possible next move when mouse is hovering over it and mark it as possible move'''
    possibleMove = False
    if not mainBoard and not current_placed_tiles: #if there are no Tiles in mainBoard yet, highlight the first possible move
        x = WINDOWWIDTH/2 - BOXSIZE/2
        y = WINDOWHEIGHT/2 - BOXSIZE/2
        boxRect = pygame.Rect(x, y, BOXSIZE, BOXSIZE)
        if boxRect.collidepoint(mouse_state['x'], mouse_state['y']):
            possibleMove = True
            pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, BOXSIZE, BOXSIZE))
    else:
        # Check if there is an empty tile spot next to a real tile
        boxx, boxy = getTileAtPixel(mouse_state['x'], mouse_state['y'])

        if boxx is not None:
            if current_placed_tiles:
                possibleMove = check_possible_placement(current_placed_tiles, boxx, boxy)
            else:
                possibleMove = check_possible_placement(mainBoard, boxx, boxy)

            if possibleMove:
                x = WINDOWWIDTH/2 - BOXSIZE/2 + boxx*BOXSIZE + boxx*GAPSIZE
                y = WINDOWHEIGHT/2 - BOXSIZE/2 + boxy*BOXSIZE + boxy*GAPSIZE
                if y < (WINDOWHEIGHT - BOXSIZE*3):  # This is so that it is not possible to make a move 
                                                    # across the hadn area
                    pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, BOXSIZE, BOXSIZE))

                # If the board becomes bigger than the screen, shrink the tiles
                if x > (WINDOWWIDTH - (BOXSIZE)) or x < (BOXSIZE) or y > (WINDOWHEIGHT - (BOXSIZE*3)) or y < (BOXSIZE):
                    BOXSIZE = BOXSIZE*0.99
                    GAPSIZE = GAPSIZE*0.99
    # if a possible move is selected, and a tile is selected, draw the current tile there
    if possibleMove and mouse_state['clicked'] and current_selected_tiles:
        for tile, x, y in current_selected_tiles:
            current_placed_tiles.append([getTileAtPixel(mouse_state['x'], mouse_state['y']), (tile, x, y)])
            current_selected_tiles.remove((tile, x, y))
            break

    if current_placed_tiles:
        for (tilex, tiley), (tile, x, y) in current_placed_tiles:
            # This is to highlight the newly placed tile
            x, y = leftTopCoordsOfBox(tilex, tiley)
            pygame.draw.rect(DISPLAYSURF, YELLOW, (x - GAPSIZE/2 , y - GAPSIZE/2, BOXSIZE + GAPSIZE, BOXSIZE + GAPSIZE)) #Draw the highlight around the tile
            drawBoardTile(tile, tilex,  tiley)  # Draw the actual tile


def draw_hand(hand, mouse_state, currentSelectedTiles, currentPlacedTiles):
    # Draw the player hand area
    boxx = WINDOWWIDTH/2 - (BOXSIZE*3 + GAPSIZE*4)
    boxy = WINDOWHEIGHT - BOXSIZE*1.1 - GAPSIZE
    pygame.draw.rect(DISPLAYSURF, WHITE, (boxx, boxy, (BOXSIZE+GAPSIZE)*6 + GAPSIZE, BOXSIZE*2))

    # Highlight the hand tile the mouse is hovering over and select if mousebutton is selected
    hoverTile = getHandTileAtPixel(mouse_state['x'], mouse_state['y'], hand)
    tileSelected = False
    if mouse_state['clicked']:
        if hoverTile is not None:
            for tile, x, y in currentSelectedTiles:
                if hoverTile == (tile, x, y):
                    tileSelected = True
                    currentSelectedTiles.remove((tile, x, y))
            if not tileSelected:
                currentSelectedTiles.append(hoverTile)

    # Highlight the currently selected tiles in the hand
    if currentSelectedTiles:
        for currentTile, x, y in currentSelectedTiles:
            space = 0
            for tile in hand:
                if tile == currentTile:
                    x = WINDOWWIDTH/2 - (BOXSIZE+GAPSIZE)*3 + space
                    y = WINDOWHEIGHT - BOXSIZE*1.1
                    pygame.draw.rect(DISPLAYSURF,BLUE, (x - GAPSIZE/2 , y - GAPSIZE/2, BOXSIZE + GAPSIZE, BOXSIZE + GAPSIZE))         
                space = space + BOXSIZE + GAPSIZE

    # Draw the player hand
    space = 0
    for tile in hand:
        x = WINDOWWIDTH/2 - (BOXSIZE+GAPSIZE)*3 + space
        y = WINDOWHEIGHT - BOXSIZE*1.1
        drawTile(tile, x, y, BOXSIZE)
        space = space + BOXSIZE + GAPSIZE

    # Hide the currently placed tiles from the hand
    for pos, (currentPlacedTile, x, y) in currentPlacedTiles:
        space = 0
        for tile in hand:
            if tile == currentPlacedTile:
                x = WINDOWWIDTH/2 - (BOXSIZE+GAPSIZE)*3 + space
                y = WINDOWHEIGHT - BOXSIZE*1.1
                pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, BOXSIZE, BOXSIZE))
                break
            space = space + BOXSIZE + GAPSIZE


def draw_score(DISPLAYSURF, game):
    # Update the Score
    for playernr, player in enumerate(game.players, start=1):
        scoreText = 'Player ' + str(playernr) + ': ' + str(player.total_score())
        if player == game.current_player:
            txtColor = GREEN
        else:
            txtColor = TEXTCOLOR
        SCORE_SURF, SCORE_RECT = makeText(scoreText, txtColor, MESSAGECOLOR, WINDOWWIDTH - 125, 25 * playernr)
        DISPLAYSURF.blit(SCORE_SURF, SCORE_RECT)  # Draw statistics of names and scores on top right corner


def drawBoardTile(tile, tilex, tiley):  # new method to use on board instead of just drawTile
    x = WINDOWWIDTH/2 - BOXSIZE/2 + tilex*BOXSIZE + tilex*GAPSIZE
    y = WINDOWHEIGHT/2 - BOXSIZE/2 + tiley*BOXSIZE + tiley*GAPSIZE
    drawTile(tile, x, y, BOXSIZE)


def drawTile(tile, x_i, y_i, size):
    tile_surface = tile_drawer.get_tile_surface(tile)
    DISPLAYSURF.blit(tile_surface, dest=(x_i, y_i))


def getHandTileAtPixel(x, y, hand):
    space = 0
    for tile in hand:
        boxx = WINDOWWIDTH/2 - (BOXSIZE+GAPSIZE)*3 + space
        boxy = WINDOWHEIGHT - BOXSIZE*1.1
        boxRect = pygame.Rect(boxx, boxy, BOXSIZE, BOXSIZE)
        if boxRect.collidepoint(x, y):
            pygame.draw.rect(DISPLAYSURF, BLACK, (boxx - GAPSIZE/2, boxy - GAPSIZE/2, BOXSIZE + GAPSIZE, BOXSIZE + GAPSIZE))  
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
