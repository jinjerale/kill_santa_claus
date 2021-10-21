#World

import pygame
#from pygame.locals import *
#from Vec2d import *
#from bullet_0102 import *
from player1 import *
from ref import resource_path
from player2 import *
from Block import *
from zombie import *
from AC import *
import Generator

# revision: determine whether zombie all die
    
class World:

    def __init__(self, screen, Pnum ,LAND = None, friend = True, mode = 1):

        self.Pnum = Pnum
        
        #the input LAND is a int from 1 to 3, which determine the venue
        self.land_num = LAND
        if LAND == 1:  self.land = Venue1()
        elif LAND == 2:  self.land = Venue2()
        elif LAND == 3: self.land = Venue3()
        else: self.land = LAND

        self.friend = friend
        self.mode = mode
        self.level = 0
        self.new_challenge = False
    
        self.entities = {}
        self.entity_id = 0
        #group names
        self.players = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.explosives = pygame.sprite.Group()
        self.AC_group = pygame.sprite.Group()
        self.gifts = pygame.sprite.Group()
        
        # self.background = pygame.Surface(screen.get_size())
        # self.background.fill((0,0,0))
        self.background = pygame.image.load(resource_path('./_data/back/background.png')).convert_alpha()

        self.score = 0

    
    def add_entity(self, entity):
        
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1
        
    
    def remove_entity(self, entity):
        
        del self.entities[entity.id]
    
    def get(self, entity_id):

        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None
    
    def update(self, time_passed_seconds):
        
        self.land.block_group.update()

        #zombies
        for entity in self.entities.values():
            entity.update(time_passed_seconds)

        
        
        for bullet in self.bullets:
            
            bullet.update(time_passed_seconds)
        # print(self.bullets)    # problem: shooter hit itself
        
        for explosive in self.explosives:            
            
            explosive.update(time_passed_seconds)  

        self.AC_group.update(time_passed_seconds) 

        self.gifts.update(time_passed_seconds)         
            



    def draw(self, surface):
        #draw background black
        surface.blit(self.background, (0, 0))
        #draw venue
        self.land.draw(surface)
        
        #draw entities        
        for entity in self.entities.values():
            entity.draw(surface)
    
        # print(self.bullets)
        for bullet in self.bullets:
            bullet.draw(surface)
        
        for explosive in self.explosives:
            explosive.draw(surface)
        
        for box in self.AC_group:
            box.draw(surface)
        
        for gift in self.gifts:
            gift.draw(surface)
        
        font = pygame.font .Font(None, 30)
        Text = font.render('Score: %d, Level: %d'% (self.score,self.level), True, (255,255,255))
        surface.blit(Text,(300,50))


    
    def get_close_entity(self, name, location, range=100.):
        location = Vec2d(*location)
        for entity in self.entities.values():
            if entity.name == name:
                distance = location.get_distance(entity.location)
                if distance < range:
                    return entity
        return None
    
    def clean_dead(self):
        
        dead_list = []
        trans_list = []
        for entity in self.entities.values():
            if entity.blood <= 0:
                # rezombie explode when dead
                if entity.name == 're_zombie':
                    explosives = Explosives(entity.world,entity.location, Vec2d(0,1))
                    explosives.explosion(entity.location)
                    try:
                        player = entity.world.get(entity.player_id)
                        if player is None:
                            pass
                        else:
                            player.get_hurt(entity.lethality, entity.direction)
                            if player.blood <= 0:
                                entity.brain.active_state.got_kill = True
                    except AttributeError:pass
                    dead_list.append(entity)
                    wa = waZombie(self, entity.direction_name, self.mode)
                    wa.location = deepcopy(entity.location)
                    trans_list.append(wa)
                                    
                # entity.kill()
                else: dead_list.append(entity)
        
        for i in dead_list:
            self.remove_entity(i)
            i.kill()
        for i in trans_list:
            
            self.add_entity(i)
    
    def game_over(self):
        return len(self.players) == 0


    def challenge_clear(self):
        return len(self.entities) == len(self.players)

    
