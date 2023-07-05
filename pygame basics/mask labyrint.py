import pygame

from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT


pygame.init()

screen_width = 1500
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
bg = pygame.image.load("sprites\Background_space.png").convert()
bg = pygame.transform.scale(bg, (screen_width, screen_height))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\player\Fighter-1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = [x, y]
        self.speed = speed
    def update(self):
        self.rect.center = self.pos



class Obstackle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("terrain\collision-map.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(screen_width, screen_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        pass

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("terrain\lava.png").convert()
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.rect = self.image.get_rect()
        self. rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect.top -=1


player = Player(30, screen_height - 50, 5)
obstackle = Obstackle(0,0)
lava = Lava(0, screen_height + 150)

player_group = pygame.sprite.Group()
obstackle_group = pygame.sprite.Group()

player_group.add(player)
obstackle_group.add(lava)
obstackle_group.add(obstackle)


FPS = pygame.time.Clock()
is_working = True

while is_working:
    FPS.tick(30)
    pressed_keys = pygame.key.get_pressed()    

    if pressed_keys[K_UP]:
        player.pos[1] -= player.speed
    if pressed_keys[K_DOWN]:
        player.pos[1] += player.speed
    if pressed_keys[K_LEFT]:
        player.pos[0] -= player.speed
    if pressed_keys[K_RIGHT]:
        player.pos[0] += player.speed

    if pygame.sprite.spritecollide(player, obstackle_group, False, pygame.sprite.collide_rect):
        if pygame.sprite.spritecollide(player, obstackle_group, False, pygame.sprite.collide_mask):
            player.pos = [30, screen_height - 50]

    screen.blit(bg, (0,0))
    obstackle_group.draw(screen)
    player_group.update()
    obstackle_group.update()
    player_group.draw(screen)
    

    for event in pygame.event.get():
        if event.type ==QUIT:
            is_working = False
    pygame.display.flip()