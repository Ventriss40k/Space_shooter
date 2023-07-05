import pygame
from pygame.constants import QUIT

pygame.init()

screen_width = 1000
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.mouse.set_visible(False)

BG = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\player\Fighter-1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft =(x, y)
        self.mask = pygame.mask.from_surface(self.image)

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, colour):
        pos = pygame.mouse.get_pos()
        self.rect.center = (pos)
        self.image.fill(colour)

# create instances
player = Player(350,250)
bullet = Bullet()

# create sprite groups
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

# add instances to groups
player_group.add(player)
bullet_group.add(bullet)
run = True

while run:
    screen.fill(BG)
    # sprite_collide(sprite, group, dokill, collided)
    
    col = GREEN
    if pygame.sprite.spritecollide(bullet, player_group, False, pygame.sprite.collide_rect):
        if pygame.sprite.spritecollide(bullet, player_group, False, pygame.sprite.collide_mask):
            col = RED

        

    bullet_group.update(col) # call the method for each instance of group
    player_group.draw(screen)
    bullet_group.draw(screen)

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
    pygame.display.flip()