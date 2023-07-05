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



    screen.blit(bg, (0,0))
    player_group.update()
    player_group.draw(screen)









    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
    pygame.display.flip()













