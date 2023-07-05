import pygame
import math
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

class GunMount(pygame.sprite.Sprite):
    def __init__ (self, x,y,):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r"turret\turret mount.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.pos = [x, y]
        self.mask = pygame.mask.from_surface(self.image)       


class Gun(pygame.sprite.Sprite):
    def __init__ (self, x,y,):
        pygame.sprite.Sprite.__init__(self)
        self.image_nominal = pygame.image.load(r"turret\turret gun.png").convert_alpha()
        self.nominal_image_rect = self.image_nominal.get_rect()
        self.nominal_image_rect.center = [x, y]
        self.image = pygame.image.load(r"turret\turret gun.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.pos = [x, y]
        self.mask = pygame.mask.from_surface(self.image)   
        self.angle = 0    
        self.gun_cooldown_nominal = 50
        self.gun_cooldown = 0
    def update(self):
        x1 = player.rect.centerx
        y1 = player.rect.centery
        x2 = self.rect.centerx
        y2 = self.rect.centery
        self.angle =  math.degrees(math.atan2(y2 - y1, x2 - x1))

        if self.gun_cooldown >0:
            self.gun_cooldown -=1


        self.image = pygame.transform.rotate(self.image_nominal, -self.angle//1)
        self.rect.center = (self.nominal_image_rect.centerx - int(self.image.get_width()//2) +50, self.nominal_image_rect.centery - (self.image.get_height()//2)+50) # + 50 - to compensate offcentre bug
        self.shoot_player()

    def shoot_player(self):
        if self.gun_cooldown == 0:
            # from where the shot is fired
            x_start = self.rect.centerx
            Y_start = self.rect.centery
            # difference between x,y of self and target
            dx = x_start - player.rect.centerx
            dy = Y_start - player.rect.centery
            # ratio of x/y, x% + y% = 1 
            x_percent = (abs(dx) / (abs(dx) + abs(dy))) * 100
            y_percent = (abs(dy) / (abs(dx) + abs(dy))) * 100
            # avoiding division on zero error later
            if x_percent == 0:
                x_percent = 0.001
            if y_percent == 0:
                y_percent = 0.001

            # chosing correct direction
            if player.rect.centerx > x_start:
                x_sign = 1
            elif player.rect.centerx < x_start:
                x_sign = -1
            else:
                x_sign = 0
            if player.rect.centery > Y_start:
                y_sign = 1
            elif player.rect.centery < Y_start:
                y_sign = -1
            else:
                y_sign = 0
            projectile_group.add(Projectile(x_start, Y_start, x_percent, y_percent, x_sign, y_sign))
            # gun cooldown
            self.gun_cooldown = self.gun_cooldown_nominal


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, x_percent, y_percent, x_sign, y_sign):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,5))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 10
        # calculating speed for x,y component 
        self.x_vel = self.speed * x_percent/100 * x_sign
        self.y_vel = self.speed * y_percent/100 * y_sign
        self.pos = {"x": x, "y": y}
        #  for debug
        self.x_percent = x_percent
        self.y_percent = y_percent
        self.printed = False
    def update(self):
        self.pos["x"] += self.x_vel
        self.pos["y"] += self.y_vel 
        self.rect.center =[self.pos["x"], self.pos["y"] ]
        







player = Player(30, screen_height - 50, 5)
player_group = pygame.sprite.Group()
player_group.add(player)

gun = Gun(screen_width*0.8, screen_height - 50)
gun_group = pygame.sprite.Group()
gun_group.add(gun)

gun_mount = GunMount(screen_width*0.8, screen_height - 50)
gun_mount_group = pygame.sprite.Group()
gun_mount_group.add(gun_mount)
projectile_group = pygame.sprite.Group()




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
    gun_group.update()
    gun_group.draw(screen)
    gun_mount_group.draw(screen)
    projectile_group.update()
    projectile_group.draw(screen)







    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
    pygame.display.flip()













