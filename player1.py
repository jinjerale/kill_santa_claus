import pygame
from pygame.locals import *
from Vec2d import *
#from copy import deepcopy

from bullet import *
from weapon import *
from GameSprite import *


screen_width = 800
screen_height = 600
# add gun changing time
class Player1(GameSprite):#  pygame.sprite.Sprite

    def __init__(self, world, image = None):
        
        GameSprite.__init__(self)
        # pygame.sprite.Sprite.__init__(self)
        # super(Player1, self).__init__()
        self.location = (280, 300)
        self.image = image
        self.w, self.h = self.image.get_size()
        
        self.world = world
        self.rect = self.image.get_rect()
        self.speed = 70
        self.direction = Vec2d(0, -1)

        
        #added
        self.blood = 45
        self.lethality = 0
        self.is_dead = False
        
        self.gun_num = 0
        self.what_in_hand = 'pistal'
        self.weapons = ['pistal']#], 'machine_gun', 'shotgun','grenade', 'mine', 'RPG']
        self.bags = {'pistal':'inf'}#, 'machine_gun':30, 'shotgun':5,'grenade':3, 'mine':3, 'RPG':1}
        self.gun_cd()
        self.changeguntime = 0.2
        self.timer = 0
        '''
        self.weapons = Weapon(self)
        '''
        self.name = "player"
        #added
        
        
        self.world.players.add(self)
        
    def get_key(self):
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[K_w], pressed_keys[K_s],pressed_keys[K_a],pressed_keys[K_d],pressed_keys[K_r],pressed_keys[K_y],pressed_keys[K_t]      

    def gun_cd(self):

        if self.what_in_hand == 'pistal': self.cd_time = 0.4

        elif self.what_in_hand == 'machine_gun': self.cd_time = 0.2
        
        elif self.what_in_hand == 'shotgun': self.cd_time = 0.5
        
        elif self.what_in_hand == 'grenade': self.cd_time = 1.5

        elif self.what_in_hand == 'mine': self.cd_time = 2
            
        elif self.what_in_hand == 'RPG': self.cd_time = 1 

    def weapons_update(self,time_passed_seconds):
        
        # self.location = self.player.location
        # self.direction = self.player.direction
        self.gun_cd()
        self.timer += time_passed_seconds
        self.timer = min(self.timer,self.cd_time)   
    
    def is_cool_down(self):
        return self.timer >= self.cd_time
    def can_change_gun(self):
        return self.timer >= self.changeguntime
    
    def update(self, time_passed_seconds):

        # self.weapons.update(time_passed_seconds)
        self.weapons_update(time_passed_seconds)

        pressed_keys = self.get_key()
        key_direction = Vec2d(0, 0)
        ### for moving
        if pressed_keys[0]:
            key_direction.y = -1

        elif pressed_keys[1]:
            key_direction.y = +1

        if pressed_keys[2]:
            key_direction.x = -1

        elif pressed_keys[3]:
            key_direction.x = +1
            #print(self.location)

        key_direction.normalized()
        if not key_direction == Vec2d(0,0):
            self.direction = key_direction
        
        ### for weapon
        if  pressed_keys[4]:
            if self.can_change_gun():
                self.changegun1()
                self.timer = 0


        elif pressed_keys[5]:#move to function
            if self.can_change_gun():
                self.changegun2()
                self.timer = 0
                
        
        if  pressed_keys[6]:
            if self.is_cool_down():
                weapon = Weapon(self)# , self.world, self.location, self.direction, self.what_in_hand
                weapon.fire(time_passed_seconds)
                try:
                    self.bags[self.what_in_hand] -= 1
                    
                    if self.bags[self.what_in_hand] <= 0:
                        self.bags.__delitem__(self.what_in_hand)
                        self.weapons.remove(self.what_in_hand)
                        self.changegun1()

                except Exception: pass
                self.timer = 0
            else: pass
        
        # get result
        self.location += key_direction * self.speed * time_passed_seconds        
        
        if self.location.x < self.w / 2: self.location.x = self.w / 2
        elif self.location.x > screen_width - self.w / 2: self.location.x = screen_width - self.w / 2
        if self.location.y < self.h / 2: self.location.y = self.h / 2
        elif self.location.y > screen_height - self.h / 2: self.location.y = screen_height - self.h / 2

        #the player cannot go through walls,this funtion is in line 86-112.
        self.colide_with_group(self.world.land.block_group)
        self.colide_with_p1()
        
    
    # move to weapon class
    '''def fire(self, time_passed_seconds):
        
        tmp = deepcopy(self.location)
        Bullet(self.world, tmp, self.direction)
    '''
    
    def draw(self, surface):
        
        x, y = self.location
        surface.blit(self.image, (x-self.w/2, y-self.h/2))
        
        #blood bar
        bar_x = x - 15
        bar_y = y - 25
        surface.fill( (230, 0, 0), (bar_x, bar_y, 30, 5))
        surface.fill( (0, 230, 0), (bar_x, bar_y, self.blood*2/3, 5))
        #gun in hand
        font = pygame.font .Font(None, 15)
        try: gunText = font.render('%s:%d'% (self.what_in_hand,self.bags[self.what_in_hand]), True, (255,255,255))
        except Exception:gunText = font.render(self.what_in_hand, True, (255,255,255))
        surface.blit(gunText,(bar_x,bar_y-15))
    
    def get_hurt(self,lethality,direction):
        self.blood -= lethality
        self.location += 10 * direction
        if self.blood <= 0:
            self.is_dead = True
    
    def get_heal(self,contain,plus):
        if contain[0] not in self.weapons: self.weapons.append(contain[0])
        self.bags[contain[0]] = self.bags.get(contain[0],0)+contain[1]
        self.blood = min(self.blood + plus, 45)
    
    def changegun1(self):#gun_num += 1
        self.gun_num += 1
        self.gun_num = self.gun_num % len(self.weapons)
        self.what_in_hand = self.weapons[self.gun_num]

    def changegun2(self):#gun_num -= 1
        self.gun_num -= 1
        self.gun_num = self.gun_num % len(self.weapons)
        self.what_in_hand = self.weapons[self.gun_num]

    def colide_with_p1(self):
        pass