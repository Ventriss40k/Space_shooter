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
        self.gun_cooldown = 200 
        self.gun_ready = True
    def update(self):
        self.rect.center = self.pos


    # This can be used not only to fire cursor
    # All you have to do is change mx, ne to your targets coords
    def shoot_cursor(self):
        # from where the shot is fired
        x_start = self.rect.right 
        Y_start = self.rect.bottom
        # difference between x,y of self and target
        dx = x_start - mx
        dy = Y_start - my
        # ratio of x/y, x% + y% = 1 
        x_percent = (abs(dx) / (abs(dx) + abs(dy))) * 100
        y_percent = (abs(dy) / (abs(dx) + abs(dy))) * 100
        # avoiding division on zero error later
        if x_percent == 0:
            x_percent = 0.001
        if y_percent == 0:
            y_percent = 0.001

        # chosing correct direction
        if mx > x_start:
            x_sign = 1
        elif mx < x_start:
            x_sign = -1
        else:
            x_sign = 0
        if my > Y_start:
            y_sign = 1
        elif my < Y_start:
            y_sign = -1
        else:
            y_sign = 0
        projectile_group.add(Projectile(x_start, Y_start, x_percent, y_percent, x_sign, y_sign))
        # gun cooldown
        self.gun_ready = False 
        pygame.time.set_timer(GUN_CD_EVENT, self.gun_cooldown)



class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, x_percent, y_percent, x_sign, y_sign):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,5))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 20
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
projectile_group = pygame.sprite.Group()


GUN_CD_EVENT = pygame.USEREVENT+4
pygame.time.set_timer(GUN_CD_EVENT, player.gun_cooldown)

while is_working:
    fps.tick(60)

    mx, my = pygame.mouse.get_pos()

    pressed_keys = pygame.key.get_pressed()    
    LMB_pressed = pygame.mouse.get_pressed()[0] # left mouse button press

    if pressed_keys[K_UP]:
        player.pos[1] -= player.speed
    if pressed_keys[K_DOWN]:
        player.pos[1] += player.speed
    if pressed_keys[K_LEFT]:
        player.pos[0] -= player.speed
    if pressed_keys[K_RIGHT]:
        player.pos[0] += player.speed
    if LMB_pressed:
        if player.gun_ready:
        # if player.rect.bottom < my and player.rect.right < mx and player.gun_ready:
            player.shoot_cursor()



    screen.blit(bg, (0,0))
    player_group.update()
    player_group.draw(screen)
    projectile_group.update()
    projectile_group.draw(screen)


    # print(len(projectile_group))





    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == GUN_CD_EVENT:
            player.gun_ready = True
    pygame.display.flip()













