import pygame
import os
import random
import math
from pygame.math import Vector2
pygame.init()

display_width = 800
display_height = 600
walldistance = 180

game_name = pygame.display.set_caption("Oh no! Parasites!")  # define the name of the game
gameDisplay = pygame.display.set_mode((display_width, display_height))

background = pygame.image.load('BackGround.png')
guy = pygame.image.load('guy.png')
friendimg = pygame.image.load('friend.png')
cross = pygame.image.load('cross.png')
enemyimg = pygame.image.load('Alien.png')
gameover = pygame.image.load('gameover.png')
youlost = pygame.image.load('youlost.png')
shoot = pygame.image.load('Bullet.png')


hole_x = 350
hole_y = 600

friend_count = 0

enemy_speed = 2
friend_speed = 2
white = (255, 255, 255)

lives_max = 10
lives_count = lives_max

holecoord = (hole_x, hole_y)

friendslst = []
enemieslst = []
bulletslst = []

clock = pygame.time.Clock()

class Shooter(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = 5

        self.image = guy
        self.orig_image = guy
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

        self.rotated_surface = guy.copy()

    def update(self):
        angle = math.atan2(pygame.mouse.get_pos()[1] - self.y, pygame.mouse.get_pos()[0] - self.x)
        angle = angle * (-180/math.pi)
        self.move()
        self.rotate(angle)
        gameDisplay.blit(self.rotated_surface, (self.x, self.y))


    def rotate(self, angle):

        rot_image = pygame.transform.rotozoom(self.orig_image, angle, 1)
        rot_rect = self.rect.copy()
        rot_rect.center = rot_image.get_rect().center
        self.rotated_surface = rot_image
        mousepos = (pygame.mouse.get_pos())
        gameDisplay.blit(cross, (mousepos[0] - 20, mousepos[1] - 20))


    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < display_height - 80:
            self.y += self.speed
        if keys[pygame.K_LEFT] and self.x > walldistance:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < display_width - 80:
            self.x += self.speed

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.shoot()

    def shoot(self):
        if len(bulletsgrp)<10:
            bullet = Bullet(self.x+70, self.y+90)
            all_sprites.add(bullet)
            bulletsgrp.add(bullet)

#now we onlyhave one class with friends and enemies. differences are defined in the rangen (random generator) function
class FriendsEnemies (pygame.sprite.Sprite):

    def __init__(self,x, y, image, speed,type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.speed = speed
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x=x
        self.rect.y=y
        self.type=type
        self.xdirection = ((hole_x - x) / (abs(hole_x - x)+abs(hole_y - y)))
        self.ydirection = ((hole_y - y) / (abs(hole_x - x)+abs(hole_y - y)))

    def move(self):
        global hole_x, hole_y, friend_count, lives_count
        self.x += self.xdirection * self.speed
        self.y += self.ydirection * self.speed

        if 286 < self.x < 584 and 556 < self.y < 600:  # collision with the box
            if self.type == 2:
                lives_count-= 1
            else :
                friend_count +=1
            self.kill()
            #collision with the bottom right wall,tofix
     #   if 755<self.x and 300<self.y:
    #        self.x += 2
      #      self.y+= self.ydirection * self.speed

    def update(self):
        self.move()
        gameDisplay.blit(self.image,(self.x,self.y))


class Bullet(pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.img = shoot
        self.x = x
        self.y = y
        self.rect = self.img.get_rect()
        self.speed=10
        xmouse, ymouse = pygame.mouse.get_pos()
        self.xdirection = ((xmouse - x) / (abs(xmouse - x)+abs(ymouse - y)))
        self.ydirection = ((ymouse - y) / (abs(xmouse - x)+abs(ymouse - y)))

    def move(self):

        if 69 < self.x < display_width and 0 < self.y < 556:
            self.x += self.xdirection*self.speed
            self.y += self.ydirection*self.speed
        else:
            self.kill()
        for bullet in bulletsgrp:
            hits = pygame.sprite.spritecollide(bullet, enemiesgrp, True)
            for hit in hits:
                print("hit")
                hit.kill()

    def update(self):
        self.move()
        gameDisplay.blit(self.img, (self.x,self.y))


#***can these two things be condensed in one? and we should change the font***
def information_box_friend():
    font = pygame.font.SysFont(None, 25)
    text = font.render(str(friend_count), True, white)
    gameDisplay.blit(text, (128, 465))

def information_box_enemy():
    font = pygame.font.SysFont(None, 25)
    text = font.render(str(lives_count) +"/"+str ( lives_max), True, white)
    gameDisplay.blit(text, (110, 515))

#******this is where the miracle of life happens, friends and enemies are born******
def ranposgen(n):
    global friend_count, enemy_count, friend_speed, enemy_speed, friendimg, enemyimg
    #****spawning ranges that can be modified ****
    ran_x_up=random.randrange(250, (display_width + 100))
    ran_y_up=random.randrange(-300, -100)
    ran_x_right=random.randrange(display_width+50,display_width+200)
    ran_y_right=random.randrange(30, 250)

    if n == 1:
        m = FriendsEnemies(ran_x_up,ran_y_up,friendimg,friend_speed,1)
        friendsgrp.add(m)
    elif n == 2:
        m=FriendsEnemies(ran_x_right, ran_y_right, friendimg,friend_speed,1)
        friendsgrp.add(m)
    elif n == 3:
        m=FriendsEnemies(ran_x_up, ran_y_up, enemyimg, enemy_speed,2)
        enemiesgrp.add(m)
    elif n == 4:
        m = FriendsEnemies(ran_x_right, ran_y_right, enemyimg, enemy_speed,2)
        enemiesgrp.add(m)
    all_sprites.add(m)


def redrawGameWindow():

    gameDisplay.blit(background, (0, 0))  # placing background
    #****sprites groups are basically lists, so the respawn mechanism is the same as before*****
    if len(friendsgrp) <= 2:
        ranposgen(random.randrange(1, 3))
    if len(enemiesgrp) <= 2:
        ranposgen(random.randrange(3, 5))
#trying to create collision between one single bullet and a group? it works for nerea. i thing it must be something to do with rects
    for bullet in bulletsgrp:
        hits=pygame.sprite.spritecollide( bullet, enemiesgrp, True)
        for hit in hits:
            print ("hit")
            hit.kill()

    information_box_friend()
    information_box_enemy()
#everything is both in its own group and in "all_sprites", so we only need this to update everything

    all_sprites.update()

    pygame.sprite.groupcollide(enemiesgrp, bulletsgrp, True, True)

#collision between groups - need to watch tutorial to understand how to makeit work, it would be perfect
#   hits= pygame.sprite.groupcollide(enemiesgrp, bulletsgrp, True, True)
    #print (len(hits))
   # for hit in hits:
       # m = FriendEnemies()
      # all_sprites.add(m)
      #  mobs.add(m)

    pygame.display.update()


enemiesgrp = pygame.sprite.Group()
friendsgrp = pygame.sprite.Group()
bulletsgrp = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
#we call the instance of the shooter here.
all_sprites.add(Shooter(200, 200))

friends_saved = False

while not friends_saved:

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            friends_saved = True
            pygame.quit()
            os._exit(0)

    if lives_count == 0 :
        gameDisplay.blit(youlost, (400, 300))
        pygame.display.update()
    else:
        redrawGameWindow()


pygame.quit()
os._exit(0)




