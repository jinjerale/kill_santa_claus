import pygame
from ref import resource_path
from pygame.locals import *
from Vec2d import *
from random import randint

#from bullet_0102 import *
#from weapon_0102 import *
from GameSprite import *

class AC_box(GameSprite):
    
    
    
    def __init__(self,world):
        
        GameSprite.__init__(self)
        
        self.world = world
        self.level = self.world.level
        self.gener_list()   # generate weapon list with respect to level

        self.image = pygame.image.load(resource_path('./_data/AC/AC.png')).convert_alpha()
        self.w,self.h = self.image.get_size()
        self.location = Vec2d(randint(150,650),randint(100,500))
        while self.check_groupcolide(self.world.land.block_group):
            self.location = Vec2d(randint(100,700),randint(100,500))
        self.contain = self.weapon_list[randint(0,len(self.weapon_list)-1)]
        self.plus_blood = 10

    def gener_list(self):# generate when challenge clear
        _level_ = ( 
            None,
            None,
            (('machine_gun',20), ('shotgun',10)),
            (('machine_gun',20), ('shotgun',10)),
            (('machine_gun',30),('shotgun',15),('grenade',5)),
            (('machine_gun',30), ('shotgun',15),('grenade',10), ('mine',5)),
            (('machine_gun',30), ('shotgun',15),('grenade',10), ('mine',5), ('RPG',2)),
            (('machine_gun',40), ('shotgun',20),('grenade',15), ('mine',10), ('RPG',5))
        
        )
        self.weapon_list =  _level_[self.level]
    
    def update(self,time_passed_seconds):
        colision_list = self.find_colision(self.world.entities.values())
        if colision_list != []:
            
            for thing in colision_list:
                if thing in self.world.players: 
                    thing.get_heal(self.contain,self.plus_blood)
                    self.kill()
                else:
                    
                    self.kill()
    
    def draw(self,surface):
        x,y = self.location
        surface.blit(self.image, (x - self.w/2, y - self.h/2))
        
        font = pygame.font .Font(None, 15)
        Text = font.render('AC', True, (255,255,255))
        surface.blit(Text,(x-5,y-25))