import pygame

from pygame.constants import QUIT, K_LEFT, K_RIGHT


pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))
FPS = pygame.time.Clock()
is_working = True

BG =(0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

pygame.mouse.set_visible(False)

player_image = pygame.image.load("sprites\player\Fighter-1.png").convert_alpha() # surface class
player_rect = player_image.get_rect()
player_mask = pygame.mask.from_surface(player_image) # actual mask (invisibl)
mask_image = player_mask.to_surface() # allows to see a representation of mask in screen as Surface

# enemy_image = pygame.image.load(r"sprites\asteroid\asteroid-1.png").convert_alpha()

bullet = pygame.Surface((10,10))
bullet.fill(RED)
bullet_mask = pygame.mask.from_surface(bullet)

player_rect.topleft = (350,250)

while is_working:
    FPS.tick(60)

    # get mouse position
    pos = pygame.mouse.get_pos()
    

    screen.fill(BG)

    #check mask overlap
    if player_mask.overlap(bullet_mask, (pos[0] - player_rect.x, pos[1] - player_rect.y)):
        col = RED
    else:
        col = GREEN

    screen.blit(mask_image, (0, 0))
    bullet.fill(col)
    screen.blit(bullet, pos)
    screen.blit(player_image, player_rect)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
    
    
    
    
    
    pygame.display.flip()