import pygame
from pygame.locals import *
from Vec2d import *
from bullet import *
from player1 import *

screen_width = 800
screen_height = 600

class Player2(Player1):

    def __init__(self, world, image = None):


        Player1.__init__(self,world,image)
        self.location = (520,300)
        self.world.players.add(self)

    def get_key(self):
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[K_UP], pressed_keys[K_DOWN],pressed_keys[K_LEFT],pressed_keys[K_RIGHT],pressed_keys[K_COMMA],pressed_keys[K_SLASH],pressed_keys[K_PERIOD]  


    def colide_with_p1(self):
        try:
            self. colide_with_entity(self.world.entities[0])
        except KeyError:
            pass
    