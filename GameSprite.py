'''
this is the fundamental class of all entities in the game,
they all share the colision funtion with other entities, groups, or other.
All class we use later, such as Enemy, Player, Bullet, Block come from here.
'''

import pygame
from pygame.locals import *
from Vec2d import *

class GameSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    
    def check_colide(self,obj):#
        if isinstance(self,Vec2d):
            dis = obj.location - self.location
            dis_x,dis_y = abs(dis.x),abs(dis.y)
            if 0 <= 2*dis_x <= self.w + obj.w and 0 <= 2*dis_y <= self.h + obj.h:
                return True
            else: return False
        
        else:   #especially for bullets
            location = Vec2d(*self.location)
            dis = obj.location - location
            dis_x,dis_y = abs(dis.x),abs(dis.y)
            if 0 < 2*dis_x < self.w + obj.w and 0 < 2*dis_y < self.h + obj.h:
                return True
            else: return False
        '''
        if obj.location.x-obj.w/2-self.w/2<self.location.x<obj.location.x+obj.h/2+self.w/2:
            if obj.location.y-self.h/2-obj.h/2<self.location.y<obj.location.y+self.h/2+obj.h/2:
                return True'''
    
    def check_groupcolide(self,group):
        for entity in group:
            if self.check_colide(entity):
                return True
        return False

    def colide_with_entity(self,entity):
        #one cannot move;
        # self.blood -= entity.lethality
        # entity.blood -= self.lethality
        dis = entity.location - self.location
        if abs(dis.x) >= abs(dis.y):     #找比較長的，如果比較短的有發生碰撞，迴圈根本輪不到長的
            
            if 0 <= dis.x <= entity.w/2 + self.w / 2:          #you cannot move right
                self.location.x = entity.location.x - entity.w/2 -  self.w / 2
            elif - entity.w/2 -  self.w / 2 < dis.x <= 0 :    #your cannot move left
                self.location.x = entity.location.x + entity.w/2 + self.w / 2
        
        elif abs(dis.x)<abs(dis.y):
           
            if 0 <= dis.y <= entity.h/2 + self.h / 2:          #you cannot move down
                self.location.y = entity.location.y - entity.h/2 -  self.h / 2
            elif - entity.h/2 -  self.h / 2 <= dis.y <= 0:     #you cannot move up
                self.location.y = entity.location.y + entity.h/2 + self.h / 2
    
        
    def colide_with_group(self,group_list):
        for entity in group_list:
            
            if self.check_colide(entity): 
                self.colide_with_entity(entity)
                return
            else: continue
    
    def find_colision(self,group):
        colision = []
        for entity in group:
            if self.check_colide(entity):
                colision.append(entity)
        return colision
    
    