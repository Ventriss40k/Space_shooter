
from typing import Any
import pygame
import random
from random import randint
from pygame.constants import QUIT, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_SPACE, K_LCTRL, K_1, K_2, K_3, K_4
import math
from pygame.math import Vector2

pygame.init()

fps = pygame.time.Clock()
user_screen_stats = pygame.display.Info()
# screen_width = user_screen_stats.current_w
# screen_height = user_screen_stats.current_h
screen_width = 1800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
is_working = True

bg = pygame.image.load(r"sprites\Background_space.png").convert()
bg = pygame.transform.scale(bg, (screen_width, screen_height))

# CREATE_ENEMY = pygame.USEREVENT+1
# pygame.time.set_timer(CREATE_ENEMY, 5000)

# Pause related
class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y, font_size):
        pygame.sprite.Sprite.__init__(self)
        self.font_normal = pygame.font.SysFont(None, font_size)
        self.font_hover = pygame.font.SysFont(None, int(font_size * 1.1))
        self.font = self.font_normal
        self.text = text
        self.pos = [x, y]
        self.image = self.font.render(text, True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        self.mouse_pointed = False

    def update(self):
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
    
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.mouse_hover_on()
        else:
            self.mouse_hover_off()


    def mouse_hover_on(self):
        self.font_update()
        self.font = self.font_hover
        self.mouse_pointed = True


    def mouse_hover_off(self):
        self.font_update()
        self.font = self.font_normal
        self.mouse_pointed = False

    def font_update(self):
        self.image = self.font.render(self.text, True, (pygame.color.Color("Green3")))

class PauseMenu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.buttons_group = pygame.sprite.Group()   
        self.resume_button = Button("Resume", 0, 0, 80)
        self.exit_button = Button("Quit", 0, 0, 80)
        self.settings_button = Button("Settings", 0, 0, 80)
        self.save_button = Button("Save", 0, 0, 80)
        self.load_button = Button("Load", 0, 0, 80)
        # self.buttons_list = [self.resume_button, self.exit_button]

        self.buttons_list = [self.resume_button, self.settings_button, self.save_button, self.load_button, self.exit_button]
        self.button_height = self.resume_button.rect.height
        self.button_padding_multiplyer = 1.3
        self.per_button_height =  self.button_height * self.button_padding_multiplyer 
        self.menu_width = max(self.buttons_list, key=lambda button: button.rect.width).rect.width * 1.5 
        self.menu_height = len(self.buttons_list) * self.per_button_height
        self.rect = pygame.Rect(0,0,self.menu_width, self.menu_height)
        self.rect.center = (screen_width//2, screen_height//2)
        n_button = 0
        for i in self.buttons_list: 
            n_button += 1  
            i.pos = [self.rect.centerx,self.rect.top + self.per_button_height*n_button - self.per_button_height//2 ]
            self.buttons_group.add(i)
    def update(self):
        pygame.draw.rect(screen, pygame.color.Color("ivory3"), self.rect)
        self.buttons_group.update()
        self.buttons_group.draw(screen)
# --- pause related end

class MainMenu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.buttons_group = pygame.sprite.Group()   
        self.new_game_button = Button("New game", 0, 0, 100)
        self.continue_button = Button("Continue", 0, 0, 100)
        self.exit_button = Button("Quit", 0, 0, 100)
        self.settings_button = Button("Settings", 0, 0, 100)
        self.save_button = Button("Save", 0, 0, 100)
        self.load_button = Button("Load", 0, 0, 100)
        self.bg = pygame.image.load("sprites\Art.png")
        self.bg = pygame.transform.scale(self.bg, (screen_width, screen_height))


        self.buttons_list = [self.new_game_button, self.continue_button, self.load_button, self.settings_button, self.exit_button]
        self.button_height = self.exit_button.rect.height
        self.button_padding_multiplyer = 1.3
        self.per_button_height =  self.button_height * self.button_padding_multiplyer 
        self.menu_width = max(self.buttons_list, key=lambda button: button.rect.width).rect.width * 1.5 
        self.menu_height = len(self.buttons_list) * self.per_button_height
        self.rect = pygame.Rect(0,0,self.menu_width, self.menu_height)
        self.rect.center = (screen_width//2, screen_height//2)
        n_button = 0
        for i in self.buttons_list: 
            n_button += 1  
            i.pos = [self.rect.centerx,self.rect.top + self.per_button_height*n_button - self.per_button_height//2 ]
            self.buttons_group.add(i)
    def update(self):
        screen.blit(self.bg, (0, 0))
        self.buttons_group.update()
        self.buttons_group.draw(screen)
        





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
        self.level_lenght = 1000
        self.progress = 0 
        self.enemy_spawn_list = enemy_spawn_list
    def update(self):
        self.distance += 1
        if self.get_progress()> 100:
            self.progress = 100
        else:
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
        self.pos = [-100, -100]
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.hp = 100
        self.gun = BasicGun()
        # autopilot related
        self.controllable = False
        self.spawned = False
        self.spawned_arrived = False
        self.disengaging = False
        self.invincible = False
    def update(self):
        self.rect.center = self.pos
        self.gun.update()
        if self.hp<0:
            self.kill()
        if not self.spawned_arrived:
            self.spawn()
        if level.progress >=100:
            self.disengage()

    def spawn(self):
        if self.spawned == False:
            self.pos = [-250, screen_height//2]
            self.spawned = True
        if not self.spawned_arrived:
            if self.autopilot([screen_width//4, screen_height//2],1):
                self.spawned_arrived = True
                self.controllable = True

    def disengage(self):
        self.controllable = False
        # triggering when level progress ==100
        self.autopilot([screen_width*1.2, screen_height//2],1)


    def shoot(self):
        self.gun.shoot()

    def autopilot(self, target_pos, speed_k):
        self.controllable = False
        self.invincible = True
        if self.pos[0] < target_pos[0]:
            self.pos[0] += self.speed*speed_k
        elif self.pos[0] > target_pos[0]:
            self.pos[0] -= self.speed*speed_k

        if self.pos[1] < target_pos[1]:
            self.pos[1] += self.speed*speed_k
        elif self.pos[1] > target_pos[1]:
            self.pos[1] -= self.speed*speed_k

        if self.pos == target_pos:
            self.invincible = False
            return True



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
        elif behavior == 5:
            self.behavior = self.intercept       

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

class TorpedoCorvette(Enemy):
    def __init__(self, spawn_distance, y, behavior, x=screen_width + 50):
        super().__init__(spawn_distance, y, behavior, x)
    # def __init__(self,spawn_distance, y, behavior, x = screen_width+50,  ):
    #     pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\enemies\Torpedo corvette\Body.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image.get_size()[0]//3 , self.image.get_size()[1]//3))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.pos = [x, y]
        self.mask = pygame.mask.from_surface(self.image) 
        self.prev_pos = self.pos
        self.engine_frame = 0
        self.engine_counter = 0
        self.torpedo_cooldown = 100
        self.gun_cooldown_nominal = 5
        self.gun_cooldown_max = self.gun_cooldown_nominal
        self.turret_ammo_max = 4
        self.turret_ammo = self.turret_ammo_max
        self.turret_reload_time = 70
        self.turret_reload_progress = 0 
        self.target_state ="Left-top"
        self.torpedo_ammo = 3 
        #additional parts
        self.radar_img = pygame.image.load("sprites\enemies\Torpedo corvette\Radar.png").convert_alpha()
        self.radar_img = pygame.transform.scale(self.radar_img,(self.radar_img.get_size()[0]//3 , self.radar_img.get_size()[1]//3))
        self.radar_rect = self.radar_img.get_rect()
        self.radar_rect.bottom = self.rect.top
        self.radar_rect.centerx = self.rect.centerx
        self.radar_relative_pos = [self.radar_rect.centerx - self.rect.centerx, self.radar_rect.centery - self.rect.centery]

        self.thruster_img = pygame.image.load("sprites\enemies\Torpedo corvette\Thruster.png").convert_alpha()       
        self.thruster_img  = pygame.transform.scale(self.thruster_img ,(self.thruster_img .get_size()[0]//3 , self.thruster_img.get_size()[1]//3))
        self.thruster_rect = self.thruster_img.get_rect()
        self.thruster_rect.center = [self.rect.right - self.thruster_rect.width//2, self.rect.top]
        self.thruster_relative_pos = [self.thruster_rect.centerx - self.rect.centerx, self.thruster_rect.centery - self.rect.centery]

        self.turret_mount_img = pygame.image.load("sprites\enemies\Torpedo corvette\Turret mount.png").convert_alpha()       
        self.turret_mount_img  = pygame.transform.scale(self.turret_mount_img ,(self.turret_mount_img .get_size()[0]//3 , self.turret_mount_img.get_size()[1]//3))
        self.turret_mount_rect = self.turret_mount_img.get_rect()        
        self.turret_mount_rect.center = [self.rect.left + self.rect.width//4, self.rect.bottom]
        self.turret_mount_relative_pos = [self.turret_mount_rect.centerx - self.rect.centerx, self.turret_mount_rect.centery - self.rect.centery]



        self.turret_gun_img = pygame.image.load("sprites\enemies\Torpedo corvette\Turret gun.png").convert_alpha()       
        self.turret_gun_img  = pygame.transform.scale(self.turret_gun_img ,(self.turret_gun_img .get_size()[0]//3 , self.turret_gun_img.get_size()[1]//3))
        self.turret_gun_rect = self.turret_gun_img.get_rect()
        self.turret_gun_rect.center = self.turret_mount_rect.center
        self.turret_gun_relative_pos = [self.turret_gun_rect.centerx - self.rect.centerx, self.turret_gun_rect.centery - self.rect.centery]

        self.thruster_fire_right0 = pygame.image.load("sprites\enemies\Torpedo corvette\Thruster fire_0.png")
        self.thruster_fire_right0 = pygame.transform.scale(self.thruster_fire_right0, (self.thruster_fire_right0.get_size()[0]//3.5, self.thruster_fire_right0.get_size()[1]//3))
        self.thruster_fire_right1 = pygame.image.load("sprites\enemies\Torpedo corvette\Thruster fire_1.png")
        self.thruster_fire_right1 = pygame.transform.scale(self.thruster_fire_right1, (self.thruster_fire_right1.get_size()[0]//4, self.thruster_fire_right1.get_size()[1]//3))


        self.thruster_fire_right2 = pygame.image.load("sprites\enemies\Torpedo corvette\Thruster fire_2.png")
        self.thruster_fire_right2 = pygame.transform.scale(self.thruster_fire_right0, (self.thruster_fire_right2.get_size()[0]//4.5, self.thruster_fire_right2.get_size()[1]//3))

        self.thruster_fire_right3 = pygame.image.load("sprites\enemies\Torpedo corvette\Thruster fire_3.png")
        self.thruster_fire_right3 = pygame.transform.scale(self.thruster_fire_right3, (self.thruster_fire_right3.get_size()[0]//5, self.thruster_fire_right3.get_size()[1]//3))

        self.thruster_fire_right = [self.thruster_fire_right0, self.thruster_fire_right1, self.thruster_fire_right2, self.thruster_fire_right3]
        self.thrusrer_fire_right_rect = self.thruster_fire_right0.get_rect()

        self.thruster_fire_left0 = pygame.transform.flip(self.thruster_fire_right0, True, False)
        self.thruster_fire_left1 = pygame.transform.flip(self.thruster_fire_right1, True, False)
        self.thruster_fire_left2 = pygame.transform.flip(self.thruster_fire_right2, True, False)
        self.thruster_fire_left3 = pygame.transform.flip(self.thruster_fire_right3, True, False)
        self.thruster_fire_left = [self.thruster_fire_left0, self.thruster_fire_left1, self.thruster_fire_left2, self.thruster_fire_left3]
        self.thrusrer_fire_left_rect = self.thruster_fire_left0.get_rect()

        self.torp_loaded_img = pygame.image.load("sprites\enemies\Torpedo corvette\Loaded torpedo tube.png").convert_alpha()
        self.torp_loaded_img = pygame.transform.scale(self.torp_loaded_img ,(self.torp_loaded_img .get_size()[0]//3 , self.torp_loaded_img.get_size()[1]//3))
        self.torp_empty_img = pygame.image.load("sprites\enemies\Torpedo corvette\Empty torpedo tube.png").convert_alpha()
        self.torp_empty_img = pygame.transform.scale(self.torp_empty_img ,(self.torp_empty_img .get_size()[0]//3 , self.torp_empty_img.get_size()[1]//3))

        # torpedo containers
        self.torp_cont_1_img =  self.torp_loaded_img
        self.torp_cont_2_img =  self.torp_loaded_img
        self.torp_cont_3_img =  self.torp_loaded_img

        self.torp_cont_1_rect =  self.torp_cont_1_img.get_rect()
        self.torp_cont_2_rect =  self.torp_cont_2_img.get_rect()
        self.torp_cont_3_rect =  self.torp_cont_3_img.get_rect()

        self.torp_cont_1_rect.center = [self.rect.centerx, self.rect.centery + 0.2* self.rect.height]
        self.torp_cont_2_rect.center = [self.torp_cont_1_rect.centerx + self.torp_cont_1_rect.width//5*1, self.torp_cont_1_rect.centery] 
        self.torp_cont_3_rect.center = [self.torp_cont_1_rect.centerx + self.torp_cont_1_rect.width//5 *2, self.torp_cont_1_rect.centery] 
  
        self.torp_cont_1_rel_pos = [ self.torp_cont_1_rect.centerx - self.rect.centerx,  self.torp_cont_1_rect.centery - self.rect.centery]
        self.torp_cont_2_rel_pos = [ self.torp_cont_2_rect.centerx - self.rect.centerx,  self.torp_cont_2_rect.centery - self.rect.centery]
        self.torp_cont_3_rel_pos = [ self.torp_cont_3_rect.centerx - self.rect.centerx,  self.torp_cont_3_rect.centery - self.rect.centery]

    def shoot_torpedo(self):
        if self.torpedo_ammo >0:
            if self.torpedo_cooldown == 0:
                enemy_projectiles.add(Torpedo(self.rect.centerx, self.rect.centery, 9, 0, 50, player)) 
                self.torpedo_cooldown = 200
                self.torpedo_ammo -=1
                self.torpedo_cont_update()
            else:
                self.torpedo_cooldown -= 1

    def torpedo_cont_update(self):
        if self.torpedo_ammo == 2:
            self.torp_cont_1_img = self.torp_empty_img
        elif self.torpedo_ammo == 1:
            self.torp_cont_2_img = self.torp_empty_img
        elif self.torpedo_ammo == 0:
            self.torp_cont_3_img = self.torp_empty_img

    def update(self):
        #update pos of each part 
        self.radar_rect.center = [self.pos[0]+self.radar_relative_pos[0], self.pos[1]+self.radar_relative_pos[1],]
        self.thruster_rect.center = [self.pos[0]+self.thruster_relative_pos[0], self.pos[1]+self.thruster_relative_pos[1],]
        
        self.turret_mount_rect.center = [self.pos[0]+self.turret_mount_relative_pos[0], self.pos[1]+self.turret_mount_relative_pos[1],]
        self.turret_gun_rect.center = [self.pos[0]+self.turret_gun_relative_pos[0], self.pos[1]+self.turret_gun_relative_pos[1],]
       
        self.torp_cont_1_rect.center = [self.pos[0]+self.torp_cont_1_rel_pos[0], self.pos[1]+self.torp_cont_1_rel_pos[1],]
        self.torp_cont_2_rect.center = [self.pos[0]+self.torp_cont_2_rel_pos[0], self.pos[1]+self.torp_cont_2_rel_pos[1],]
        self.torp_cont_3_rect.center = [self.pos[0]+self.torp_cont_3_rel_pos[0], self.pos[1]+self.torp_cont_3_rel_pos[1],]
        
        self.thrusrer_fire_right_rect.left = self.thruster_rect.right
        self.thrusrer_fire_right_rect.centery = self.thruster_rect.centery
        self.thrusrer_fire_left_rect.right = self.thruster_rect.left
        self.thrusrer_fire_left_rect.centery = self.thruster_rect.centery
        
        self.engine_counter +=1
        if self.engine_counter >= 20:
            if self.engine_frame <3:
                self.engine_frame +=1
            else:
                self.engine_frame = 0
            self.engine_counter = 0
            




        super().update()
        # draw parts
        self.target_state = self.target_in_range(player) # defines if target is in range 
# shoot turret
        if self.target_state == "Left-bottom":
            self.turret_gun_img_rot = pygame.transform.rotate(self.turret_gun_img, -self.angle_to_target(self.turret_gun_rect.center,player.pos,)+180)
            self.turret_gun_rect.center = (self.turret_mount_rect.centerx - int(self.turret_gun_img_rot.get_width()//2)+self.turret_gun_img.get_width()//2 , self.turret_mount_rect.centery - int(self.turret_gun_img_rot.get_height()//2)+self.turret_gun_img.get_height()//2)
            self.shoot_turret()
        elif self.target_state == "Left-top" or self.target_state == "Right-top":
            self.turret_gun_img_rot = self.turret_gun_img
        elif self.target_state == "Right-bottom":
            self.turret_gun_img_rot = pygame.transform.rotate(self.turret_gun_img, 90)
            self.turret_gun_rect.center = (self.turret_mount_rect.centerx - int(self.turret_gun_img_rot.get_width()//2)+self.turret_gun_img.get_width()//2 , self.turret_mount_rect.centery - int(self.turret_gun_img_rot.get_height()//2)+self.turret_gun_img.get_height()//2)
#shoot torpedo 

        self.shoot_torpedo()

# (self.nominal_image_rect.centerx - int(self.image.get_width()//2) +50, self.nominal_image_rect.centery - (self.image.get_height()//2)+50) # + 50 - to compensate offcentre bug

        screen.blit(self.radar_img, self.radar_rect)
        screen.blit(self.thruster_img, self.thruster_rect)
        screen.blit(self.turret_gun_img_rot, self.turret_gun_rect)
        # screen.blit(self.turret_gun_img, self.turret_gun_rect)
        screen.blit(self.turret_mount_img, self.turret_mount_rect)
        screen.blit(self.torp_cont_1_img, self.torp_cont_1_rect)
        screen.blit(self.torp_cont_2_img, self.torp_cont_2_rect)
        screen.blit(self.torp_cont_3_img, self.torp_cont_3_rect)
        

        
        screen.blit(self.thruster_fire_right[self.engine_frame],  self.thrusrer_fire_right_rect)

    def shoot(self):
        pass
    def shoot_turret(self):
        if self.turret_ammo >0:
            if self.gun_cooldown == 0:
            # if self.turret_mount_rect.centerx > player.pos[0]:
                # from where the shot is fired
                x_start = self.turret_mount_rect.centerx
                Y_start = self.turret_mount_rect.centery
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
                enemy_projectiles.add(RoundProjectile(x_start, Y_start, x_percent, y_percent, x_sign, y_sign, 10, 10))
                self.turret_ammo -= 1
                self.gun_cooldown = self.gun_cooldown_max
            else:
                self.gun_cooldown -=1
        else:
            self.turret_reload_progress +=1

        if self.turret_reload_progress >= self.turret_reload_time:
            self.turret_ammo = self.turret_ammo_max
            self.turret_reload_progress = 0
              

        

    def angle_to_target(self, start_pos, targ_pos):
        # Calculate the angle between the points
        angle = math.atan2(targ_pos[1] - start_pos[1], targ_pos[0] - start_pos[0])
        # Convert the angle from radians to degrees
        angle = math.degrees(angle)
        # Adjust the angle to be between 0 and 360 degrees
        # print(angle)
        if angle < 0:
            angle += 360

        return angle

    def target_in_range(self, target):
        if target.pos[0] <= self.turret_mount_rect.centerx and target.pos[1] >= self.turret_mount_rect.centery -150 :
            return "Left-bottom"
        elif target.pos[0] <= self.turret_mount_rect.centerx and target.pos[1] <= self.turret_mount_rect.centery:
            return "Left-top"
        elif target.pos[0] >= self.turret_mount_rect.centerx and target.pos[1] >= self.turret_mount_rect.centery:
            return "Right-bottom"
        elif target.pos[0] >= self.turret_mount_rect.centerx and target.pos[1] >= self.turret_mount_rect.centery:
            return "Right-top"
        else:
            return "Left-top"
    # def aim_gun(self,gun_center, target):
    #     angle = self.angle_to_target(gun_center, target)
    #     index = int(angle//15)
    #     if index in range(0,5):
    #         self.turret_gun_img = self.turret_gun_sprites[index]

class Torpedo(pygame.sprite.Sprite):
    def __init__(self, x ,y, speed_x, speed_y, damage, target):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\enemies\Torpedo corvette\Torpedo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image.get_size()[0]//4 , self.image.get_size()[1]//2.5))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = [x, y]
        self.pos = [x, y]
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.damage = damage
        self.target = target
    def update(self):
        self.pos[0] -= self.speed_x
        self.rect.center = self.pos
        if self.target.pos[0] < self.pos[0]: # if target ahead of rocket
            if self.target.pos[1] > self.pos[1]:
                self.pos[1] += self.speed_x//4
            elif self.target.pos[1] < self.pos[1]:
                self.pos[1] -= self.speed_x//4
        if self.pos[0]>0:
            smoke_particles_group.add(SmokeParticle((self.rect.right, self.rect.centery)))
            smoke_particles_group.add(FirePartickle((self.rect.right, self.rect.centery)))      


class RoundProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, x_percent, y_percent, x_sign, y_sign, speed, damage):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.damage = damage
        self.image = pygame.Surface((6,6))
        self.image.set_colorkey((0, 0, 0))
        self.circle_radius = self.image.get_width()//2
        self.circle_center = [self.circle_radius,self.circle_radius]
        # self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        # calculating speed for x,y component 
        self.x_vel = self.speed * x_percent/100 * x_sign
        self.y_vel = self.speed * y_percent/100 * y_sign
        self.pos = {"x": x, "y": y}
        #  for debug
        self.x_percent = x_percent
        self.y_percent = y_percent
        self.printed = False
        pygame.draw.circle(self.image, pygame.color.Color("Orange1"), self.circle_center, self.circle_radius)
    def update(self):
        self.pos["x"] += self.x_vel
        self.pos["y"] += self.y_vel 
        self.rect.center =[self.pos["x"], self.pos["y"] ]
        # self.circle_center = self.rect.center 
        screen.blit(self.image, self.rect)

enemy_spawn_list = [TorpedoCorvette(100, screen_height//2, 2), Enemy(250, 450, 1), Enemy(550, 150, 2), Enemy(650, 450, 4), TorpedoCorvette(850, 250, 3), Enemy(850, 550, 3), Enemy(1150, 250, 4), Enemy(1150, 800, 4), 
                    Enemy(1450, 250, 3), Enemy(1450, 800, 3),Enemy(1650, 150, 3), TorpedoCorvette(1650, 600, 3),Enemy(1150, 250, 4), Enemy(1150, 800, 4)]
level = LevelData(enemy_spawn_list)
bg = MlBackground()
player = Player(30, screen_height//2, 5)
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
main_menu = MainMenu()
pause_menu = PauseMenu()

paused = False
in_main_menu = True
while is_working:
    fps.tick(60)
    if in_main_menu:
        main_menu.update()

    elif paused:
        pause_menu.update()

    else:   
        pressed_keys = pygame.key.get_pressed()    
        if player.controllable:
            if pressed_keys[K_UP]:
                player.pos[1] -= player.speed
            if pressed_keys[K_DOWN]:
                player.pos[1] += player.speed
            if pressed_keys[K_LEFT]:
                player.pos[0] -= player.speed
            if pressed_keys[K_RIGHT]:
                player.pos[0] += player.speed
            # if pressed_keys[K_SPACE]:
            if pressed_keys[K_LCTRL]: # fixes bug, when pressing left, down and space, and movement stalls
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
        
        enemy_group.draw(screen)
        enemy_group.update()

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
            if not player.invincible:
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
        if event.type == pygame.MOUSEBUTTONDOWN and pause_menu.resume_button.mouse_pointed:
            paused = not paused
        if event.type == pygame.MOUSEBUTTONDOWN and main_menu.new_game_button.mouse_pointed:
            in_main_menu = False
            print("Click on resume")
        if event.type == pygame.MOUSEBUTTONDOWN and pause_menu.exit_button.mouse_pointed:
            in_main_menu = True
        if event.type == pygame.MOUSEBUTTONDOWN and main_menu.exit_button.mouse_pointed:
            print("Click on exit")
            is_working = False       
        # if event.type == CREATE_ENEMY:
        #     enemy_group.add(Enemy( screen_height *random.uniform(0, 0.8)))


    pygame.display.flip()













