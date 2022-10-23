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
        width,height = 16,28
        self.image = pygame.Surface((width,height))
        self.image.fill(GREEN)
        self.rect = Rect(
            (WIDTH-width)/2,
            (HEIGHT-height)/2,
            width,
            height
        )
        self.posx,self.posy = 0,0
        self.speedx,self.speedy = 2,2
        
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

class Gun(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        width,height = 20,5
        self.image = pygame.Surface((width,height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen.get_width()-width)/2,(screen.get_height()-height)/2,

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.width,self.height = 20,20
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.posx,self.posy = x*20,y*20

    def update(self,player):
        self.rect.topleft = (
            (WIDTH-self.width)/2-(player.posx-self.posx),
            (HEIGHT-self.height)/2-(player.posy-self.posy)
        )

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (255,0,255)
WIDTH,HEIGHT = 800,550

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.key.set_repeat(10)
fps = pygame.time.Clock()

######### Groups #########
group_players = pygame.sprite.Group()
# group_guns = pygame.sprite.Group()
group_blocks = pygame.sprite.Group()

##########################

player = Player()
group_players.add(player)
# gun = Gun()
# group_guns.add(gun)
group_blocks.add(Block(3,3))


while True:
    fps.tick(60)

    screen.fill(WHITE) # clear the screen
    
    for event in pygame.event.get():
        if event.type in (QUIT,):
            pygame.quit()
            sys.exit()
        elif event.type in (MOUSEBUTTONDOWN,):
            if event.button == 4:
                pass
            elif event.button == 5:
                pass

    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.move("UP")
    if key[pygame.K_s]:
        player.move("DOWN")
    if key[pygame.K_a]:
        player.move("LEFT")
    if key[pygame.K_d]:
        player.move("RIGHT")

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

    iftouchwall = pygame.sprite.spritecollide(player,group_blocks,False)
    screen.blit(
        formtext(f"touch-wall: {iftouchwall}"),
        (0,36)
    )

    group_players.draw(screen)
    group_blocks.update(player)
    group_blocks.draw(screen)
    # group_guns.update(screen)
    # group_guns.draw(screen)

    pygame.display.update()
