import pygame
from ref import resource_path
from World import *
from Generator import *

# from pygame.locals import *
# from Vec2d import *
from sys import exit
# from bullet_2019 import *
# from player1_2019 import *
# from player2_2019 import *
# from Block import *


pygame.init()  
screen_width = 800
screen_height = 600
up = (714, 75)
down = (714, 113)
left = (624, 27)
right = (660, 27)
degree = (710, 175)
x, y = 100, 75


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kill Santa Claus")
clock = pygame.time.Clock()
p1_image = pygame.image.load(resource_path('./_data/player/p1.png')).convert_alpha()
p2_image = pygame.image.load(resource_path('./_data/player/p2.png')).convert_alpha()
over_image = pygame.image.load(resource_path('./_data/grey/over.png')).convert_alpha()

menu_image = pygame.image.load(resource_path('./_data/grey/Fong.png')).convert_alpha()
teach_image = pygame.image.load(resource_path('./_data/grey/intro.png')).convert_alpha()

p1land1_image = pygame.image.load(resource_path('./_data/land/p1l1.png')).convert_alpha()
p1land2_image = pygame.image.load(resource_path('./_data/land/p1l2.png')).convert_alpha()
p1land3_image = pygame.image.load(resource_path('./_data/land/p1l3.png')).convert_alpha()
p2land1_image = pygame.image.load(resource_path('./_data/land/p2l1.png')).convert_alpha()
p2land2_image = pygame.image.load(resource_path('./_data/land/p2l2.png')).convert_alpha()
p2land3_image = pygame.image.load(resource_path('./_data/land/p2l3.png')).convert_alpha()

up_blue_image = pygame.image.load(resource_path('./_data/choose/up_blue.png')).convert_alpha()
up_red_image = pygame.image.load(resource_path('./_data/choose/up_red.png')).convert_alpha()
up_gray_image = pygame.image.load(resource_path('./_data/choose/up_gray.png')).convert_alpha()
down_blue_image = pygame.image.load(resource_path('./_data/choose/down_blue.png')).convert_alpha()
down_red_image = pygame.image.load(resource_path('./_data/choose/down_red.png')).convert_alpha()
down_gray_image = pygame.image.load(resource_path('./_data/choose/down_gray.png')).convert_alpha()
left_red_image = pygame.image.load(resource_path('./_data/choose/left_red.png')).convert_alpha()
left_blue_image = pygame.image.load(resource_path('./_data/choose/left_blue.png')).convert_alpha()
left_gray_image = pygame.image.load(resource_path('./_data/choose/left_gray.png')).convert_alpha()
right_red_image = pygame.image.load(resource_path('./_data/choose/right_red.png')).convert_alpha()
right_blue_image = pygame.image.load(resource_path('./_data/choose/right_blue.png')).convert_alpha()
right_gray_image = pygame.image.load(resource_path('./_data/choose/right_gray.png')).convert_alpha()

easy_image = pygame.image.load(resource_path('./_data/choose/easy_50.png')).convert_alpha()
medium_image = pygame.image.load(resource_path('./_data/choose/medium_50.png')).convert_alpha()
hard_image = pygame.image.load(resource_path('./_data/choose/hard_50.png')).convert_alpha()

p1images = [p1land1_image, p1land2_image, p1land3_image]
p2images = [p2land1_image, p2land2_image, p2land3_image]
degree_images = [easy_image, medium_image ,hard_image]





def GenerWorld(Prum,MapChoose,Friend=None,Mode=None):
    
    clock = pygame.time.Clock()
    
    #generate 1p, world = Venue2    
    world = World(screen,Prum,MapChoose)
    generator = Generator(world,Mode)# ,wa_image,re_image,santa_image
    
    p1 = Player1(world,p1_image)
    world.add_entity(p1)


    if world.Pnum == 2:
        p2 = Player2(world,p2_image)
        world.add_entity(p2)

    #it need improve

    while True:
        
        for event in pygame.event.get():

            if event.type == QUIT:
                exit() 

            elif pygame.key.get_pressed()[K_ESCAPE]:
                
                return world.score

        time_passed = clock.tick(30)
        time_passed_seconds = time_passed / 1000 
        
        # all things in the world update
        if world.new_challenge:
            
            generator.generate_enemy(world.level,time_passed_seconds)
            
            
        world.update(time_passed_seconds)
        world.clean_dead()
        
        
        # all thing in the world draw on the screen
        world.draw(screen)
        
        if world.game_over():
            return world.score
        if world.challenge_clear() and not world.new_challenge:
            
            world.level+=1
            if world.level >= 8: return world.score
            else:
                for i in range(generator.ACs[world.level]):
                    generator.generate_AC()
                generator.update_level(world.level)
                world.new_challenge = True
        
                if len(world.players) < world.Pnum :
                    for sirvivor in world.players:
                        if isinstance(sirvivor,Player2):
                            p1 = Player1(world,p1_image)
                            world.entities[0] = p1
                            p1.id = 0
                        elif isinstance(sirvivor, Player1):
                            p2 = Player2(world,p2_image)
                            world.entities[1] = p2
                            p2.id = 1
                        
                        
                
            
        
        pygame.display.flip()
    
def show_score(score,surface):
    
    clock = pygame.time.Clock()
    timer = 0
    
    # background = pygame.Surface(surface.get_size())
    over_image.set_alpha(400)
    # background.fill((200,200,200))

    while True:
        
        time_passed = clock.tick(30)
        time_passed_seconds = time_passed / 1000 
        
        # operation
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif pygame.key.get_pressed()[K_RETURN]:
                return
        
        # screen display
        

        surface.blit(over_image,(0,0))
        
        font1 = pygame.font .Font(None, 60)
        font2 = pygame.font .Font(None, 40)
        
        Text1 = font1.render('Your Score: %d'% score, True, (255,255,255))
        surface.blit(Text1,(200,200))
        
        if score < 60:
            Text2 = font2.render('Sorry, see you next semester',True,(250,250,250))
        elif score < 70:
            Text2 = font2.render('You can get a C',True,(250,250,250))
        elif score < 80:
            Text2 = font2.render('You can get a B',True,(250,250,250))
        elif score < 90:
            Text2 = font2.render('You can get a A',True,(250,250,250))
        elif score < 90:
            Text2 = font2.render('You can get a A+',True,(250,250,250))
        elif score > 100:
            Text2 = font2.render('TA is handsome!',True,(250,250,250))
    
        surface.blit(Text2,(200,270))
        
        # shining text
        timer += time_passed_seconds
        if timer >= 0.3:
            timer -= 0.5
            pass
        else:
            Text3 = font2.render('click ENTER to Menu.',True,(250,250,250))
            surface.blit(Text3,(200,400))

        
        pygame.display.flip()
def draw(surface, p1land_images, p2land_images, degree_images , player_num, land_num, nd, key):

    screen.fill((40, 40, 40))
    initial = 0

    if key == 'no':
        surface.blit(up_gray_image, up)
        surface.blit(down_gray_image, down)
        surface.blit(left_gray_image, left)
        surface.blit(right_gray_image, right)

    if key == 'up':
        surface.blit(up_red_image, up)
        surface.blit(down_blue_image, down)
        surface.blit(left_gray_image, left)
        surface.blit(right_gray_image, right)

    if key == 'down':
        surface.blit(up_blue_image, up)
        surface.blit(down_red_image, down)
        surface.blit(left_gray_image, left)
        surface.blit(right_gray_image, right)
    
    if key == 'left':
        surface.blit(up_gray_image, up)
        surface.blit(down_gray_image, down)
        surface.blit(left_red_image, left)
        surface.blit(right_blue_image, right)
        

    if key == 'right':
        surface.blit(up_gray_image, up)
        surface.blit(down_gray_image, down)
        surface.blit(left_blue_image, left)
        surface.blit(right_red_image, right)

    if key == 'space':
        surface.blit(up_gray_image, up)
        surface.blit(down_gray_image, down)
        surface.blit(left_gray_image, left)
        surface.blit(right_gray_image, right)
        surface.blit(degree_images[nd], degree)
        memory = nd

    if key != 'space':
        surface.blit(degree_images[initial], degree)
    
    if player_num == 0:
        picture = p1land_images[land_num]

    if player_num == 1:
        picture = p2land_images[land_num]

    surface.blit(picture, (x, y))
    pygame.display.update()


def Menu(surface ,images1, images2, images3):

    player_num = [1, 2]
    maps = [1, 2, 3]
    modes = [1, 2, 3]
    c1, c2, c3, c4 = 0, 0, 0 ,0
    run1, run2, run3 ,run4 = True, True, True, True
    mapisselected = False
    p1land_images = images1
    p2land_images = images2
    degree_images = images3

    while run1:
 
        surface.blit(menu_image, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == QUIT:
                # run1 = False
                # run2 = False
                # run3 = False
                # run4 = False
                exit()

            elif event.type == KEYDOWN:
                
                if event.key == K_RETURN:
                    run1 = False

    while run2:

        screen.fill((40, 40, 40))
        surface.blit(p1land1_image, (x, y))
        surface.blit(up_gray_image, up)
        surface.blit(down_gray_image, down)
        surface.blit(left_gray_image, left)
        surface.blit(right_gray_image, right)
        surface.blit(easy_image, degree)
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == QUIT:
                run2 = False
                run3 = False
                run4 = False
                exit()

            if event.type == KEYDOWN:
                run2 = False

    while run3:

        if not mapisselected:

            for event in pygame.event.get():

                if event.type == QUIT:
                    run3 = False
                    run4 = False
                    exit()

                if event.type == KEYDOWN:
                    
                    key = 'no'

                    if event.key == K_LEFT:
                        c1 = (c1 - 1) % len(player_num)
                        key = 'left'

                    elif event.key == K_RIGHT:
                        c1 = (c1 + 1) % len(player_num)
                        key = 'right'

                    if event.key == K_UP:
                        c2 = (c2 + 1) % len(maps)
                        key = 'up'

                    elif event.key == K_DOWN:
                        c2 = (c2 - 1) % len(maps)
                        key = 'down'
                    
                    if event.key == K_SPACE:
                        c3 = (c3 + 1) % len(modes)
                        key = 'space'
                    
                    elif event.key == K_RETURN:
                        mapisselected = True
                        Prum = player_num[c1]
                        land = maps[c2] 
                        mode = modes[c3] 
                        run3 = False

                    draw(surface, p1land_images, p2land_images, degree_images, c1, c2, c3, key)

    while run4:
        screen.fill((0, 0, 0))
        surface.blit(teach_image, (0,0))
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == QUIT:
                run4 = False
                exit()

            elif event.type == KEYDOWN :

                if event.key == K_RETURN:
                    return [Prum, land, True, mode]
                    run4 = False

def run():
    while True:
        finalchoice = Menu(screen ,p1images, p2images, degree_images)
        score = GenerWorld(finalchoice[0], finalchoice[1], finalchoice[2], finalchoice[3])
        show_score(score,screen)

# print('gameover')
run()
exit()
# world.__init__(self, screen, Pnum ,LAND = None, friend = True, mode = 'easy')