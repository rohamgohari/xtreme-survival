import pygame
pygame.init()

import moviepy
from moviepy.editor import *
import os
win = pygame.display.set_mode((1880,1080))
pygame.display.set_caption("xtreme survival")
os.environ["SDL_VIDEO_CENTERED"] = "1"

clip = VideoFileClip('xtrim.mp4')


clip.preview()


import pygame_menu
pygame.init()
surface = pygame.display.set_mode((1880, 1080))
def set_difficulty(value, difficulty):
    # Do the job here !
    pass
def xtrem():
    win = pygame.display.set_mode((1366,768))
    pygame.display.set_caption("xtreme survival")
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    clip = VideoFileClip('jjjj.mp4')


    clip.preview()
 
    
def start_the_game():
    win = pygame.display.set_mode((1000,420))
    walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
    walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
    bg = pygame.image.load('background2.jpg')
    char=pygame.image.load('standing.png')
    clock = pygame.time.Clock()


    #bulletSound = pygame.mixer.Sound("bullet.wav")
    #hitSound = pygame.mixer.Sound("hit.wav")


    music = pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    score=0
    b=11

    player_health=50

    class player(object):
        def __init__(self,x,y,width,height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = 5
            self.isJump = False
            self.left = False
            self.right = False
            self.walkCount = 0
            self.jumpCount = 10
            self.standing = True
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)

        def draw(self, win):
            if self.walkCount + 1 >= 27:
                self.walkCount = 0

            if not(self.standing):
                if self.left:
                    win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                    self.walkCount += 1
                elif self.right:
                    win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                    self.walkCount +=1
            else:
                if self.right:
                    win.blit(walkRight[0], (self.x, self.y))
                else:
                    win.blit(walkLeft[0], (self.x, self.y))
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)

        def hit(self):
            self.isJump=False
            self.jumpCount=10
            self.x = 60
            self.y = 310
            self.walkCount = 0
            font1 = pygame.font.SysFont('comicsans', 100)
            text = font1.render('hp -10', 1, (255,0,0))
            win.blit(text, (370 - (text.get_width()/2),200))
            pygame.display.update()
            i = 0
            while i < 100:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 101
                        pygame.quit()

    class projectile(object):
        def __init__(self,x,y,radius,color,facing):
            self.x = x
            self.y = y
            self.radius = radius
            self.color = color
            self.facing = facing
            self.vel = 8 * facing

        def draw(self,win):
            pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

    class enemy(object):
        walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
        walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
        
        def __init__(self, x, y, width, height, end):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.end = end
            self.path = [self.x, self.end]
            self.walkCount = 0
            self.vel = 3
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            self.health = 10
            self.visible = True

        def draw(self,win):
            self.move()
            if self.visible:
                if self.walkCount + 1 >= 33:
                    self.walkCount = 0

                if self.vel > 0:
                    win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                    self.walkCount += 1
                else:
                    win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                    self.walkCount += 1

                pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
                pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
                self.hitbox = (self.x + 17, self.y + 2, 31, 57)

        def move(self):
            if self.vel > 0:
                if self.x + self.vel < self.path[1]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0
            else:
                if self.x - self.vel > self.path[0]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0

        def hit(self):
            if self.health > 0:
                self.health -= 1
            else:
                self.visible = False



    def redrawGameWindow():
        win.blit(bg, (0,0))
        text=font.render('score: '+ str(score),1,(255,255,255))
        win.blit(text,(610,10))
        text=font.render('player HP: '+str(player_health),1,(255,255,255))
        win.blit(text,(20,10))
        man.draw(win)
        goblin.draw(win)
        for bullet in bullets:
            bullet.draw(win)
        pygame.display.update() 
        
    font=pygame.font.SysFont('comicsans',30,True)
    man=player(500,310,64,64)
    goblin = enemy(200, 310, 64, 64, 500)
    shooting_bug=0
    bullets=[]
    run = True

    while run:
        clock.tick(27)

        if goblin.visible==True:
            if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                    man.hit()
                    player_health-=10
                    

        if player_health==0:
            font1 = pygame.font.SysFont('comicsans', 100)
            text = font1.render('Game over', 1, (255,0,0))
            win.blit(text, (370 - (text.get_width()/2),100))
            pygame.display.update()
            i = 0
            while i < 100:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 301
                        pygame.quit()
                isJump=False
            man.jumpCount=10
            man.x = 60
            man.y = 310
            man.walkCount = 0
            score=0
            goblin.health=10
            player_health=50

        if score>b:
            b+=11
            goblin.draw(win)
            pygame.display.update()
        
        
        
        if shooting_bug>0:
            shooting_bug+=1
        if shooting_bug>3:
            shooting_bug=0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for bullet in bullets:
            if goblin.visible==True:
                if bullet.y-bullet.radius<goblin.hitbox[1]+goblin.hitbox[3] and bullet.y+bullet.radius>goblin.hitbox[1]:
                    if bullet.x+bullet.radius>goblin.hitbox[0] and bullet.x-bullet.radius<goblin.hitbox[0]+goblin.hitbox[2]:
                        goblin.hit()
                        score+=1
                        bullets.pop(bullets.index(bullet))
                    
            if bullet.x<740 and bullet.x>0:
                bullet.x+=bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        if goblin.visible==False:
            goblin.x = 200
            goblin.y = 310
            goblin.width = 64
            goblin.height = 64
            goblin.end = 610
            goblin.path = [200, 610]
            goblin.walkCount = 0
            goblin.vel = 3
            goblin.hitbox = (goblin.x + 17, goblin.y + 2, 31, 57)
            goblin.health = 10
            goblin.visible = True
            i = 0
            

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and shooting_bug==0:
            if man.left:
                facing= -1
            else:
                facing=1
            if len(bullets)<5:
                bullets.append(projectile(round(man.x+man.width//2), round(man.y+man.height//2), 6, (0,0,0), facing))

            shooting_bug=1
        if keys[pygame.K_LEFT] and man.x > man.vel: 
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing=False
        elif keys[pygame.K_RIGHT] and man.x < 850 - man.width - man.vel:  
            man.x += man.vel
            man.left = False
            man.right = True
            man.standing=False
        else: 
            man.standing=True
            man.walkCount = 0
            
        if not(man.isJump):
            if keys[pygame.K_UP]:
                man.isJump = True
                man.left = False
                man.right = False
                man.walkCount = 0
        else:
            if man.jumpCount >= -10:
                neg=1
                man.y -= (man.jumpCount * abs(man.jumpCount)) * 0.5*neg
                man.jumpCount -= 1
            else: 
                man.jumpCount = 10
                man.isJump = False

        redrawGameWindow()


def sss():

    menu.add_button('Halloween',rrr)
    menu.add_botton('texas',lll)
    
def tti():
    

    menu.add_button('background',sss)
    

menu = pygame_menu.Menu(700, 700, 'Welcome',
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add_text_input('Name :', default='John Doe')
menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add_button('Play', start_the_game)
menu.add_button('about',xtrem)
menu.add_button('settings',tti)
menu.add_button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)

execfile("xtrim.py")
execfile("ttt.py")
pygame.quit()
