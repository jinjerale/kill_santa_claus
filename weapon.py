import pygame
from pygame.locals import *
from Vec2d import *
from pygame.time import *
from copy import deepcopy

from bullet import *
import math



clock = pygame.time.Clock()

#the collection of guns,initaite when player is generate

# change: shotgun split after shoot
class Weapon():

    def __init__(self, player):

        # self.player = player 
        self.player = player
        self.world = player.world
        self.location = player.location
        self.direction = player.direction
        self.what_in_hand = player.what_in_hand

        # self.shoot_sound = shoot_sound
        '''
        self.gun_num = 0
        self.weapons = ['pistal', 'machine_gun', 'shotgun','grenade', 'mine', 'RPG']
        self.what_in_hand = 'pistal'
        '''
        
        # the cool down time each bullet is released
        # self.gun_cd()
        # self.timer = 0
    '''    
    def gun_cd(self):

        if self.what_in_hand == 'pistal':
            self.cd_time = 0.5

        elif self.what_in_hand == 'machine_gun':
            self.cd_time = 0.1
        
        elif self.what_in_hand == 'shotgun':
            self.cd_time = 0.3
        
        elif self.what_in_hand == 'grenade':
            self.cd_time = 1.5

        elif self.what_in_hand == 'mine':
            self.cd_time = 2
            
        elif self.what_in_hand == 'RPG':
            self.cd_time = 0.7 
    '''
    '''
    def update(self,time_passed_seconds):
        
        self.location = self.player.location
        self.direction = self.player.direction
        self.timer += time_passed_seconds
        self.timer = min(self.timer,self.cd_time)
        
    
    def is_cool_down(self):
        return self.timer >= self.cd_time
    '''
    def fire(self, time_passed_seconds):

        #tmp = (self.location[0],self.location[1])
        tmp = deepcopy(self.location)
        # get print('fire')
        bullet = Bullet(self.player,self.world, tmp, self.direction, self.what_in_hand)
        self.world.bullets.add(bullet)
        # self.play_sound()
        '''
        if self.what_in_hand != 'shotgun':
            # get print('bullet')
            bullet = Bullet(self.player,self.world, tmp, self.direction, self.what_in_hand)
            self.world.bullets.add(bullet)
            # print(self.world.bullets)
        
        elif self.what_in_hand == 'shotgun':
            n = 5
            for angle in range (0,360,10):

                bullet = Bullet(self.player,self.world, tmp, self.rotate(angle), self.what_in_hand)
                
                self.world.bullets.add(bullet)
                # print(self.world.bullets)'''
        
        self.timer = 0
    
    def rotate(self, angle):

        theta = angle * math.pi / 180
        x = self.direction.x * math.cos(theta) - self.direction.y * math.sin(theta)
        y = self.direction.x * math.sin(theta) + self.direction.y * math.cos(theta)
        return Vec2d(x, y)
    '''
    def play_sound(self):
        """这个就是播放声音的函数"""
        channel = self.shoot_sound.play()
 
        if channel is not None:
            # 设置左右声道的音量
            left, right = stero_pan(self.position.x, SCREEN_SIZE[0])
            channel.set_volume(left, right)

    def stero_pan(self, screen_width):
        """这个函数根据位置决定要播放声音左右声道的音量"""
        right_volume = self.location.x / 800
        left_volume = 1.0 - right_volume
        return (left_volume, right_volume)'''

'''    def changegun1(self):#gun_num += 1
        self.gun_num += 1
        self.gun_num = self.gun_num % len(self.weapons)
        self.what_in_hand = self.weapons[self.gun_num]

    def changegun2(self):#gun_num -= 1
        self.gun_num -= 1
        self.gun_num = self.gun_num % len(self.weapons)
        self.what_in_hand = self.weapons[self.gun_num]'''