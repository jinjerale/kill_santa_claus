#block
import pygame
from ref import resource_path
from pygame.locals import *
from Vec2d import *


class Block(pygame.sprite.Sprite):
    def __init__(self,location):
        
        # super(Block, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(resource_path('./_data/back/wall3.png')).convert_alpha()
        self.w,self.h = 40,40
        #self.surf = pygame.Surface((self.size, self.size))
        #self.surf.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.location = location
        # self.lethality = 0
        self.blood = 300
        self.point = 10
    
    def update(self):
        if self.blood <= 0: self.kill()
    

    
    def draw(self,surface):
        x,y = self.location
        #w,h = self.image.get_size()
        surface.blit(self.image, (x - self.w/2, y - self.h/2))

class Venue1:
    #只有上下兩條線，其他都沒東西    
    def __init__(self):
        self.block_group = pygame.sprite.Group()
        #self.blocks = []
        
        for pos_y in (20,580):
            for pos_x in range(20,820,40):
                wall = Block(Vec2d(pos_x,pos_y))
                self.block_group.add(wall)
                #self.blocks.a(wall)
        for pos_x in range(300,820,40):
            wall = Block(Vec2d(pos_x,420))
            self.block_group.add(wall)
        for pos_x in range(20,380,40):
            wall = Block(Vec2d(pos_x,180))
            self.block_group.add(wall)
        for pos_x in range(580,820,40):
            wall = Block(Vec2d(pos_x,180))
            self.block_group.add(wall)
    
    def draw(self,surface):
        for block in self.block_group:
            block.draw(surface)


class Venue2:
    #一點一點狀結構
    
    def __init__(self):
        self.block_group = pygame.sprite.Group()
        
        # self.blocks = []
        for pos_x in range(100,740,120):
            for pos_y in (140,300,460):
                wall = Block(Vec2d(pos_x,pos_y))
                self.block_group.add(wall)
               

    def draw(self,surface):
        for block in self.block_group:
            block.draw(surface)



class Venue3:
    #maze_like shape
    def __init__(self):
        self.block_group = pygame.sprite.Group()
        # horizontal margin
        for pos_x in range(8):
            for pos_y in (20,580):
                wall = Block(Vec2d(40*pos_x+20,pos_y))
                self.block_group.add(wall)
        for pos_x in range(8):
            for pos_y in (20,580):
                wall = Block(Vec2d(780-40*pos_x,pos_y))
                self.block_group.add(wall)
        # vertical margin
        for pos_y in range(6):
            for pos_x in (20,780):
                wall = Block(Vec2d(pos_x,40*pos_y+20))
                self.block_group.add(wall)
        for pos_y in range(6):
            for pos_x in (20,780):
                wall = Block(Vec2d(pos_x,580-40*pos_y))
                self.block_group.add(wall)
        # inner margin
        # for pos_x in range(10):
        #     for pos_y in (220,460):
        #         wall = Block(Vec2d(40*pos_x+220,pos_y))
        #         self.block_group.add(wall)

        for pos_y in range(5):
            for pos_x in (260,660):
                wall = Block(Vec2d(pos_x,40*pos_y+100))
                self.block_group.add(wall)
        for pos_y in range(4):
            for pos_x in (140,540):
                wall = Block(Vec2d(pos_x,40*pos_y+340))
                self.block_group.add(wall)
        
        
    def draw(self,surface):
        for block in self.block_group:
            block.draw(surface)

'''
class Player1(pygame.sprite.Sprite):

    def __init__(self, world=None, image=None):

        pygame.sprite.Sprite.__init__(self)
        self.w, self.h = 25, 25
        self.location = (250, 300)
        self.image = pygame.image.load(image).convert_alpha()
        #self.image = pygame.Surface((self.w, self.h))
        #self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.speed = 50
        self.direction = Vec2d(0, -1)
        self.world = world
        #self.num = num
        #self.gun_in_hand = 'pistal'
        #self.blood = 30

    def update(self, time_passed_seconds,):

        pressed_keys = pygame.key.get_pressed()
        key_direction = Vec2d(0, 0)

        if pressed_keys[K_LEFT]:
            key_direction.x = -1
            #print(self.location)

        elif pressed_keys[K_RIGHT]:
            key_direction.x = +1

        if pressed_keys[K_UP]:
            key_direction.y = -1

        elif pressed_keys[K_DOWN]:
            key_direction.y = +1
        
        if pressed_keys[K_RSHIFT] :
            self.fire(time_passed_seconds,surface)
        
        key_direction.normalized()
        if not key_direction == Vec2d(0,0):
            self.direction = key_direction
        self.location += key_direction * self.speed * time_passed_seconds        
        
        if self.location.x < self.w / 2: self.location.x = self.w / 2
        elif self.location.x > screen_width - self.w / 2: self.location.x = screen_width - self.w / 2
        if self.location.y < self.h / 2: self.location.y = self.h / 2
        elif self.location.y > screen_height - self.h / 2: self.location.y = screen_height - self.h / 2
        #player v.s. blocks
        blocks_hit_list = pygame.sprite.spritecollide(self, v1.block_group, False)        
        #print(blocks_hit_list)
        if blocks_hit_list != None:
            for block in blocks_hit_list:
                pos_x,pos_y = block.location
                if self.location.x < pos_x+20+self.w / 2: self.location.x = pos_x+20+self.w / 2
                elif self.location.x > pos_x - 20 - self.w / 2: self.location.x = pos_x - 20 - self.w / 2
                if self.location.y < pos_y+20+self.h / 2: self.location.y = pos_y+20+self.h / 2
                elif self.location.y > pos_y-20 - self.h / 2: self.location.y = pos_y-20 - self.h / 2
        else:pass
        if pygame.sprite.spritecollideany(self,v1.block_group):
            print('bomb')
    
    def backoff(self):
        pass    #run if player is being hit.
    
    def fire(self, time_passed_seconds):

        tmp = (self.location[0], self.location[1])
        bullet = Bullet(self.world, tmp, self.direction)
        self.world.bullets.append(bullet)
    
    def draw(self, surface):

        x, y = self.location
        #w, h = self.surf.get_size()
        surface.blit(self.image, (x-self.w/2, y-self.h/2))
#start
pygame.init()  
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
v1 = Venue1()
#playerGroup
players = pygame.sprite.Group()
p1 = Player1(None,'p1.png')
players.add(p1)
background = pygame.Surface(screen.get_size())
background.fill((0,0,0))
#loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:    
            exit()
        elif pygame.key.get_pressed()[K_ESCAPE]:
            exit()
    time_passed = clock.tick(30)
    time_passed_seconds = time_passed / 1000 #it should be 1000, but it's too slow;
    colide = None
    #colider = pygame.sprite.spritecollideany(p1, v1.block_group)
    if colider != None:
        if pygame.sprite.collide_rect_ratio(0.65)(player,colider):
            pos_x,pos_y = block.location
            if self.location.x < pos_x+20+self.w / 2: self.location.x = pos_x+20+self.w / 2
            elif self.location.x > pos_x - 20 - self.w / 2: self.location.x = pos_x - 20 - self.w / 2
            if self.location.y < pos_y+20+self.h / 2: self.location.y = pos_y+20+self.h / 2
            elif self.location.y > pos_y-20 - self.h / 2: self.location.y = pos_y-20 - self.h / 2
    
    p1.update(time_passed_seconds)
    screen.blit(background, (0, 0))
    v1.draw(screen)    
    p1.draw(screen)
    pygame.display.flip()'''