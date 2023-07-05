import pygame

from pygame.constants import QUIT, K_DOWN, K_UP

pygame.init()


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))

FPS = pygame.time.Clock()
is_working = True

image = pygame.image.load(r"sprites\player\Fighter-1.png").convert_alpha()
image_rect = image.get_rect(center = (screen_width//2, screen_height//2))

rotated_image = image
rotated_image_rect = image_rect
rotation_degree = 0

while is_working:
    FPS.tick(60)
    pressed_keys = pygame.key.get_pressed()    


    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        
    
        
    if pressed_keys[K_UP]:
        if rotation_degree + 5 > 360:
            rotation_degree = 0
            
        else:
            rotation_degree += 5
            # FPS.tick(30)


    elif pressed_keys[K_DOWN]:
        if rotation_degree - 5 < 0:
            rotation_degree = 360
        else:
            rotation_degree -= 5        


    
    rotated_image = pygame.transform.rotate(image, rotation_degree)
    rotated_image_rect = image.get_rect(center = (screen_width//2, screen_height//2))
    screen.fill((0,0,0))
    # pygame.draw.rect(screen,(0,255,0), rotated_image_rect)
    screen.blit(rotated_image, rotated_image_rect)


    pygame.display.flip()