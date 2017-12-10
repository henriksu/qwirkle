import pygame
from pygame.locals import *
from nltk.app.nemo_app import images

# Initialize the game
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

#Load images

#Game loop
while 1:
    #Clear the screen before drawing again
    screen.fill(0)
    #draw the screen elements
    #screen.draw.rect()
    #update the screen
    pygame.display.flip()
    #loop through the events
    for event in pygame.event.get():
            #check if the event is the X button
            if event.type==pygame.QUIT:
                    pygame.quit()
                    exit(0)
    
    