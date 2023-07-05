import pygame
import random
from random import randint
from pygame.constants import QUIT, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_SPACE, K_1, K_2, K_3, K_4
from pygame.math import Vector2

pygame.init()

fps = pygame.time.Clock()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
is_working = True

bg = pygame.image.load("sprites\Background_space.png").convert()
bg = pygame.transform.scale(bg, (screen_width, screen_height))

# CREATE_ENEMY = pygame.USEREVENT+1
# pygame.time.set_timer(CREATE_ENEMY, 5000)

class MlBackground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        # loading images and scaling them
        # layer1 - in the back, layer 3 - in the front
        self.layer1_img = pygame.transform.scale(pygame.image.load(r"sprites\background\Background_space.png").convert(), (screen_width, screen_height))
        self.layer2_img = pygame.transform.scale(pygame.image.load(r"sprites\background\darker_space_station.png").convert_alpha(), (screen_width//2, screen_height//2))
        # self.layer2_img = pygame.image.load(r"sprites\asteroid\background\bg_space_station.png").convert_alpha()

        self.layer3_img = pygame.transform.scale(pygame.image.load(r"sprites\background\bg_asteroids_dark.png").convert_alpha(), (screen_width*1.7, screen_height))
        # getting positions of first and second background for each layer
        self.layer1_pos = {"x1": 0, "x2": self.layer1_img.get_width()}
        self.layer2_pos = {"x1": screen_width//3, "x2": self.layer2_img.get_width()}
        self.layer3_pos = {"x1": 0, "x2": self.layer3_img.get_width()}
        # speed of each layer. 
        self.layer1_speed = 0.1
        self.layer2_speed = 0.2
        self.layer3_speed = 2

    def update(self):
        self.layer1_pos["x1"] -= self.layer1_speed
        self.layer1_pos["x2"] -= self.layer1_speed
        self.layer2_pos["x1"] -= self.layer2_speed
        self.layer2_pos["x2"] -= self.layer2_speed
        self.layer3_pos["x1"] -= self.layer3_speed
        self.layer3_pos["x2"] -= self.layer3_speed

        screen.blit(self.layer1_img, (self.layer1_pos["x1"],  0))
        screen.blit(self.layer1_img, (self.layer1_pos["x2"],  0))
        screen.blit(self.layer2_img, (self.layer2_pos["x1"],  screen_width//3))
        # screen.blit(self.layer2_img, (self.layer2_pos["x2"],  0)) #  I only nned station to be drawn once
        screen.blit(self.layer3_img, (self.layer3_pos["x1"],  0))
        screen.blit(self.layer3_img, (self.layer3_pos["x2"],  0))

        # resetting bg coordinates when they are out of screen
        if self.layer1_pos["x1"] < -self.layer1_img.get_width():
            self.layer1_pos["x1"] = self.layer1_img.get_width()
        if self.layer1_pos["x2"] < -self.layer1_img.get_width():
            self.layer1_pos["x2"] = self.layer1_img.get_width()

        # if self.layer2_pos["x1"] < -self.layer2_img.get_width(): # dont need this, since station must be showed only once
        #     self.layer2_pos["x1"] = self.layer2_img.get_width()
        # if self.layer2_pos["x2"] < -self.layer2_img.get_width():
        #     self.layer2_pos["x2"] = self.layer2_img.get_width()

        if self.layer3_pos["x1"] < -self.layer3_img.get_width():
            self.layer3_pos["x1"] = self.layer3_img.get_width()
        if self.layer3_pos["x2"] < -self.layer3_img.get_width():
            self.layer3_pos["x2"] = self.layer3_img.get_width()






class LevelData():
    def __init__(self,enemy_spawn_list):
        self.distance = 0
        self.level_lenght = 5000
        self.progress = 0 
        self.enemy_spawn_list = enemy_spawn_list
    def update(self):
        self.distance += 1
        self.progress = self.get_progress()
        self.spawn_enemy()
    def get_progress(self):
        if self.distance == 0:
            return 0
        else:
            return self.distance / self.level_lenght * 100
    
    def spawn_enemy(self):
        if enemy_spawn_list:
            if self.enemy_spawn_list[0].spawn_distance<= self.distance:
                enemy_group.add(self.enemy_spawn_list[0])
                self.enemy_spawn_list.pop(0)
    def spawn_bg_object(self):
        pass

    def level_complete(self):
        pass

class BasicGun():
    def __init__(self):
        self.cooldown_max = 50
        self.cooldown = 50
        self.color = pygame.Color("green")
        self.speed_x = 10
        self.speed_y = 0
        self.deviation_y = 0.2
        self.damage = 25
        self.proj_size =(15,5)
        self.name = "Basic gun"
    def shoot(self):
        if self.cooldown == 0:
            player_projectile_group.add(HorizontalProjectile(player.rect.centerx, player.rect.centery, self.color, self.speed_x, self.speed_y, self.deviation_y, self.damage, self.proj_size))
            self.cooldown = self.cooldown_max
    def update(self):
        if self.cooldown >0:
            self.cooldown -=1


class FastGun():
    def __init__(self):
        self.cooldown_max = 10
        self.cooldown = 20
        self.color = pygame.Color("yellow1")
        self.speed_x = 5
        self.speed_y = 0
        self.deviation_y = 0.5
        self.damage = 10
        self.proj_size =(5,2)
        self.name = "Fast gun"
    def shoot(self):
        if self.cooldown == 0:
            player_projectile_group.add(HorizontalProjectile(player.rect.centerx, player.rect.centery, self.color, self.speed_x, self.speed_y, self.deviation_y, self.damage,self.proj_size))
            self.cooldown = self.cooldown_max
    def update(self):
        if self.cooldown >0:
            self.cooldown -=1

class DoubleBarrelGun():
    def __init__(self):
        self.cooldown_max = 17
        self.cooldown = 25
        self.color = pygame.Color("red1")
        self.speed_x = 6
        self.speed_y = 0
        self.deviation_y = 0.5
        self.barrell= 1
        self.barell_offset = 10
        self.damage = 15
        self.proj_size =(12,4)
        self.name = "Twin gun"
    def shoot(self):
        if self.cooldown == 0:
            if self.barrell == 1:
                player_projectile_group.add(HorizontalProjectile(player.rect.centerx, player.rect.centery + self.barell_offset, self.color, self.speed_x, self.speed_y, self.deviation_y, self.damage, self.proj_size))
                self.barrell = 2
            elif self.barrell == 2:
                player_projectile_group.add(HorizontalProjectile(player.rect.centerx, player.rect.centery - self.barell_offset, self.color, self.speed_x, self.speed_y, self.deviation_y, self.damage, self.proj_size))
                self.barrell = 1            
            self.cooldown = self.cooldown_max
    def update(self):
        if self.cooldown >0:
            self.cooldown -=1

class SpreadGun():
    def __init__(self):
        self.cooldown_max = 75
        self.cooldown = 75
        self.color = pygame.Color("orange3")
        self.speed_x = 5
        self.speed_y = 0
        self.deviation_y = 2
        self.damage = 10
        self.proj_size =(3,3)
        self.name = "Spread gun"
    def shoot(self):
        if self.cooldown == 0:
            for i in range(10):
                player_projectile_group.add(HorizontalProjectile(player.rect.centerx, player.rect.centery, self.color, self.speed_x, self.speed_y , self.deviation_y, self.damage, self.proj_size ))

            self.cooldown = self.cooldown_max
    def update(self):
        if self.cooldown >0:
            self.cooldown -=1   




class HorizontalProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed_x, speed_y, deviation_y, damage, proj_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(proj_size)
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.pos =[x,y]
        self.deviation_y = random.uniform(-deviation_y, deviation_y)
        self.damage = damage
    def update(self):
        self.pos[0] += self.speed_x
        self.pos[1] += self.speed_y + self.deviation_y
        self.rect.center = self.pos





class Player(pygame.sprite.Sprite):
    def __init__ (self, x,y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\player\Fighter-1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.pos = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.hp = 100
        self.gun = BasicGun()
    def update(self):
        self.rect.center = self.pos
        self.gun.update()
        if self.hp<0:
            self.kill()

    def shoot(self):
        self.gun.shoot()

class PlayerInterface():
    def __init__(self):
        self.hp = player.hp
        self.hp_pos = (0,0)
        self.font = pygame.font.SysFont(None, 24)
        self.color = pygame.color.Color("palegreen")
        self.gun = player.gun
        self.gun_pos = (0, 20)
        self.progress = 0
        self.progress_pos = (screen_width - 140, 0)
    def update(self):
        self.hp = player.hp
        self.hp_obj = self.font.render(f"Hull integrity: {self.hp}", True, self.color)
        self.gun = player.gun
        self.gun_obj = self.font.render(f"Active weapon: {self.gun.name}", True, self.color)
        self.progress = int(level.progress)
        self.progress_obj = self.font.render(f"Completed: {self.progress}%", True, self.color)

    def draw(self):
        screen.blit(self.hp_obj, self.hp_pos)
        screen.blit(self.gun_obj, self.gun_pos)
        screen.blit(self.progress_obj, self.progress_pos)

        # self.cooldown_max = 17
        # self.cooldown = 25
class SmokeParticle(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = Vector2(pos)
        self.vel = Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
        self.acc = Vector2(0, 0)
        self.size = random.randint(3, 10)
        self.color = (pygame.color.Color("gray64"))
        self.life = 45
        
    def update(self):
        self.vel += self.acc
        self.pos += self.vel
        self.size *= 0.95
        self.life -= 1
        
        # If particle has died, remove it from the list
        if self.life <= 0:
            self.kill()
        if self.pos[0]<=10:
            self.kill()
        pygame.draw.circle(screen, self.color, self.pos, self.size)    

class FirePartickle(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = Vector2(pos)
        self.vel = Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
        self.acc = Vector2(0, 0)
        self.size = random.randint(2, 6)
        self.color = (pygame.color.Color("tan1"))
        self.life = 20
        
    def update(self):
        self.vel += self.acc
        self.pos += self.vel
        self.size *= 0.95
        self.life -= 1
        
        # If particle has died, remove it from the list
        if self.life <= 0:
            self.kill()
        pygame.draw.circle(screen, self.color, self.pos, self.size)    



class Explosion (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r"sprites\explosions\explosion-1.png")
        self.lifetime = 40
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    def update(self):
        self.lifetime -=1
        if self.lifetime <= 0:
            self.kill()
        elif self.lifetime <= 10:
            self.image = pygame.image.load(r"sprites\explosions\explosion-4.png")
        elif self.lifetime <= 20:
            self.image = pygame.image.load(r"sprites\explosions\explosion-3.png")
        elif self.lifetime <= 30:
            self.image = pygame.image.load(r"sprites\explosions\explosion-2.png")

class Enemy (pygame.sprite.Sprite):
    def __init__(self,spawn_distance, y, behavior, x = screen_width+50,  ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\enemies\enemy_pirate_fighter.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image.get_size()[0]//3 , self.image.get_size()[1]//3))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.pos = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_nominal = 1.5
        self.speed = self.speed_nominal
        self.gun_cooldown_nominal = 50
        self.gun_cooldown_max = self.gun_cooldown_nominal
        self.gun_cooldown = self.gun_cooldown_nominal
        self.maneuver_countdow = 100
        self.y_vector = 1
        self.hp = 50
        self.spawn_distance = spawn_distance
        

        self.proj_color = pygame.Color("orchid2")
        self.proj_speed_x = -6
        self.proj_speed_y = 0
        self.proj_deviation_y = 1.3
        self.damage = 10
        self.proj_size =(10,3)

        if behavior == 1:
            self.behavior = self.fly_left_shoot
        elif behavior == 2:
            self.behavior = self.intercept_shoot_on_sight
        elif behavior == 3:
            self.behavior = self.zigzag_left_shoot_on_sight
        elif behavior == 4:
            self.behavior = self.snipe_from_afar


    def update(self):


        # self.fly_left()
        # self.intercept() 
        # self.goto_player_altitude()
        # self.goto_player_longtitude()
        # self.hover_above_player(300)
        # self.hover_below_player(300)
        # self.shoot()
        # self.shoot_on_sight(150)
        # self.zigzag_left()
        self.behavior()
        self.rect.center = self.pos

        # damage effects
        if self.hp<0:
            self.explode()
        if self.pos[0]>0: # quick fix for a bug when smoke pos is <0
            if self.hp <30:
                smoke_particles_group.add(SmokeParticle((self.rect.centerx+ 20, self.rect.centery+5)))
                self.speed = self.speed_nominal / 1.5
                self.gun_cooldown_max = self.gun_cooldown_nominal * 1.5
            if self.hp <20:
                smoke_particles_group.add(FirePartickle((self.rect.centerx+20,self.rect.centery+5)))
                self.speed = self.speed_nominal / 1.7
                self.gun_cooldown_max = self.gun_cooldown_nominal * 1.7

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
            enemy_projectiles.add(HorizontalProjectile(self.rect.centerx, self.rect.centery, self.proj_color, self.proj_speed_x, self.proj_speed_y, self.proj_deviation_y, self.damage, self.proj_size))
            self.gun_cooldown = self.gun_cooldown_max
        else:
            self.gun_cooldown -=1

    def shoot_on_sight(self, deviation):
        if player.rect.centery + deviation >= self.rect.centery and player.rect.centery - deviation <= self.rect.centery and self.rect.centerx > player.rect.centerx:
            self.shoot()

    def fly_left_shoot(self):
        self.fly_left()
        self.shoot()

    def zigzag_left_shoot_on_sight(self):
        self.zigzag_left()
        self.shoot_on_sight(150)

    def snipe_from_afar(self):
        if self.rect.right> screen_width - 60:
            self.fly_left()
        else:
            self.goto_player_altitude()
            self.shoot_on_sight(150)
    
    def intercept_shoot_on_sight(self):
        self.intercept()
        self.shoot_on_sight(150)
        
# damage
    def explode(self):
        explosions_group.add(Explosion(self.rect.centerx, self.rect.centery))
        self.kill()

enemy_spawn_list = [Enemy(100, 150, 1), Enemy(150, 250, 1), Enemy(250, 350, 1), Enemy(250, 450, 1), Enemy(550, 150, 2), Enemy(650, 450, 4), Enemy(850, 250, 3), Enemy(850, 550, 3), Enemy(1150, 250, 4), Enemy(1150, 800, 4), 
                    Enemy(1450, 250, 3), Enemy(1450, 800, 3),Enemy(1650, 150, 3), Enemy(1650, 600, 3),Enemy(1150, 250, 4), Enemy(1150, 800, 4)]
level = LevelData(enemy_spawn_list)
bg = MlBackground()
player = Player(30, screen_height - 50, 5)
player_group = pygame.sprite.Group()
player_group.add(player)
player_projectile_group = pygame.sprite.Group()
player_interface = PlayerInterface()

# enemy = Enemy(screen_width - 130,300)
enemy_group = pygame.sprite.Group()
# enemy_group.add(enemy)
enemy_projectiles = pygame.sprite.Group()

explosions_group = pygame.sprite.Group()
smoke_particles_group = pygame.sprite.Group()

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


    # screen.blit(bg, (0,0))
    level.update()
    bg.update() 
    player_group.update()
    player_group.draw(screen)
    player_projectile_group.update()
    player_projectile_group.draw(screen)
    player_interface.update()
    player_interface.draw()
    

    enemy_group.update()
    enemy_group.draw(screen)
    enemy_projectiles.update()
    enemy_projectiles.draw(screen)
    explosions_group.update()
    explosions_group.draw(screen)
    smoke_particles_group.update()
    # smoke_particles_group.draw(screen)
# despawn objects out of screen, collisions and damage
    for projectile in enemy_projectiles:
        if projectile.rect.right <0:
            projectile.kill()
        if pygame.sprite.spritecollide(projectile, player_group, False, pygame.sprite.collide_rect):
            if pygame.sprite.spritecollide(projectile, player_group, False, pygame.sprite.collide_mask):
                projectile.kill()
                player.hp -= projectile.damage

    for projectile in player_projectile_group:
        if projectile.rect.left > screen_width:
            projectile.kill()
        for enemy in enemy_group:
            if projectile.rect.colliderect(enemy.rect):
                if pygame.sprite.collide_mask(enemy, projectile):
                    projectile.kill()
                    enemy.hp -= projectile.damage


    for enemy in enemy_group:
        if enemy.rect.right <0:
            enemy.kill()

# for debug
    # print(f" player shoots {len(player_projectile_group)}")
    # print(f" enemy shoots {len(enemy_projectiles)}")
    # print(f" enemies {len(enemy_group)}")
    # print(f" player health {player.hp}")
    # print(f"level distance: {level.distance}")
    # print(f"level progress: {level.progress}")

# event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        # if event.type == CREATE_ENEMY:
        #     enemy_group.add(Enemy( screen_height *random.uniform(0, 0.8)))


    pygame.display.flip()













