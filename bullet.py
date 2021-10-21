import pygame
from pygame.locals import *
from Vec2d import *
from GameSprite import *
from copy import deepcopy
import random

# bug line 121 the "is not None" expression is wrong
# bug line 125 shooter hit itself and distroy the bullet
# add new parameter: player to prevent line125
# RPG explode when hit other
# shotgun is still bug

class Bullet(GameSprite):# pygame.sprite.Sprite
    
    def __init__(self, player,world, location, direction, weapon = ''):

        #super(Bullet, self).__init__()
        GameSprite.__init__(self)
        #self.image = pygame.image.load()
        self.w = self.h = 7
        self.surf = pygame.Surface((self.w, self.h))
        self.surf.fill((200, 200, 200))
        self.rect = self.surf.get_rect()
        
        self.location = location
        self.initial_location = deepcopy(self.location)
        self.direction = direction
        
        self.player = player
        self.world = world
        #self.world.bullets.add(self)
        
        self.blood = 0

        self.speed = 30
        self.weapon = weapon
        self.range = 100
        self.lethality = 0
        # self.timer = 0
        # self.cd_time = 0 # the cool down time each bullet is released
        self.gun()
    

    # generate different bullets with respect to weapon
    def gun(self):

        if self.weapon == 'pistal':
            self.surf.fill((200, 200, 200))
            self.speed = 200
            self.range = 350
            self.lethality = 7

        elif self.weapon == 'machine_gun':
            self.surf.fill((241, 191, 69))
            self.speed = 400
            self.range = 500
            self.lethality = 7

        
        elif self.weapon == 'shotgun':
            self.surf.fill((255, 255, 255))
            self.speed = 100
            self.range = 10
            self.lethality = 20

        
        elif self.weapon == 'grenade':
            self.surf.fill((255, random.randint(200,230), 0))
            self.speed = 30
            self.range = 100
            self.lethality = 20


        elif self.weapon == 'mine':
            self.surf.fill((208, 208, 208))
            self.speed = 1
            self.range = 3
            self.lethality = 30
            # self.stop_time = 3

            
        elif self.weapon == 'RPG':
            self.h = self.w = 10
            self.surf = pygame.Surface((self.w, self.h))
            self.surf.fill((208,208,208))
            self.speed = 200
            self.range = 300
            self.lethality = 35

        
        elif self.weapon == 'fragmentation':
            self.surf.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            self.speed = 100
            self.range = 50
            self.lethality = 5
        
        

    def update(self, time_passed_seconds):
        
        if (self.location[0] - self.initial_location[0]) ** 2 + (self.location[1] - self.initial_location[1]) ** 2 < self.range ** 2:
            
            if -50 < self.location[0] < 850 and -50 < self.location[1] < 650 :

                if self.weapon == 'RPG':
                    self.surf.fill((random.randint(198,218), random.randint(0,218), 0))
                
                self.location += self.direction * self.speed * time_passed_seconds
                

            else:
                self.kill()
                return False
        else:
            
            if self.weapon == 'grenade' or self.weapon == 'mine' or self.weapon == 'RPG':
                
                self.explosion(self.location,self.weapon)

            elif self.weapon == 'shotgun':
                tmp = (self.location[0],self.location[1])
                
                for angle in range (-20,30,10):

                    # bullet = Bullet(self.world, tmp, self.rotate(angle), 'fragmentation')
                    bullet = Bullet(self.player,self.world, tmp, self.rotate(angle), 'pistal')
                    self.world.bullets.add(bullet)

            self.kill()
        
        #hit blocks
        if self.check_groupcolide(self.world.land.block_group):
            colision = self.find_colision(self.world.land.block_group)
            for block in colision:
                block.blood -= self.lethality
                if block.blood <= 0: self.world.score += block.point
            
            self.kill()
        
        #hit enemy
        colision_list = self.find_colision(self.world.entities.values())
        if colision_list != []:
            
            for thing in colision_list:
                # if thing in self.world.players: continue
                if thing == self.player: continue
                else:
                    thing.get_hurt(self.lethality,self.direction)
                    if self.weapon in ('mine','grenade','RPG'):
                        self.explosion(self.location,'fragmentation')
                    self.kill()
                    break


    def explosion(self, center, kind):

        tmp = (self.location[0],self.location[1])

        for angle in range (0, 360, 10):

            # bullet = Bullet(self.world, tmp, self.rotate(angle), 'fragmentation')
            bullet = Bullet(self.player,self.world, tmp, self.rotate(angle), 'fragmentation')
            self.world.bullets.add(bullet)
            # print(self.world.bullets)
        # self.kill()
    
    def rotate(self, angle):

        theta = angle * math.pi / 180
        x = self.direction.x * math.cos(theta) - self.direction.y * math.sin(theta)
        y = self.direction.x * math.sin(theta) + self.direction.y * math.cos(theta)
        return Vec2d(x, y)
    
    def draw(self,surface):
        # print('5ok')
        x,y = self.location
        #w,h = self.image.get_size()
        surface.blit(self.surf, (x - self.w/2, y - self.h/2))
    

    