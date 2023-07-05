import pygame

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


class MlBackground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        # loading images and scaling them
        # layer1 - in the back, layer 3 - in the front
        self.layer1_img = pygame.transform.scale(pygame.image.load(r"sprites\background\Background_space.png").convert(), (screen_width, screen_height))
        self.layer2_img = pygame.transform.scale(pygame.image.load(r"sprites\background\darker_space_station.png").convert_alpha(), (screen_width//2, screen_height//2))
        # self.layer2_img = pygame.image.load(r"sprites\asteroid\background\bg_space_station.png").convert_alpha()

        self.layer3_img = pygame.transform.scale(pygame.image.load(r"sprites\background\bg_asteroids.png").convert_alpha(), (screen_width*1.7, screen_height))
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



 
    
bg = MlBackground()
player = Player(30, screen_height - 50, 5)
player_group = pygame.sprite.Group()
player_group.add(player)





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




    bg.update()   # this method is responsible for background drawing
    player_group.update()
    player_group.draw(screen)









    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
    pygame.display.flip()













