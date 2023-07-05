import pygame

from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))



FPS = pygame.time.Clock()
is_working = True

while is_working:
    FPS.tick(60)





    for event in pygame.event.get():
        if event.type ==QUIT:
            is_working = False
    pygame.display.flip()