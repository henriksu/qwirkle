import pygame, sys
from pygame.locals import *

# Initialize the game
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Qwirkle')
FPS = 30 #Frames per second setting
fpsClock = pygame.time.Clock()

#Mouse coordinates
mousex = 0
mousey = 0

# set up the colors
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)

fontObj = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj = fontObj.render('Henrik!', True, GREEN, BLUE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200, 150)

#Game loop
while True:
    mouseClicked = False
    #loop through the events
    for event in pygame.event.get():
            #check if the event is the X button
            if event.type==pygame.QUIT:
                    pygame.quit()
                    exit(0)
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True          
    
    #Draw on the screen
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (200, 150, 100, 50))
    pygame.draw.circle(screen, BLUE,  (mousex, mousey), 20, 0)
    screen.blit(textSurfaceObj, textRectObj)
    
    #Update the screen
    pygame.display.update()
    fpsClock.tick(FPS)
    
    