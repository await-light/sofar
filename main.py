import sys
import time
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
        self.direction = "RIGHT"
        
    def move(self,direction,group_blocks):
        # move the role
        x,y = self.posx,self.posy

        if direction == "UP":
            self.posy-=self.speedy
        elif direction == "DOWN":
            self.posy+=self.speedy
        elif direction == "LEFT":
            self.posx-=self.speedx
            self.direction = "LEFT"
        elif direction == "RIGHT":
            self.posx+=self.speedx
            self.direction = "RIGHT"

        group_blocks.update(self)
        touchwall = pygame.sprite.spritecollide(self,group_blocks,False)
        if touchwall:
            self.posx,self.posy = x,y
            for sprite in touchwall:
                sprite.touched(player)

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

    def touched(self,object_):
        print(f"{self} is touched by {object_}")
        self.image.fill(BLUE)

class Gun(pygame.sprite.Sprite):
    def __init__(self,timegap):
        pygame.sprite.Sprite.__init__(self)
        self.width,self.height = 20,5
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.direction = "RIGHT"
        self.timegap = timegap # sec
        self.lastshoot = 0

    def update(self,player):
        self.direction = player.direction
        if self.direction == "LEFT":
            dire = -1
        elif self.direction == "RIGHT":
            dire = 1
        self.rect.topleft = (
            (WIDTH-self.width)/2+dire*5,
            (HEIGHT-self.height)/2
        )

    def shoot(self,groups_bullet,player):
        nowtime = time.time()
        if nowtime - self.lastshoot >= self.timegap:
            groups_bullet.add(Bullet(self.direction,5,1000,player.posx,player.posy))
            self.lastshoot = nowtime

class Bullet(pygame.sprite.Sprite):
    def __init__(self,direction,speed,far,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.width,self.height = 5,3
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.posx,self.posy = x,y
        self.direction = direction
        self.speed = speed
        self.far = [far,0]

    def update(self,player):
        if self.direction == "LEFT":
            self.posx -= self.speed
        elif self.direction == "RIGHT":
            self.posx += self.speed
        self.far[1] += self.speed
        self.rect.topleft = (
            (WIDTH-self.width)/2-(player.posx-self.posx),
            (HEIGHT-self.height)/2-(player.posy-self.posy)
        )

        # If the bullet reaches the most length
        if self.far[1] >= self.far[0]:
            self.kill()

    def knock(self,object_):
        print(f"{self} knocks {object_}")
        # when knocking something
        self.kill()

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
group_blocks = pygame.sprite.Group()
group_guns = pygame.sprite.Group()
group_bullets = pygame.sprite.Group()

##########################

player = Player()
group_players.add(player)
gun = Gun(timegap=1)
group_guns.add(gun)
group_blocks.add(Block(3,3))
group_blocks.add(Block(1,5))
group_blocks.add(Block(2,2))
group_blocks.add(Block(3,8))
group_blocks.add(Block(3,7))
group_blocks.add(Block(3,6))
group_blocks.add(Block(3,5))
group_blocks.add(Block(3,4))

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
        player.move("UP",group_blocks)
    if key[pygame.K_s]:
        player.move("DOWN",group_blocks)
    if key[pygame.K_a]:
        player.move("LEFT",group_blocks)
    if key[pygame.K_d]:
        player.move("RIGHT",group_blocks)
    if key[pygame.K_j]:
        gun.shoot(group_bullets,player)

    for bullet,blocks in pygame.sprite.groupcollide(group_bullets,group_blocks,False,False).items():
        for block in blocks:
            bullet.knock(block)
            block.touched(bullet)
    
    group_blocks.update(player)
    group_blocks.draw(screen)

    group_players.draw(screen)
    
    group_bullets.update(player)
    group_bullets.draw(screen)

    group_guns.update(player)
    group_guns.draw(screen)
    
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

    screen.blit(
        formtext(f"player-direction: {player.direction}"),
        (0,48)
    )

    pygame.display.update()
