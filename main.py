import random
from os import listdir # returns list of files
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE

pygame.init()

FPS = pygame.time.Clock()
screen =  width, height = 1000, 700

# Constants
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
player_color = [10,10,10]
background_color = (255, 255, 255)

font = pygame.font.SysFont('Verdana', 20)
main_surface = pygame.display.set_mode(screen)

IMGS_PATH = "sprites"

# Background related
bg = pygame.transform.scale(pygame.image.load(IMGS_PATH +'/'+ "Background_space.png").convert(), screen) # convert is used instead of convert_alpha, because picture dont have transparent elements
bgx = 0
bgx2 = bg.get_width()
bg_speed = 3

player_imgs = [pygame.image.load(IMGS_PATH +'/player/'+ file).convert_alpha() for file in listdir(IMGS_PATH +"/player")] # creates a list of images 
player = player_imgs[0]
player_img_index = 0
player_rect = player.get_rect()
player_rect.center = width//3, height//2 # start position
player_speed = 7
player_shields = 0
gun_cooldown = 1000 # ms
gun_ready = True

explosion_imgs = [pygame.image.load(IMGS_PATH +'/explosions/'+ file).convert_alpha() for file in listdir(IMGS_PATH +"/explosions")]


# Events
CREATE_ENEMY = pygame.USEREVENT+1
pygame.time.set_timer(CREATE_ENEMY, 1000)
CREATE_BONUS =  pygame.USEREVENT+2
pygame.time.set_timer(CREATE_BONUS, 3500)
CHANGE_IMG =  pygame.USEREVENT+3
pygame.time.set_timer(CHANGE_IMG, 150)
GUN_CD_EVENT = pygame.USEREVENT+4
pygame.time.set_timer(GUN_CD_EVENT, gun_cooldown)



# Data
enemies = []
bonuses = []
projectiles = []
explosions = []
scores = 0
ammo = 10
is_working = True


# Functions
def create_bonus():
    bonus = pygame.image.load(IMGS_PATH +'/'+"bonus.png").convert_alpha()
    bonus_rect = pygame.Rect(width+300, random.randint(0, height), *bonus.get_size())
    bonus_speed = 3
    return [bonus, bonus_rect, bonus_speed]

def create_enemy():
    enemy = pygame.image.load(f"{IMGS_PATH}/asteroid/asteroid-{str(random.randint(1,5))}.png").convert_alpha()
    enemy_size = random.randint(40, 200)
    enemy = pygame.transform.scale(enemy, (enemy_size, enemy_size))
    enemy_rect = pygame.Rect(width, random.randint(0, height), enemy_size, enemy_size)
    enemy_rect.inflate_ip(-enemy_size*0.2, -enemy_size*0.2 )
    
    enemy_speed = [random.randint(2,5),random.randint(-1,1)]
    return [enemy, enemy_rect, enemy_speed]

def shoot():
    projectile = pygame.Surface((10,5))
    projectile.fill((0, 255, 0))
    projectile_speed = [5,0]
    projectile_rect = projectile.get_rect()
    projectile_rect.x = player_rect.right - 20
    projectile_rect.y = player_rect.centery
    projectiles.append([projectile, projectile_rect, projectile_speed])
    global ammo 
    ammo -= 1
    # return [projectile, projectile_rect, projectile_speed]

# def explosion(center, size, speed):
#     explosion_frame = 1
#     explosion = pygame.image.load(IMGS_PATH +f'/explosions/explosion-{explosion_frame}.png')
#     explosion_rect = explosion.get_rect()
#     explosion_rect.center = center
#     explosion_rect.size = size
#     explosion_speed = speed
#     explosions.append([explosion, explosion_rect, explosion_speed, explosion_frame])
    


# Main cycle
while is_working:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False


        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())            
        if event.type == CREATE_BONUS:

            bonuses.append(create_bonus()) 
        if event.type == CHANGE_IMG:
            if player_img_index +1 > len(player_imgs):
                player_img_index = 0
            for expl in explosions:
                if expl[3]+1 <4:
                    expl[1] = explosion_imgs[expl[3]]
                    expl[3]+=1
                else:
                    expl[3] = 1
              
            player = player_imgs[player_img_index]
            player_img_index +=1      
        if event.type == GUN_CD_EVENT:
            gun_ready = True
            pygame.time.set_timer(GUN_CD_EVENT, 0)

    pressed_keys = pygame.key.get_pressed()

 
    #background movement & drawing
    # bg coords change
    bgx -= bg_speed
    bgx2 -= bg_speed

    # reset bg coords, when out of screen
    if bgx < -bg.get_width():
        bgx = bg.get_width()
    if bgx2 < -bg.get_width():
        bgx2 = bg.get_width()

    main_surface.blit(bg, (bgx,0))
    main_surface.blit(bg, (bgx2,0))

    # draw player, scores
    main_surface.blit(player, player_rect)

    main_surface.blit(font.render(str(scores), True, GREEN), (width- 40, 0))
    main_surface.blit(font.render(str(f"Ammo: {ammo}"), True, GREEN), (20, height-60))
    main_surface.blit(font.render(str(f"Shields: {player_shields}"), True, GREEN), (20, height-40))
    
    # enemies movement, drawing & collision
    for enemy in enemies:
        enemy[1]= enemy[1].move(-enemy[2][0], enemy[2][1])
        pygame.draw.rect(main_surface, (255, 0, 0), enemy[1]) # DRAW ENEMY RECT FOR TEST
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < -enemy[1].width : # deleting enemies
            enemies.pop(enemies.index(enemy))
        if player_rect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy)) 
            # is_working = False
        for projct in projectiles:
            if projct[1].colliderect(enemy[1]):
                enemies.pop(enemies.index(enemy))
                projectiles.pop(projectiles.index(projct))
    




    
    #bonuses movement,drawing & collision
    for bonus in bonuses:
        bonus[1]= bonus[1].move(-bonus[2], 0 )
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].right <0: # deleting bonuses
            bonuses.pop(bonuses.index(bonus))
        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1 
            if random.randint(0,1) == 0:
                if ammo +2 < 11:
                    ammo +=2
            else:
                if player_shields + 1 < 6:
                        player_shields += 1


    #projectiles movement, draving,& collision 
    for projct in projectiles:
        projct[1] = projct[1].move(projct[2][0], projct[2][1] )
        main_surface.blit(projct[0], projct[1])
        if projct[1].left > width:
            projectiles.pop(projectiles.index(projct))

        # print(len(bonuses))
        # print(len(enemies))
    print(len(projectiles))



    #Player movement 
    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
         player_rect = player_rect.move((0, player_speed))
    if pressed_keys[K_UP] and not player_rect.top <=0:
         player_rect = player_rect.move((0, -player_speed))
    if pressed_keys[K_LEFT]and not player_rect.left <= 0:
         player_rect = player_rect.move((-player_speed, 0 ))
    if pressed_keys[K_RIGHT]and not player_rect.right >=width:
         player_rect = player_rect.move((player_speed, 0 ))

    if pressed_keys[K_SPACE] and ammo >0 and gun_ready:
        shoot()
        gun_ready = False
        pygame.time.set_timer(GUN_CD_EVENT, gun_cooldown)

    pygame.display.flip()



    
