import pygame
from random import randint
from pygame.constants import QUIT, K_UP, K_DOWN, K_RIGHT, K_LEFT


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
    def update(self):
        self.rect.center = self.pos

class Enemy (pygame.sprite.Sprite):
    def __init__(self, x, y ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\enemies\enemy_pirate_fighter.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image.get_size()[0]//3 , self.image.get_size()[1]//3))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.pos = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 1.5
        self.gun_cooldown = 50
        self.maneuver_countdow = 100
        self.y_vector = 1
    def update(self):

        # self.fly_left()
        # self.intercept()
        # self.goto_player_altitude()
        # self.goto_player_longtitude()
        # self.hover_above_player(300)
        # self.hover_below_player(300)
        # self.shoot()
        self.shoot_on_sight(150)
        self.zigzag_left()

        self.rect.center = self.pos 

    def goto_player_altitude(self):
        if player.pos[1] > self.pos[1]:
            self.pos[1]+=self.speed
        if player.pos[1] < self.pos[1]:
            self.pos[1]-=self.speed

    def goto_player_longtitude(self):
        if player.pos[0] > self.pos[0]:
            self.pos[0]+=self.speed
        if player.pos[0] < self.pos[0]:
            self.pos[0]-=self.speed

    def hover_above_player(self, hover_height):
        self.goto_player_longtitude()
        if player.pos[1] > self.pos[1] + hover_height :
            self.pos[1]+=self.speed
        if player.pos[1] < self.pos[1] + hover_height:
            self.pos[1]-=self.speed        

    def hover_below_player(self, hover_height):
        self.goto_player_longtitude()
        if player.pos[1] > self.pos[1] - hover_height :
            self.pos[1]+=self.speed
        if player.pos[1] < self.pos[1] - hover_height:
            self.pos[1]-=self.speed        

    def fly_left(self):
        self.pos[0]-= self.speed

    def zigzag_left(self):
        self.fly_left()
        if self.maneuver_countdow == 0:
            self.y_vector *= -1
            self.maneuver_countdow = randint(70, 120)
        else:
            self.maneuver_countdow -=1
        self.pos[1] += self.speed * self.y_vector
    

    def intercept(self):
        if player.rect.centerx < self.rect.centery:
            self.goto_player_altitude()
        self.fly_left()

    def ram_player(self):
        self.goto_player_altitude()
        self.goto_player_longtitude()

    def shoot(self):
        if self.gun_cooldown == 0:
            enemy_projectiles.add(HorizontalProjectile(self.rect.centerx, self.rect.centery))
            self.gun_cooldown = 50
        else:
            self.gun_cooldown -=1

    def shoot_on_sight(self, deviation):
        if player.rect.centery + deviation >= self.rect.centery and player.rect.centery - deviation <= self.rect.centery and self.rect.centerx > player.rect.centerx:
            self.shoot()



class HorizontalProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15,3))
        self.image.fill(pygame.Color("orchid1"))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 7
        self.pos =[x,y]
    def update(self):
        self.pos[0] -= self.speed
        self.rect.center = self.pos


player = Player(30, screen_height - 50, 5)
player_group = pygame.sprite.Group()
player_group.add(player)


enemy = Enemy(screen_width - 130,300)
enemy_group = pygame.sprite.Group()
enemy_group.add(enemy)
enemy_projectiles = pygame.sprite.Group()

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



    screen.blit(bg, (0,0))
    player_group.update()
    player_group.draw(screen)
    enemy_group.update()
    enemy_group.draw(screen)
    enemy_projectiles.update()
    enemy_projectiles.draw(screen)
    print(len(enemy_projectiles))







    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
    pygame.display.flip()













