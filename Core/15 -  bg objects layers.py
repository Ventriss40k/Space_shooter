import pygame
import random
from random import randint
from pygame.constants import QUIT, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_SPACE, K_LCTRL, K_1, K_2, K_3, K_4
import math
from pygame.math import Vector2
from PIL import Image




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
        self.load_button = Button("Load", 0, 00, 80)
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
        
class LoadongScreen(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r"sprites\Art.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.level_n = 1
        self.font1 = pygame.font.Font(None, 130) 
        
        
        self.loading_data = ""
        self.font2 = pygame.font.Font(None, 50) 
        
    def update(self):
        self.text1 = self.font1.render(f"Level {self.level_n}", True, pygame.color.Color("Green3"))
        self.text1_rect = self.text1.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        self.text2 = self.font2.render(f"Loading ... {self.loading_data}", True, pygame.color.Color("Green3"))
        self.text2_rect = self.text2.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 65))

        screen.blit(self.image,(0,0))
        screen.blit(self.text1, self.text1_rect)
        screen.blit(self.text2, self.text2_rect)
        pygame.display.update()
class MlBackground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        # loading images and scaling them
        # layer1 - in the back, layer 3 - in the front
        self.layer1_img = pygame.transform.scale(pygame.image.load(r"sprites\background\Background_space.png").convert(), (screen_width, screen_height))
        self.layer2_img = pygame.transform.scale(pygame.image.load(r"sprites\background\darker_space_station.png").convert_alpha(), (screen_width//2, screen_height//2))
        # self.layer2_img = pygame.image.load(r"sprites\asteroid\background\bg_space_station.png").convert_alpha()
        self.layer3_img_def_size = [pygame.image.load(r"sprites\background\bg_asteroids_dark.png").get_width(),pygame.image.load(r"sprites\background\bg_asteroids_dark.png").get_height()]
        self.layer3_img_size_mult = screen_height/self.layer3_img_def_size[1]
        self.layer3_img = pygame.transform.scale(pygame.image.load(r"sprites\background\bg_asteroids_dark.png").convert_alpha(), (self.layer3_img_def_size[0]*self.layer3_img_size_mult, self.layer3_img_def_size[1]*self.layer3_img_size_mult))
        # getting positions of first and second background for each layer
        self.layer1_pos = {"x1": 0, "x2": self.layer1_img.get_width()}
        self.layer2_pos = {"x1": screen_width//3, "x2": self.layer2_img.get_width()}
        self.layer3_pos = {"x1": 0, "x2": self.layer3_img.get_width()}
        # speed of each layer. 
        self.layer1_speed = 0.1
        self.layer2_speed = 0.2
        self.layer3_speed = 2

        self.bg2_obj_counter_max = 25
        self.bg2_obj_counter = 0

    def update(self):
        self.layer1_pos["x1"] -= self.layer1_speed
        self.layer1_pos["x2"] -= self.layer1_speed
        self.layer2_pos["x1"] -= self.layer2_speed
        self.layer2_pos["x2"] -= self.layer2_speed
        self.layer3_pos["x1"] -= self.layer3_speed
        self.layer3_pos["x2"] -= self.layer3_speed
        if self.bg2_obj_counter == self.bg2_obj_counter_max:
            bg2_obj_group.add(Asteroid(root_folder=r"sprites\asteroid\asteroids_plan_2\asteroid_plan2_", y_min_max=[-0.2,0.2]))
            bg3_obj_group.add(Asteroid(root_folder=r"sprites\asteroid\asteroids_plan_3\asteroid_plan3_", y_min_max=[-0.2,0.2]))
            self.bg2_obj_counter = 0
        self.bg2_obj_counter +=1
        bg2_obj_group.update()
        bg3_obj_group.update()

        screen.blit(self.layer1_img, (self.layer1_pos["x1"],  0))
        screen.blit(self.layer1_img, (self.layer1_pos["x2"],  0))
        bg2_obj_group.draw(screen)
        screen.blit(self.layer2_img, (self.layer2_pos["x1"],  screen_width//3))
        # screen.blit(self.layer2_img, (self.layer2_pos["x2"],  0)) #  I only nned station to be drawn once
        # screen.blit(self.layer3_img, (self.layer3_pos["x1"],  0))
        # screen.blit(self.layer3_img, (self.layer3_pos["x2"],  0))
        bg2_obj_group.draw(screen)

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
    def __init__(self,enemy_spawn_list= []):
        self.level_n = 1
        self.distance = 0
        self.level_lenght = 7000
        self.progress = 0 
        self.enemy_spawn_list = enemy_spawn_list
        self.hazard_spawn_list = []
        self.difficulty = 1
    def update(self):
        self.distance += 1
        if self.get_progress()> 100:
            self.progress = 100
        else:
            self.progress = self.get_progress()
        self.spawn_enemy()
        self.spawn_hazard()
    def get_progress(self):
        if self.distance == 0:
            return 0
        else:
            return self.distance / self.level_lenght * 100
    
    def spawn_enemy(self):
        if self.enemy_spawn_list:
            if self.enemy_spawn_list[0].spawn_distance<= self.distance:
                enemy_group.add(self.enemy_spawn_list[0])
                self.enemy_spawn_list.pop(0)

    def spawn_hazard(self):
        if self.hazard_spawn_list:
            if self.hazard_spawn_list[0].spawn_distance <= self.distance:
                hazard_group.add(self.hazard_spawn_list[0])
                self.hazard_spawn_list.pop(0)
                # print("asteroid spawned")
    def spawn_bg_object(self):
        pass

    def level_complete(self):
        pass

class BasicGun():
    def __init__(self):
        self.cooldown_max = 50
        self.cooldown = 50
        self.color = pygame.Color("green")
        self.speed_x = 11
        self.speed_y = 0
        self.deviation_y = 0.2
        self.damage = 25
        self.proj_size =(15,5)
        self.name = "Basic gun"
    def shoot(self):
        if self.cooldown == 0:
            player_projectile_group.add(HorizontalProjectile(player.rect.centerx + player.rect.width//3, player.rect.centery, self.color, self.speed_x, self.speed_y, self.deviation_y, self.damage, self.proj_size))
            self.cooldown = self.cooldown_max
    def update(self):
        if self.cooldown >0:
            self.cooldown -=1


class FastGun():
    def __init__(self):
        self.cooldown_max = 10
        self.cooldown = 20
        self.color = pygame.Color("yellow1")
        self.speed_x = 10
        self.speed_y = 0
        self.deviation_y = 0.5
        self.damage = 10
        self.proj_size =(5,2)
        self.name = "Fast gun"
    def shoot(self):
        if self.cooldown == 0:
            player_projectile_group.add(HorizontalProjectile(player.rect.centerx+ player.rect.width//3, player.rect.centery, self.color, self.speed_x, self.speed_y, self.deviation_y, self.damage,self.proj_size))
            self.cooldown = self.cooldown_max
    def update(self):
        if self.cooldown >0:
            self.cooldown -=1

class DoubleBarrelGun():
    def __init__(self):
        self.cooldown_max = 17
        self.cooldown = 25
        self.color = pygame.Color("red1")
        self.speed_x = 9
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
                player_projectile_group.add(HorizontalProjectile(player.rect.centerx+ player.rect.width//3, player.rect.centery, self.color, self.speed_x, self.speed_y , self.deviation_y, self.damage, self.proj_size ))

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
        self.rect.center = self.pos
        self.muzzle_flash()
    def update(self):
        self.pos[0] += self.speed_x
        self.pos[1] += self.speed_y + self.deviation_y
        self.rect.center = self.pos
    def hit(self):
        if self.rect.centerx > 15 and self.rect.centerx < screen_width-15:
            smoke_particles_group.add(SmokeParticle(self.rect.center, color = self.color,))
        self.kill()
    def muzzle_flash(self):
        if self.rect.centerx > 15 and self.rect.centerx < screen_width-15:
            for i in range(3):
                smoke_particles_group.add(SmokeParticle(self.pos, color = self.color, speed_x=self.speed_x//5.5, speed_y=self.speed_y//5))





class Player(pygame.sprite.Sprite):
    def __init__ (self, x,y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.imgage_scale = 0.14
        # self.image_straight = pygame.image.load("sprites\player\miner_default.png").convert_alpha()
        # self.image_straight = pygame.transform.scale(self.image_straight,[self.image_straight.get_width()*self.imgage_scale, self.image_straight.get_height()*self.imgage_scale ]) 

        # self.image_up = pygame.image.load("sprites\player\miner_up.png").convert_alpha()
        # self.image_up = pygame.transform.scale(self.image_up,[self.image_up.get_width()*self.imgage_scale, self.image_up.get_height()*self.imgage_scale ]) 

        # self.image_down = pygame.image.load("sprites\player\miner_down.png").convert_alpha()
        # self.image_down = pygame.transform.scale(self.image_down,[self.image_down.get_width()*self.imgage_scale, self.image_down.get_height()*self.imgage_scale ]) 

        original_image = Image.open("sprites\player\miner_default.png")
        resized_image = original_image.resize((int(original_image.width * self.imgage_scale), int(original_image.height * self.imgage_scale)), resample=Image.Resampling.LANCZOS)
        pygame_image = pygame.image.fromstring(resized_image.tobytes(), resized_image.size, resized_image.mode).convert_alpha()
        self.image_straight = pygame_image

        original_image = Image.open("sprites\player\miner_up.png")
        resized_image = original_image.resize((int(original_image.width * self.imgage_scale), int(original_image.height * self.imgage_scale)), resample=Image.Resampling.LANCZOS)
        pygame_image = pygame.image.fromstring(resized_image.tobytes(), resized_image.size, resized_image.mode).convert_alpha()
        self.image_up = pygame_image

        original_image = Image.open("sprites\player\miner_down.png")
        resized_image = original_image.resize((int(original_image.width * self.imgage_scale), int(original_image.height * self.imgage_scale)), resample=Image.Resampling.LANCZOS)
        pygame_image = pygame.image.fromstring(resized_image.tobytes(), resized_image.size, resized_image.mode).convert_alpha()
        self.image_down = pygame_image

        # self.image_straight = Image.open("sprites\player\miner_default.png")
        # self.image_straight1 = self.image_straight.resize(self.image_straight.tobytes(), self.image_straight.width*self.imgage_scale, self.image_straight.height * self.imgage_scale,)
        # self.image_straight = pygame.image.fromstring(self.image_straight1.tobytes(), self.image_straight1.size, self.image_straight1.mode)

        # self.image_up = Image.open("sprites\player\miner_up.png")
        # self.image_up = self.image_up.resize(self.image_up.tobytes(), self.image_up.width*self.imgage_scale, self.image_up.height * self.imgage_scale,)
        # self.image_up = pygame.image.fromstring(self.image_up.tobytes(), self.image_up.size, self.image_up.mode)

        # self.image_down = Image.open("sprites\player\miner_default.png")
        # self.image_down = self.image_down.resize(self.image_down.tobytes(), self.image_down.width*self.imgage_scale, self.image_down.height * self.imgage_scale,)
        # self.image_down = pygame.image.fromstring(self.image_down.tobytes(), self.image_down.size, self.image_down.mode)


        self.image = self.image_straight
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.pos = [-100, -100]
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.alive = True
        self.hp = 100
        self.gun = BasicGun()
        # autopilot related
        self.controllable = False
        self.spawned = False
        self.spawned_arrived = False
        self.disengaged_arrived = False
        self.disengaging = False
        self.invincible = False
        # acceleration/movement related 
        self.max_up_vel = -self.speed
        self.max_down_vel = self.speed
        self.max_left_vel = -(self.speed / 1.2)
        self.max_right_vel = (self.speed * 1.5)
        self.acc_x =  0.3
        self.acc_y = 0.15
        self.vel_x = 0
        self.vel_y = 0

    def move_left(self):
        if self.vel_x - self.acc_x > self.max_left_vel:
            self.vel_x -= self.acc_x
        else:
            self.vel_x = self.max_left_vel
        smoke_particles_group.add(SmokeParticle([self.rect.left + 25, self.rect.centery-8], color = pygame.Color('darkslategray1'), speed_x= self.vel_x+1, speed_y = self.vel_y-1, deviation_y =0, lifetime=6, size_multiplyer=0.85, minsize=4, maxsize=4))
        smoke_particles_group.add(SmokeParticle([self.rect.left + 25, self.rect.centery+8], color = pygame.Color('darkslategray1'), speed_x= self.vel_x+1, speed_y = (self.vel_y+1), deviation_y =0, lifetime=6, size_multiplyer=0.85, minsize=4, maxsize=4))

    def move_right(self):
        if self.vel_x + self.acc_x < self.max_right_vel:
            self.vel_x += self.acc_x
        else:
            self.vel_x = self.max_right_vel
    def move_up(self):
        if self.vel_y - self.acc_y > self.max_up_vel:
            self.vel_y -= self.acc_y
        else:
            self.vel_y = self.max_up_vel
        smoke_particles_group.add(SmokeParticle([self.rect.centerx + 15, self.rect.centery+8], color = pygame.Color('darkslategray1'), speed_x= self.vel_x+1, speed_y = self.vel_y+1, deviation_y =0, lifetime=6, size_multiplyer=0.85, minsize=4, maxsize=4))
        smoke_particles_group.add(SmokeParticle([self.rect.centerx - 15, self.rect.centery+8], color = pygame.Color('darkslategray1'), speed_x= self.vel_x-1, speed_y = self.vel_y+1, deviation_y =0, lifetime=6, size_multiplyer=0.85, minsize=4, maxsize=4))

    def move_down(self):
        if self.vel_y + self.acc_y < self.max_down_vel:
            self.vel_y += self.acc_y
        else:
            self.vel_y = self.max_down_vel
        smoke_particles_group.add(SmokeParticle([self.rect.centerx + 15, self.rect.centery-8], color = pygame.Color('darkslategray1'), speed_x= self.vel_x+1, speed_y = self.vel_y-1, deviation_y =0, lifetime=6, size_multiplyer=0.85, minsize=4, maxsize=4))
        smoke_particles_group.add(SmokeParticle([self.rect.centerx - 15, self.rect.centery-8], color = pygame.Color('darkslategray1'), speed_x= self.vel_x-1, speed_y = self.vel_y-1, deviation_y =0, lifetime=6, size_multiplyer=0.85, minsize=4, maxsize=4))

    def stabilize_x(self):
        pass
    def stabilize_y(self):
            pass
    def update(self):

        self.rect.center = self.pos
        self.gun.update()
        if self.hp<0:
            self.alive = False
            self.kill()
        if not self.spawned_arrived:
            self.spawn()
        if level.progress >=100:
            self.disengage()
       
        self.pos[0] += self.vel_x
        self.pos[1] += self.vel_y
        if self.spawned_arrived and not self.disengaging:
            smoke_particles_group.add(SmokeParticle([self.rect.left + 20, self.rect.centery], color = pygame.Color('darkslategray1'), speed_x= -self.speed, speed_y = self.vel_y, deviation_y =0, lifetime=10, size_multiplyer=0.8, minsize=7, maxsize=7))
        
        if self.vel_y <1.5 and self.vel_y >-1.5:
            self.image = self.image_straight
            # print("img str")
        if self.vel_y >= 1.5:
            self.image = self.image_down
            # print("img down")
        elif self.vel_y <= -1.5:
            self.image = self.image_up
            # print("img up")



    def spawn(self):
        if self.spawned == False:
            self.pos = [-250, screen_height//2]
            self.spawned = True
        if not self.spawned_arrived:
            if self.rect.left > 0:
                smoke_particles_group.add(SmokeParticle([self.rect.left,self.rect.centery], color = pygame.Color('darkslategray1')))
            if self.autopilot([screen_width//4, screen_height//2],2):
                self.spawned_arrived = True
                self.controllable = True


    def disengage(self):
        self.controllable = False
        # triggering when level progress ==100
        if not self.disengaged_arrived:
            smoke_particles_group.add(SmokeParticle([self.rect.left,self.rect.centery], color = pygame.Color('darkslategray1')))
            if self.autopilot([screen_width*1.2, screen_height//2],2):
                self.disengaged_arrived = True


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
       
        if self.pos[0] >= target_pos[0]:
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
        self.level_n_pos = (screen_width - 140, 0)
        self.progress_pos = (screen_width - 140, 20)
        
    def update(self):
        self.hp = player.hp
        self.hp_obj = self.font.render(f"Hull integrity: {self.hp}", True, self.color)
        self.gun = player.gun
        self.gun_obj = self.font.render(f"Active weapon: {self.gun.name}", True, self.color)
        self.level_n = level.level_n
        self.level_n_obj = self.font.render(f"Level {self.level_n}", True, self.color)
        self.progress = int(level.progress)
        self.progress_obj = self.font.render(f"Completed: {self.progress}%", True, self.color)

    def draw(self):
        screen.blit(self.hp_obj, self.hp_pos)
        screen.blit(self.gun_obj, self.gun_pos)
        screen.blit(self.level_n_obj, self.level_n_pos)
        screen.blit(self.progress_obj, self.progress_pos)
        # self.cooldown_max = 17
        # self.cooldown = 25
class SmokeParticle(pygame.sprite.Sprite):
    def __init__(self, pos, color = pygame.color.Color("gray64"),deviation_x=0.5, deviation_y=0.5, speed_x = 0, speed_y=0, lifetime = 45, size_multiplyer = 0.95, minsize = 3, maxsize=10):
        pygame.sprite.Sprite.__init__(self)
        self.pos = Vector2(pos)
        self.deviation_x = deviation_x 
        self.deviation_y = deviation_y 
        self.size_multiplyer = size_multiplyer
        self.vel = Vector2(random.uniform(-deviation_x + speed_x, deviation_x + speed_x), random.uniform(-deviation_y + speed_y, deviation_y + speed_y))
        self.acc = Vector2(0, 0)
        self.size = random.randint(minsize, maxsize)
        self.color = color
        self.life = lifetime


    def update(self):


        
        # If particle has died, remove it from the list
        if self.life <= 0:
            self.kill()
        if self.pos[0]<=15 or self.pos[0]>screen_width-15:
            self.kill()
        pygame.draw.circle(screen, self.color, self.pos, self.size)   

        self.vel += self.acc
        self.pos += self.vel
        self.size *= self.size_multiplyer
        self.life -= 1
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



# class Explosion (pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.image.load(r"sprites\explosions\explosion-1.png")
#         self.lifetime = 40
#         self.rect = self.image.get_rect()
#         self.rect.center = (x,y)
#     def update(self):
#         self.lifetime -=1
#         if self.lifetime <= 0:
#             self.kill()
#         elif self.lifetime <= 10:
#             self.image = pygame.image.load(r"sprites\explosions\explosion-4.png")
#         elif self.lifetime <= 20:
#             self.image = pygame.image.load(r"sprites\explosions\explosion-3.png")
#         elif self.lifetime <= 30:
#             self.image = pygame.image.load(r"sprites\explosions\explosion-2.png")

class Explosion (pygame.sprite.Sprite):
    def __init__(self, x, y, lifetime =40, diameter = 100, imgages = [pygame.image.load(r"sprites\explosions\explosion-1.png"), pygame.image.load(r"sprites\explosions\explosion-2.png"),
                                                                      pygame.image.load(r"sprites\explosions\explosion-3.png"),pygame.image.load(r"sprites\explosions\explosion-2.png")]):
        pygame.sprite.Sprite.__init__(self)
        
        self.lifetime = lifetime
        self.diameter = diameter
        self.images = imgages
        self.frame_time = self.lifetime//len(self.images)
        self.counter = 0
        self.image_n = 0
        self.image = self.images[self.image_n]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    def update(self):
        self.counter+=1 
        if self.counter>=self.frame_time:
            self.counter=0
            self.image_n += 1 
            if self.image_n > len(self.images)-1:
                self.kill()
            else:
                self.image = self.images[self.image_n]

            




class Asteroid(pygame.sprite.Sprite):
    def __init__(self, spawn_distance = 0, x =screen_width+150, y=0, scale_min = 0.2, scale_max= 1, y_min_max ="default", scale = "random", root_folder =r"sprites\asteroid\asteroids_plan_1 (300х300)\asteroid_plan1_" ):
        pygame.sprite.Sprite.__init__(self)
        if scale == "random":
            self.scale = random.uniform(scale_min, scale_max)
        else:
            self.scale = scale
        self.image_n = randint(1, 16)
        # self.image = pygame.image.load(fr"sprites\asteroid\asteroid_plan1_1.png").convert_alpha()
        # self.image = pygame.transform.scale(self.image,(self.image.get_size()[0]*self.scale , self.image.get_size()[1]*self.scale))
        

        original_image = Image.open(fr"{root_folder}{self.image_n}.png")
        resized_image = original_image.resize((int(original_image.width *self.scale), int(original_image.height *self.scale)), resample=Image.Resampling.LANCZOS)
        pygame_image = pygame.image.fromstring(resized_image.tobytes(), resized_image.size, resized_image.mode).convert_alpha()
        self.image = pygame_image
        self.def_image = self.image


        self.def_rect = self.def_image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation_period = randint(int(self.scale), int(self.scale*1.5))
        self.rotation_counter = 0
        self.current_angle = 0
        self.area = self.image.get_width()*self.image.get_height()
        self.rect = self.image.get_rect()
        self.spawn_distance = spawn_distance
        self.y = randint(-140, screen_height + 140)
        self.rect.center = [x,self.y]
        self.vel_x = randint(2,5)*-1
        if y_min_max == "default":
            if self.y >=0 and self.y <=screen_height:
                self.vel_y = randint(-2,2)
            elif self.y > screen_height:
                self.vel_y = randint(-2,-0)
            elif self.y < 0:
                self.vel_y = randint(0, 2)
        else:
            self.vel_y = random.uniform(y_min_max[0], y_min_max[1])  
        self.hp = self.area//1000*25
        self.pos = [x, self.y]
        
    def update(self):
        # rotation
        # self.rotation_counter +=1
        # if self.rotation_counter >= self.rotation_period:
        #     self.rotation_counter = 0 
            
        #     if self.current_angle >= 360:
        #         self.current_angle = 0
        #     self.image = pygame.transform.rotate(self.def_image, self.current_angle)
        #     self.mask = pygame.mask.from_surface(self.image)
        #     self.current_angle+=0.4
            # self.rect.center = self.pos
        self.rect.center = (self.def_image.get_rect().centerx - int(self.image.get_width()//2) +50, self.def_image.get_rect().centery - (self.image.get_height()//2)+50)
        self.rect.centerx += self.pos[0]
        self.rect.centery += self.pos[1]
    
        self.pos[0] += self.vel_x
        self.pos[1] += self.vel_y
        if self.hp <=0:
            # hazard_group.add(Asteroid(x= self.pos[0], y= self.pos[1]))
            self.kill()
        if self.pos[0] < -150 or self.pos[0] > screen_width + 150 or self.pos[1] < -150 or self.pos[1] > screen_height+ 150:
            self.kill()

class Enemy (pygame.sprite.Sprite):
    def __init__(self,spawn_distance = 0, y= randint(0, screen_height), behavior =1, x = screen_width+50,  ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\enemies\enemy_pirate_fighter.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image.get_size()[0]//3 , self.image.get_size()[1]//3))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.pos = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_nominal = 1.5
        self.speed = self.speed_nominal
        self.y_speed = 1.5
        self.gun_cooldown_nominal = 50
        self.gun_cooldown_max = self.gun_cooldown_nominal
        self.gun_cooldown = self.gun_cooldown_nominal
        self.maneuver_countdow = 100
        self.y_vector = random.choice([1,-1])
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
        self.pos[1] += self.y_speed * self.y_vector
    

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
        else:
            for hazard in hazard_group:
                if hazard.rect.centery + deviation >= self.rect.centery and player.rect.centery - deviation <= self.rect.centery and self.rect.centerx - hazard.rect.centerx <=300:
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
        self.hp = 75
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

        self.thruster_fire_right0 = pygame.image.load("sprites\enemies\Torpedo corvette\Thruster fire_0.png").convert_alpha()
        self.thruster_fire_right0 = pygame.transform.scale(self.thruster_fire_right0, (self.thruster_fire_right0.get_size()[0]//3.5, self.thruster_fire_right0.get_size()[1]//3))
        self.thruster_fire_right1 = pygame.image.load("sprites\enemies\Torpedo corvette\Thruster fire_1.png").convert_alpha()
        self.thruster_fire_right1 = pygame.transform.scale(self.thruster_fire_right1, (self.thruster_fire_right1.get_size()[0]//4, self.thruster_fire_right1.get_size()[1]//3))


        self.thruster_fire_right2 = pygame.image.load("sprites\enemies\Torpedo corvette\Thruster fire_2.png").convert_alpha()
        self.thruster_fire_right2 = pygame.transform.scale(self.thruster_fire_right0, (self.thruster_fire_right2.get_size()[0]//4.5, self.thruster_fire_right2.get_size()[1]//3))

        self.thruster_fire_right3 = pygame.image.load("sprites\enemies\Torpedo corvette\Thruster fire_3.png").convert_alpha()
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
        self.image = pygame.image.load(r"sprites\enemies\Projectiles\Rocket_autopilot\rocket_enemy_autopilot_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image.get_size()[0]//7 , self.image.get_size()[1]//7))

        self.images = [pygame.image.load(r"sprites\enemies\Projectiles\Rocket_autopilot\rocket_enemy_autopilot_1.png").convert_alpha(),
                       pygame.image.load(r"sprites\enemies\Projectiles\Rocket_autopilot\rocket_enemy_autopilot_2.png").convert_alpha(),
                       pygame.image.load(r"sprites\enemies\Projectiles\Rocket_autopilot\rocket_enemy_autopilot_3.png").convert_alpha(),
                       pygame.image.load(r"sprites\enemies\Projectiles\Rocket_autopilot\rocket_enemy_autopilot_4.png").convert_alpha()]
        for index, i in enumerate(self.images):
            i = pygame.transform.scale(i,(i.get_size()[0]//7 , i.get_size()[1]//7))
            self.images[index] = i
        self.expl_images =[pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_1.png').convert_alpha(),pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_2.png').convert_alpha(),
                                                                                      pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_3.png').convert_alpha(),pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_4.png').convert_alpha(),
                                                                                      pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_5.png').convert_alpha(),pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_6.png').convert_alpha(),
                                                                                      pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_7.png').convert_alpha(),pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_8.png').convert_alpha(),
                                                                                      pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_9.png').convert_alpha(),pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_10.png').convert_alpha(),]
        self.image_counter = 0
        self.image_max_counter = 4
        self.image_frame = 0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = [x, y]
        self.pos = [x, y]
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.damage = damage
        self.target = target
    def update(self):
        if self.image_counter >= self.image_max_counter:
            self.image_counter = 0
            self.image_frame+=1
            if self.image_frame > len(self.images)-1:
                self.image_frame = 0
            self.image = self.images[self.image_frame]
        self.image_counter +=1
        
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
    def hit(self):
        smoke_particles_group.add(SmokeParticle(self.rect.center))
        self.explode()
        self.kill()
        
    def explode(self):
        explosions_group.add(Explosion(self.rect.centerx, self.rect.centery,imgages= self.expl_images ))
        self.kill()
    # def explode(self):
    #     explosions_group.add(Explosion(self.rect.centerx, self.rect.centery, imgages=[pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_1.png').convert_alpha(),pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_2.png').convert_alpha(),
    #                                                                                   pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_3.png').convert_alpha(),pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_4.png').convert_alpha(),
    #                                                                                   pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_5.png').convert_alpha(),pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_6.png').convert_alpha(),
    #                                                                                   pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_7.png').convert_alpha(),pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_8.png').convert_alpha(),
    #                                                                                   pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_9.png').convert_alpha(),pygame.image.load(r'sprites\explosions\rocket_explosions\explosion_10.png').convert_alpha(),]))
    #     self.kill()
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
    def hit(self):
        smoke_particles_group.add(SmokeParticle((self.rect.centerx, self.rect.centery) ))
        self.kill()
# Enemy generation related

# Enemy Formations
class EnemyFormation():
    def __init__(self, enemy_lst, value, spawn_distance, altitude, speed = 5):
        self.enemy_lst = enemy_lst
        self.value = value
        self.spawn_distance = spawn_distance
        self.altitude = altitude
        self.speed = speed
    def lst_append(self, lst):
        new_enemy_lst = lst
        for enemy in self.enemy_lst:
            enemy.spawn_distance += self.spawn_distance
            enemy.pos[1] += self.altitude
            enemy.speed = self.speed
            enemy.speed_nominal = self.speed 
            new_enemy_lst.append(enemy)
        return new_enemy_lst
        


def enemy_gen():
    enemy_points = round(level.level_lenght* level.difficulty//100)
    points_per_span = enemy_points//10
    distance_span = level.level_lenght//10
    min_dist = 0
    max_dist = distance_span
    used_points = 0
    current_span = 0
    new_formations = []
    level.enemy_spawn_list = []
    while True:
        form = randint(1,4)
        if form ==1:
            new_formations.append(EnemyFormation ([Enemy(spawn_distance=0, y = 0, behavior= 3), Enemy(spawn_distance=49, y = 50, behavior= 3),Enemy(spawn_distance=15, y = -50, behavior= 3)],4, randint(min_dist, max_dist),randint(50,screen_height-50),2 ))
            used_points += 4
        elif form ==2:
            new_formations.append(EnemyFormation ([Enemy(spawn_distance=0, y = 0, behavior= 1), Enemy(spawn_distance=49, y = 50, behavior= 1),Enemy(spawn_distance=15, y = -50, behavior= 1)],2, randint(min_dist, max_dist),randint(50,screen_height-50),5 ))
            used_points += 2
        elif form ==3:   
            new_formations.append(EnemyFormation ([Enemy(spawn_distance=0, y = 0, behavior= 3), Enemy(spawn_distance=49, y = 50, behavior= 3),Enemy(spawn_distance=15, y = -50, behavior= 3)],3, randint(min_dist, max_dist),randint(50,screen_height-50),5  ))
            used_points += 3
        elif form ==4:
            new_formations.append(EnemyFormation ([ Enemy(spawn_distance= 0, y = 70, behavior= 3),Enemy(spawn_distance= 0, y = -70, behavior= 3), TorpedoCorvette(spawn_distance=60, y = 0, behavior= 3),],6, randint(min_dist, max_dist),randint(50,screen_height-50),2 ))
            used_points += 6
        current_span = used_points//points_per_span
        min_dist = 0 + distance_span*current_span
        max_dist = distance_span + distance_span*current_span
        if current_span > 10:
            break
        
    new_formations = sorted(new_formations, key= lambda obj: obj.spawn_distance)
    for i in new_formations:
        level.enemy_spawn_list = i.lst_append(level.enemy_spawn_list)

def hazard_gen():
    hazard_level = 5
    distance_span = level.level_lenght//150
    min_dist = 0
    max_dist = distance_span
    level.hazard_spawn_list =[]
    for i in range(int(level.level_lenght//distance_span* hazard_level)):
        level.hazard_spawn_list.append(Asteroid(spawn_distance=randint(min_dist,max_dist)))
        min_dist += distance_span
        max_dist += distance_span


# def level_gen():
#     global level, bg, player_projectile_group, enemy_group, player_interface, enemy_projectiles, hazard_group, explosions_group, smoke_particles_group, in_main_menu, paused
    # level = LevelData(enemy_spawn_list =[])
    # enemy_gen()
    # hazard_gen()
    # bg = MlBackground()
    # player = Player(30, screen_height//2, 5)
    # player_group = pygame.sprite.Group()
    # player_group.add(player)
    # player_projectile_group = pygame.sprite.Group()
    # enemy_group = pygame.sprite.Group()
    # player_interface = PlayerInterface()
    # enemy_projectiles = pygame.sprite.Group()
    # hazard_group = pygame.sprite.Group()
    # explosions_group = pygame.sprite.Group()
    # smoke_particles_group = pygame.sprite.Group()
    # in_main_menu = False
    # paused = False
    # main_menu.new_game_button.mouse_pointed = False


# level = LevelData(enemy_spawn_list =[])
# enemy_gen()
# hazard_gen()
# bg = MlBackground()
# player = Player(30, screen_height//2, 5)
# player_group = pygame.sprite.Group()
# player_group.add(player)
# player_projectile_group = pygame.sprite.Group()
# player_interface = PlayerInterface()

# enemy = Enemy(screen_width - 130,300)
# enemy_group = pygame.sprite.Group()
# enemy_group.add(enemy)
# enemy_projectiles = pygame.sprite.Group()
# hazard_group = pygame.sprite.Group()

# explosions_group = pygame.sprite.Group()
# smoke_particles_group = pygame.sprite.Group()
main_menu = MainMenu()
pause_menu = PauseMenu()
player_group = pygame.sprite.Group()
loading_screen = LoadongScreen()
bg2_obj_group = pygame.sprite.Group()
bg3_obj_group = pygame.sprite.Group()
paused = False
in_main_menu = True
while is_working:
    fps.tick(60)
    if in_main_menu:
        
        main_menu.update()

    elif paused:
        pause_menu.update()

    # transfer to next level
    elif level.progress >=100 and player.disengaged_arrived:
        loading_screen.level_n +=1
        loading_screen.update()
        # level.progress = 0
        level.distance = 0
        # level = LevelData(enemy_spawn_list =[])
        level.enemy_spawn_list =[]
        level.difficulty *=2
        level.level_n +=1

        enemy_gen()
        hazard_gen()
        bg = MlBackground()
        bg2_obj_group = pygame.sprite.Group()
        player = Player(30, screen_height//2, 5)
        player_group = pygame.sprite.Group()
        player_group.add(player)
        player_projectile_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        player_interface = PlayerInterface()
        enemy_projectiles = pygame.sprite.Group()
        hazard_group = pygame.sprite.Group()
        explosions_group = pygame.sprite.Group()
        smoke_particles_group = pygame.sprite.Group()
        in_main_menu = False
        paused = False
        main_menu.new_game_button.mouse_pointed = False           
    else:   
        # print("in game")
        pressed_keys = pygame.key.get_pressed()    
        if player.controllable and player.alive:
            if pressed_keys[K_UP]:
                # player.pos[1] -= player.speed
                player.move_up()
            if pressed_keys[K_DOWN]:
                # player.pos[1] += player.speed
                player.move_down()
            if pressed_keys[K_LEFT]:
                # player.pos[0] -= player.speed
                player.move_left()
            if pressed_keys[K_RIGHT]:
                player.move_right()
                # player.pos[0] += player.speed
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
        hazard_group.draw(screen)
        hazard_group.update()

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
            if not player.invincible and player.alive:
                if pygame.sprite.spritecollide(projectile, player_group, False, pygame.sprite.collide_rect):
                    if pygame.sprite.spritecollide(projectile, player_group, False, pygame.sprite.collide_mask):
                        projectile.hit()
                        player.hp -= projectile.damage
            for hazard in hazard_group:
                if pygame.sprite.spritecollide(projectile, hazard_group, False, pygame.sprite.collide_rect):
                    if pygame.sprite.spritecollide(projectile, hazard_group, False, pygame.sprite.collide_mask):
                        hazard.hp -= projectile.damage
                        projectile.hit()


        for projectile in player_projectile_group:
            if projectile.rect.left > screen_width:
                projectile.kill()
            for enemy in enemy_group:
                if projectile.rect.colliderect(enemy.rect):
                    if pygame.sprite.collide_mask(enemy, projectile):
                        projectile.hit()
                        enemy.hp -= projectile.damage
            for hazard in hazard_group:
                if pygame.sprite.spritecollide(projectile, hazard_group, False, pygame.sprite.collide_rect):
                    if pygame.sprite.spritecollide(projectile, hazard_group, False, pygame.sprite.collide_mask):
                        hazard.hp -= projectile.damage
                        projectile.hit()    
        
        for hazard in hazard_group:
            if not player.invincible and player.alive:
                if pygame.sprite.spritecollide(hazard, player_group, False, pygame.sprite.collide_mask):
                            hazard.hp -= 5
                            player.hp -= 1
            for enemy in enemy_group:
                if pygame.sprite.spritecollide(enemy, hazard_group, False, pygame.sprite.collide_rect):
                    if pygame.sprite.spritecollide(enemy, hazard_group, False, pygame.sprite.collide_mask):
                        hazard.hp -= 5
                        enemy.hp -= 1
        
        for hazard in hazard_group:
            if hazard.rect.right <0:
                hazard.kill()

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
        # Main menu
        if event.type == pygame.MOUSEBUTTONDOWN and pause_menu.resume_button.mouse_pointed and not in_main_menu:
            paused = not paused
            print("Click on resume")
            pause_menu.resume_button.mouse_pointed = False
        elif event.type == pygame.MOUSEBUTTONDOWN and main_menu.new_game_button.mouse_pointed:
            # loading_screen.loading_data = "level data"
            loading_screen.update()
            level = LevelData(enemy_spawn_list =[])
            # loading_screen.loading_data = "enemies"
            # loading_screen.update()
            enemy_gen()
            # loading_screen.loading_data = "hazards"
            # loading_screen.update()
            hazard_gen()
            bg = MlBackground()
            bg2_obj_group = pygame.sprite.Group()
            player = Player(30, screen_height//2, 5)
            player_group = pygame.sprite.Group()
            player_group.add(player)
            player_projectile_group = pygame.sprite.Group()
            enemy_group = pygame.sprite.Group()
            player_interface = PlayerInterface()
            enemy_projectiles = pygame.sprite.Group()
            hazard_group = pygame.sprite.Group()
            explosions_group = pygame.sprite.Group()
            smoke_particles_group = pygame.sprite.Group()
            in_main_menu = False
            paused = False
            main_menu.new_game_button.mouse_pointed = False

            print("Click on new game")
        if event.type == pygame.MOUSEBUTTONDOWN and pause_menu.exit_button.mouse_pointed:
            in_main_menu = True
            paused = False
            pause_menu.exit_button.mouse_pointed = not pause_menu.exit_button.mouse_pointed
        if event.type == pygame.MOUSEBUTTONDOWN and main_menu.exit_button.mouse_pointed:
            print("Click on exit")
            is_working = False       
            main_menu.exit_button.mouse_pointed = False
        # if event.type == CREATE_ENEMY:
        #     enemy_group.add(Enemy( screen_height *random.uniform(0, 0.8)))


    pygame.display.flip()













