import pygame
from pygame.locals import *
from Vec2d import *
from random import randint
from zombie import *
from AC import *
# from World_0102 import *

'''
in order to generate enemies and zombies with respects to game,
we need to know whether the enemies is over.
this class take world information ,and update itself.
'''


class Generator:
    # ,wa_image,re_image,santa_image
    def __init__(self,world,Mode):
        self.world = world
        self.timer = 0
        self.pause = 5
        
        self.mode = Mode

        self.wa_num = 0
        self.re_num = 0
        self.santa_num = 0

        self.Enemies = ((0, 0, 0), (5, 0, 0), (9, 1, 0) ,(10, 5, 0), (0, 10, 0), (4, 10, 1), (0, 10, 2), (0, 0, 5))
        self.ACs = (0, 0, 4, 4, 4, 8, 8, 8)
    '''
    def update(self, time_passed_seconds):

        if self.world.challenge_clear():
            # self.world.level += 1
            print(self.world.level)
            self.generate_enemy(time_passed_seconds) '''
    
    def generate_enemy(self,level,time_passed_seconds):
        
        # generate enemies every certain time
        
        self.timer += time_passed_seconds
        if self.timer >= self.pause:
            
            gener_wa = randint(0,self.wa_num)
            gener_re = randint(0,self.re_num)
            gener_santa = randint(0,self.santa_num)
            
            for i in range(gener_wa):
                wa = waZombie(self.world,'left', self.mode)#,self.wa_image
                self.gener_spot(wa)
                self.world.add_entity(wa)
            
            for i in range(gener_re):
                re = reZombie(self.world,'left', self.mode)# ,self.re_image
                self.gener_spot(re)
                self.world.add_entity(re)
            
            for i in range(gener_santa):
                santa = Santa_claus(self.world,'left', self.mode)#,self.santa_image
                self.gener_spot(santa)
                self.world.add_entity(santa)
            
            self.wa_num -= gener_wa
            self.re_num -= gener_re
            self.santa_num -= gener_santa
            self.timer = 0

            if self.wa_num == self.re_num ==  self.santa_num == 0:
                self.world.new_challenge = False
            # except TypeError: pass

    def generate_AC(self):
        
        ac = AC_box(self.world)
        self.world.AC_group.add(ac)

    def update_level(self,level):
        self.wa_num,self.re_num,self.santa_num = self.Enemies[level]
    # enemy generate(WA,RE,SANTA)

    
    # give zombies its location and direction with respect to the Venue
    def gener_spot(self,zombie):
        
        if self.world.land_num == 1:
            # left or right,left is 0,1,2 and right is 3,4 
            rand = randint(0,1)
            rand2 = randint(0,2)
            if rand == 0:
                zombie.direction_name = 'left'
                if rand2 == 0:
                    zombie.location = Vec2d(0,randint(60,140))
                else:
                    zombie.location = Vec2d(0,randint(220,540))
            elif rand == 1:
                zombie.direction_name = 'right'
                if rand2 == 0:
                    zombie.location = Vec2d(800,randint(60,140))
                elif rand2 == 1:
                    zombie.location = Vec2d(800,randint(220,380))
                elif rand2 == 2:
                    zombie.location = Vec2d(800,randint(460,540))
        
        elif self.world.land_num == 2:
            # left or right,left is 0,and right is 1,up is 2,down is 3
            rand = randint(0,3)
            if rand == 0:
                zombie.direction_name = 'left'
                zombie.location = Vec2d(0,randint(0,600))
            elif rand == 1:
                zombie.direction_name = 'right'
                zombie.location = Vec2d(800,randint(0,600))
            elif rand == 2:
                zombie.direction_name = 'up'
                zombie.location = Vec2d(randint(0,800),600)
            elif rand == 3:
                zombie.direction_name = 'down'
                zombie.location = Vec2d(randint(0,800),0)

        elif self.world.land_num == 3:

            rand = randint(0,3)
            if rand == 0:
                zombie.direction_name = 'left'
                zombie.location = Vec2d(0,randint(260,340))
            elif rand == 1:
                zombie.direction_name = 'right'
                zombie.location = Vec2d(800,randint(260,340))
            elif rand == 2:
                zombie.direction_name = 'up'
                zombie.location = Vec2d(randint(340,460),600)
            elif rand == 3:
                zombie.direction_name = 'down'
                zombie.location = Vec2d(randint(340,460),0)
        
        else:raise TypeError('only 1 to 3')

    # do this when generating enemies,put a zombie in this function,
    # and it gives them their initial location and direction

        
        

    
    
