import sys
import math
import pygame
from pygame.locals import *

def formtext(text,size=15,color=(0,0,0),font=None):
    font = pygame.font.Font(font,size)
    text = font.render(
        text,
        True,
        color
    )
    return text

def target_angle(x1,x2,y1,y2):
    angle_radians = math.atan2(y2-y1,x2-x1)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

def wrap_angle(angle):
    return abs(angle % 360)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        playerwidth,playerheight = 16,28
        self.image = pygame.Surface((playerwidth,playerheight))
        self.image.fill(GREEN)
        self.rect = Rect(
            (screen.get_width()-playerwidth)/2,
            (screen.get_height()-playerheight)/2,
            playerwidth,
            playerheight
        )
        self.posx,self.posy = 0,0
        self.speedx,self.speedy = 1,1
        
    def move(self,direction):
        # move the role
        if direction == "UP":
            self.posy-=self.speedy
        elif direction == "DOWN":
            self.posy+=self.speedy
        elif direction == "LEFT":
            self.posx-=self.speedx
        elif direction == "RIGHT":
            self.posx+=self.speedx
            

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (255,0,255)

pygame.init()
screen = pygame.display.set_mode((800,550))
pygame.key.set_repeat(120)
fps = pygame.time.Clock()

######### Groups #########
group_players = pygame.sprite.Group()
group_guns = pygame.sprite.Group()

##########################

player = Player()
group_players.add(player)


while True:
    fps.tick(60)

    screen.fill(WHITE) # clear the screen
    
    for event in pygame.event.get():
        if event.type in (QUIT,):
            pygame.quit()
            sys.exit()
        elif event.type in (KEYDOWN,):
            # Move the player
            if event.key == 119:
                player.move("UP")
            elif event.key == 115:
                player.move("DOWN")
            elif event.key == 97:
                player.move("LEFT")
            elif event.key == 100:
                player.move("RIGHT")
        elif event.type in (MOUSEBUTTONDOWN,):
            if event.button == 4:
                pass
            elif event.button == 5:
                pass
    
    screen.blit(
        formtext(f"player-position: {player.posx},{player.posy}"),
        (0,0)
    )

    mousex,mousey = pygame.mouse.get_pos()
    screen.blit(
        formtext(f"mouse-position: {mousex},{mousey}"),
        (0,12)
    )

    screen.blit(
        formtext(f"player-rect: {player.rect}"),
        (0,24)
    )

    group_players.draw(screen)
    group_guns.update(screen)
    group_guns.draw(screen)

    pygame.display.update()

    
