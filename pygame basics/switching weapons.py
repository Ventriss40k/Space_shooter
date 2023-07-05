import pygame

from pygame.constants import QUIT, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_SPACE, K_1, K_2, K_3, K_4
import random

pygame.init()

fps = pygame.time.Clock()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
is_working = True

bg = pygame.image.load("sprites\Background_space.png").convert()
bg = pygame.transform.scale(bg, (screen_width, screen_height))


class Player(pygame.sprite.Sprite):
    def __init__ (self, x,y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\player\Fighter-1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.pos = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.gun = FastGun()
    def update(self):
        self.rect.center = self.pos
        self.gun.update()

    def shoot(self):
        self.gun.shoot()



class BasicGun():
    def __init__(self):
        self.cooldown_max = 50
        self.cooldown = 0
        self.color = pygame.Color("green")
        self.speed_x = 7
        self.speed_y = 0
        self.deviation_y = 0.2
    def shoot(self):
        if self.cooldown == 0:
            player_projectile_group.add(HorizontalProjectile(player.rect.centerx, player.rect.centery, self.color, self.speed_x, self.speed_y, self.deviation_y))
            self.cooldown = self.cooldown_max
    def update(self):
        if self.cooldown >0:
            self.cooldown -=1


class FastGun():
    def __init__(self):
        self.cooldown_max = 15
        self.cooldown = 0
        self.color = pygame.Color("orchid1")
        self.speed_x = 5
        self.speed_y = 0
        self.deviation_y = 0.5
    def shoot(self):
        if self.cooldown == 0:
            player_projectile_group.add(HorizontalProjectile(player.rect.centerx, player.rect.centery, self.color, self.speed_x, self.speed_y, self.deviation_y))
            self.cooldown = self.cooldown_max
    def update(self):
        if self.cooldown >0:
            self.cooldown -=1

class DoubleBarrelGun():
    def __init__(self):
        self.cooldown_max = 20
        self.cooldown = 0
        self.color = pygame.Color("red1")
        self.speed_x = 6
        self.speed_y = 0
        self.deviation_y = 0.3
        self.barrell= 1
        self.barell_offset = 10
    def shoot(self):
        if self.cooldown == 0:
            if self.barrell == 1:
                player_projectile_group.add(HorizontalProjectile(player.rect.centerx, player.rect.centery + self.barell_offset, self.color, self.speed_x, self.speed_y, self.deviation_y))
                self.barrell = 2
            elif self.barrell == 2:
                player_projectile_group.add(HorizontalProjectile(player.rect.centerx, player.rect.centery - self.barell_offset, self.color, self.speed_x, self.speed_y, self.deviation_y))
                self.barrell = 1            
            self.cooldown = self.cooldown_max
    def update(self):
        if self.cooldown >0:
            self.cooldown -=1

class SpreadGun():
    def __init__(self):
        self.cooldown_max = 75
        self.cooldown = 0
        self.color = pygame.Color("orange3")
        self.speed_x = 5
        self.speed_y = 0
        self.deviation_y = 2
    def shoot(self):
        if self.cooldown == 0:
            for i in range(10):
                player_projectile_group.add(HorizontalProjectile(player.rect.centerx, player.rect.centery, self.color, self.speed_x, self.speed_y , self.deviation_y))

            self.cooldown = self.cooldown_max
    def update(self):
        if self.cooldown >0:
            self.cooldown -=1   




class HorizontalProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed_x, speed_y, deviation_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15,3))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.pos =[x,y]
        self.deviation_y = random.uniform(-deviation_y, deviation_y)
    def update(self):
        self.pos[0] += self.speed_x
        self.pos[1] += self.speed_y + self.deviation_y
        self.rect.center = self.pos







player = Player(30, screen_height - 50, 5)
player_group = pygame.sprite.Group()
player_group.add(player)
player_projectile_group = pygame.sprite.Group()





while is_working:
    fps.tick(60)

    pressed_keys = pygame.key.get_pressed()    

    if pressed_keys[K_UP]:
        player.pos[1] -= player.speed
    if pressed_keys[K_DOWN]:
        player.pos[1] += player.speed
    if pressed_keys[K_LEFT]:
        player.pos[0] -= player.speed
    if pressed_keys[K_RIGHT]:
        player.pos[0] += player.speed
    if pressed_keys[K_SPACE]:
        player.shoot()   

# change weapon 
    if pressed_keys[K_1]:
        player.gun = BasicGun()
    if pressed_keys[K_2]:
        player.gun = FastGun()
    if pressed_keys[K_3]:
        player.gun = DoubleBarrelGun()
    if pressed_keys[K_4]:
        player.gun = SpreadGun()



    screen.blit(bg, (0,0))
    player_group.update()
    player_group.draw(screen)
    player_projectile_group.update()
    player_projectile_group.draw(screen)








    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
    pygame.display.flip()













