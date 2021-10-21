import pygame
from ref import resource_path
from pygame.locals import *
from Vec2d import *
from random import randint, choice
from GameSprite import *
from copy import deepcopy
#import random


class State(object):
    def __init__(self, name):
        self.name = name
    def do_actions(self):
        pass
    def check_conditions(self):
        pass
    def entry_actions(self):
        pass
    def exit_actions(self):
        pass        

class StateMachine(object):
    def __init__(self):
        self.states = {}
        self.active_state = None
 
    def add_state(self, state):
        self.states[state.name] = state
 
    def think(self):
        if self.active_state is None:
            self.active_state = self.states["exploring"]
        self.active_state.entry_actions()
        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)

    def set_state(self, new_state_name):
        # if self.active_state is not None:
        #     self.active_state.exit_actions()
        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()
 
class GameEntity(GameSprite):
 
    def __init__(self, world, name):
     
        GameSprite.__init__(self)
        self.world = world
        self.name = name
        
        self.location = Vec2d(0, 0)
        self.destination = Vec2d(0, 0)
        self.direction = Vec2d(0,0)
        self.speed = 0.
        self.brain = StateMachine()
        self.id = 0
 
    def draw(self, surface):
        x, y = self.location
        #w, h = self.image.get_size()
        surface.blit(self.image, (x-self.w/2, y-self.h/2)) 
        font = pygame.font .Font(None, 15)
        gunText = font.render(self.name, True, (255,255,255))
        surface.blit(gunText,(x-25,y-25))  
 
    def update(self, time_passed):
        self.brain.think()
        if self.speed > 0. and self.location != self.destination:
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.get_length()
            self.direction = vec_to_destination.normalized()
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            self.location += travel_distance * self.direction
        self.change_dir_if_colide(self.world.land.block_group)
    
    def change_dir_if_colide(self,group):
        for entity in group:
            if self.check_colide(entity):
                dis = entity.location - self.location
                if abs(dis.x) > abs(dis.y):     #找比較長的，如果比較短的有發生碰撞，迴圈根本輪不到長的
                    
                    if 0 < dis.x < entity.w/2 + self.w / 2:          #you cannot move right
                        if self.brain.active_state.name == "exploring":
                            self.location.x = entity.location.x - entity.w/2 -  self.w / 2
                            self.direction_name, self.destination = self.which_dir()
                        else:
                            self.location.x = entity.location.x - entity.w/2 -  self.w / 2
                    elif - entity.w/2 -  self.w / 2 < dis.x < 0 : #your cannot move left
                        if self.brain.active_state.name == "exploring":   
                            self.location.x = entity.location.x + entity.w/2 +  self.w / 2
                            self.direction_name, self.destination = self.which_dir()
                        else:
                            self.location.x = entity.location.x + entity.w/2 + self.w / 2
                
                elif abs(dis.x)<abs(dis.y):
                
                    if 0 < dis.y < entity.h/2 + self.h / 2:          #you cannot move down
                        if self.brain.active_state.name == "exploring":   
                            self.location.y = entity.location.y - entity.h/2 -  self.h / 2
                            self.direction_name, self.destination = self.which_dir()
                            
                        else:
                            self.location.y = entity.location.y - entity.h/2 -  self.h / 2
                    elif - entity.h/2 -  self.h / 2 < dis.y < 0:     #you cannot move up
                        if self.brain.active_state.name == "exploring":   
                                self.location.y = entity.location.y + entity.h/2 +  self.h / 2
                                self.direction_name, self.destination = self.which_dir()
                                
                        else:
                            self.location.y = entity.location.y + entity.h/2 +  self.h / 2
                
                #self.direction.x,self.direction.y = self.direction.y, self.direction.x
                return
    
    def get_hurt(self,lethality,direction):
        self.blood -= lethality
        self.location += 10 * direction
        if self.blood <= 0:
            self.world.score += self.point
    
    def which_dir(self):
        lis = ["right","left","up","down"]
        lis.remove(self.direction_name)
        x = choice(lis)
        if x == "left":
            y = Vec2d(0,deepcopy(self.location.y))
        elif x == "right":
            y = Vec2d(800,deepcopy(self.location.y))
        elif x == "up":
            y = Vec2d(deepcopy(self.location.x), 0)
        elif x == "down":
            y = Vec2d(deepcopy(self.location.x), 600)
        return x, y 

        

class waZombie(GameEntity):
    def __init__(self, world, direction_name, difficulty):
        GameEntity.__init__(self, world, "wa_zombie")
        exploring_state = zombieStateExploring(self)
        seeking_state = zombieStateSeeking(self)
        hunting_state = zombieStateHunting(self)
        self.brain.add_state(exploring_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(hunting_state)
        self.direction_name = direction_name
        self.image = pygame.image.load(resource_path('./_data/enemy/wa.png')).convert_alpha()
        self.w,self.h = self.image.get_size()
        
        self.speed = 30
        self.blood = 30*(1+difficulty/3)
        self.point = 1
        self.lethality = 1

    def draw(self, surface):
        GameEntity.draw(self, surface)

class reZombie(GameEntity):
    def __init__(self, world, direction_name, difficulty):
        GameEntity.__init__(self, world, "re_zombie")
        exploring_state = zombieStateExploring(self)
        seeking_state = zombieStateSeeking(self)
        hunting_state = zombieStateHunting(self)
        self.brain.add_state(exploring_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(hunting_state)
        self.direction_name = direction_name

        self.image = pygame.image.load(resource_path('./_data/enemy/re.png')).convert_alpha()
        self.w,self.h = self.image.get_size()
        
        self.speed = 40
        self.blood = 30*(1+difficulty/3)
        self.point = 0
        self.lethality = 3

    def draw(self, surface):
        GameEntity.draw(self, surface)

class Santa_claus(GameEntity):
    def __init__(self, world, direction_name, difficulty):
        GameEntity.__init__(self, world, "santa_claus")
        exploring_state = zombieStateExploring(self)
        seeking_state = zombieStateSeeking(self)
        hunting_state = zombieStateHunting(self)
        self.brain.add_state(exploring_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(hunting_state)
        self.direction_name = direction_name
        self.number = 19

        self.image = pygame.image.load(resource_path('./_data/enemy/santa.png')).convert_alpha()
        self.w,self.h = self.image.get_size()

        self.speed = 60
        self.blood = 75*(1+difficulty/3)
        self.point = 5
        self.lethality = 5

    def draw(self, surface):
        GameEntity.draw(self, surface)
        
class zombieStateExploring(State):
    def __init__(self, zombie):
        State.__init__(self, "exploring")
        self.zombie = zombie
 
    # def random_destination(self):
    #     w, h = 800, 600
    #     self.zombie.destination = Vec2d(randint(0, w), randint(0, h)) 
    #     print(self.zombie.destination)
    #     print(self.zombie.location)   
 
    # def do_actions(self):
    #     self.random_destination()

    def check_conditions(self):
        player = self.zombie.world.get_close_entity("player", self.zombie.location, 200)
        if player is not None and self.zombie.location.get_distance(player.location) >= 1.:
            self.zombie.player_id = player.id
            return "seeking"
        # if player is not None and self.zombie.location.get_distance(player.location) < 1.:
        #     self.zombie.player_id = player.id
        #     return "hunting"
        return None
 
    def entry_actions(self):
        # self.zombie.speed = 40.
        if self.zombie.direction_name == "left":
            self.zombie.destination = Vec2d(0,self.zombie.location.y)
            if self.zombie.location ==Vec2d(0,self.zombie.location.y):#self.zombie.check_groupcolide(self.zombie.world.land.block_group) or
                self.zombie.direction_name = "right"
        elif self.zombie.direction_name == "right":
            self.zombie.destination = Vec2d(800,self.zombie.location.y)
            if self.zombie.location ==Vec2d(800,self.zombie.location.y):
                self.zombie.direction_name = "left"
        elif self.zombie.direction_name == "up":
            self.zombie.destination = Vec2d(self.zombie.location.x, 0)
            if self.zombie.location == Vec2d(self.zombie.location.x, 0):
                self.zombie.direction_name = "down"
        elif self.zombie.direction_name == "down":
            self.zombie.destination = Vec2d(self.zombie.location.x, 600)
            if self.zombie.location == Vec2d(self.zombie.location.x, 600):
                self.zombie.direction_name = "up"

class zombieStateSeeking(State):
    def __init__(self, zombie):
        State.__init__(self, "seeking")
        self.zombie = zombie
        self.player_id = None
 
    def check_conditions(self):
        player = self.zombie.world.get(self.zombie.player_id)
        if player is None:
            return "exploring"
        elif self.zombie.location.get_distance(player.location) >= 200 :
            return "exploring"
        elif self.zombie.name == "santa_claus" and self.zombie.location.get_distance(player.location) < 150.0:
            return "hunting"
        elif self.zombie.name != "santa_claus" and self.zombie.location.get_distance(player.location) < 15.0:
            return "hunting"
        return None
 
    def entry_actions(self):
        player = self.zombie.world.get(self.zombie.player_id)
        if player is not None:
            self.zombie.destination = player.location
            # self.zombie.speed = 40. 

class zombieStateHunting(State):
    def __init__(self, zombie):
        State.__init__(self, "hunting")
        self.zombie = zombie
        self.got_kill = False
 
    def do_actions(self):
        player = self.zombie.world.get(self.zombie.player_id)
        if player is None:
            return
        self.zombie.destination = player.location
        if self.zombie.name == "wa_zombie":

            player.get_hurt(self.zombie.lethality,self.zombie.direction)
            if player.blood <= 0:
                # self.zombie.world.remove_entity(player)
                self.got_kill = True
        
        elif self.zombie.name == "re_zombie":
            explosives = Explosives(self.zombie.world, self.zombie.location, Vec2d(0,1))
            explosives.explosion(self.zombie.location)
            
            player.get_hurt(self.zombie.lethality,self.zombie.direction)
            if player.blood <= 0:
                self.got_kill = True
            self.zombie.blood = 0
            # self.zombie.name = "wa_zombie"
        elif self.zombie.name == "santa_claus":
            if self.zombie.number % 20 == 0:
                tmp = deepcopy(self.zombie.location)
                p_l = deepcopy(player.location)
                gift = Gift(self.zombie.world, self.zombie, tmp, p_l)
                self.zombie.world.gifts.add(gift)
            self.zombie.number += 1
            if self.zombie.location.get_distance(player.location) < 15.0:
                player.get_hurt(self.zombie.lethality,self.zombie.direction)
                if player.blood <= 0:
                    # self.zombie.world.remove_entity(player)
                    self.got_kill = True
                
 
    def check_conditions(self):
        if self.got_kill:
            self.got_kill = False
            return "exploring"
        player = self.zombie.world.get(self.zombie.player_id)
        if player is None:
            return "exploring"
        if player.location.get_distance(self.zombie.location) >= 15.:
            return "seeking"
        else:
            return "exploring"
        return None
 
    def entry_actions(self):
        # self.speed = 40. 
        self.do_actions()
 
    # def exit_actions(self):
    #     self.got_kill = False

class Explosives(GameSprite):
    
    def __init__(self, world, location, direction, weapon = ''):

        # super(Explosives, self).__init__()
        #self.image = pygame.image.load()
        GameSprite.__init__(self)
        self.world = world
        self.size = 5
        self.surf = pygame.Surface((self.size, self.size))
        self.rect = self.surf.get_rect()
        self.location = location
        self.initial_location = location
        self.direction = direction
        self.weapon = weapon
        self.surf.fill((255, 0, 0))
        self.speed = 100
        self.range = 50
        self.lethality = 10

    def update(self, time_passed_seconds):
        
        if (self.location[0] - self.initial_location[0]) ** 2 + (self.location[1] - self.initial_location[1]) ** 2 < self.range ** 2:

            if 0 < self.location[0] < 800 and 0 < self.location[1] < 600:

                self.location += self.direction * self.speed * time_passed_seconds
                
            else:
                self.kill()
                return False
  
        else:
            self.kill()
            return False

    def explosion(self, center):
        #important
        tmp = (center[0], center[1])
        
        for angle in range (0, 360, 10):
            explosives = Explosives(self.world, tmp, self.rotate(angle), 'fragmentation')
            self.world.explosives.add(explosives)

    def rotate(self, angle):

        theta = angle * math.pi / 180
        x = self.direction.x * math.cos(theta) - self.direction.y * math.sin(theta)
        y = self.direction.x * math.sin(theta) + self.direction.y * math.cos(theta)
        return Vec2d(x, y)


    def draw(self,surface):

        x, y = self.location
        #w,h = self.image.get_size()
        surface.blit(self.surf, (x - self.size / 2, y - self.size / 2))

class Gift(GameSprite):
    def __init__(self, world, zombie, location, player_location):
        
        super(Gift, self).__init__()
        self.image = pygame.image.load(resource_path('./_data/enemy/gift.png')).convert_alpha()
        self.world = world
        self.range = 500
        self.speed = 150
        self.direction = (player_location - location).normalized()
        self.location = location
        self.initial_location = deepcopy(location)
        
        self.zombie = zombie
        if self.zombie.blood >= 50: self.lethality = 4
        elif self.zombie.blood < 50: self.lethality = 8
        
        self.w ,self.h = self.image.get_size()
        
    def update(self, time_passed_seconds):
        if (self.location[0] - self.initial_location[0]) ** 2 + (self.location[1] - self.initial_location[1]) ** 2 < self.range ** 2:

            if -50 < self.location[0] < 850 and -50 < self.location[1] < 650 and self.direction != Vec2d(0, 0):

                self.location += self.direction * self.speed * time_passed_seconds

            else:
                self.kill()
                return False
        
        else:
            self.kill()
            return False
        #hit blocks
        if self.check_groupcolide(self.world.land.block_group):
            colision = self.find_colision(self.world.land.block_group)
            for block in colision:
                block.blood -= self.lethality
            
            self.kill()
        
        #hit player(AOE)
        colision_list = self.find_colision(self.world.entities.values())
        if colision_list != []:
            
            for thing in colision_list:
                # if thing in self.world.players: continue
                if thing == self.zombie: continue
                else:
                    thing.get_hurt(self.lethality,self.direction)
                    self.kill()

    
    def draw(self, surface):
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x-w/2, y-h/2))   

