import pygame
from pygame.constants import QUIT

pygame.init()

screen_width = 800
screen_height = 600
screen  = pygame.display.set_mode((screen_width, screen_height))


image = pygame.image.load("sprites\player\Fighter-1.png") # load image


# display image
image_rect = image.get_rect(center = (100,100))
pygame.draw.rect(screen, (255, 0, 0), image_rect) # show rect
screen.blit(image, image_rect)


# scale image 
# scaled_image = pygame.transform.scale(image, (150,150))
scaled_image = pygame.transform.scale(image, (image_rect.width*2, image_rect.height*2))
scaled_image_rect = scaled_image.get_rect(center = (150, 200))
pygame.draw.rect(screen, (255, 0, 0), scaled_image_rect)
screen.blit(scaled_image, scaled_image_rect)

# rotate image
rotated_image = pygame.transform.rotate(image,45)
rotated_image_rect = rotated_image.get_rect(center = (100, 300))
pygame.draw.rect(screen, (255, 0, 0), rotated_image_rect)
screen.blit(rotated_image, rotated_image_rect)

# flip image 
flipped_image = pygame.transform.flip(image, True, False)
flipped_image_rect = flipped_image.get_rect(center = (100, 400))
screen.blit(flipped_image, flipped_image_rect)



pygame.display.flip()

while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        pygame.quit()
        break