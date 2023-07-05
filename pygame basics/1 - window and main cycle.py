import pygame
from pygame.constants import QUIT

pygame.init()

screen =  width, height = 1000, 700

#creates Window with certain size
main_surface = pygame.display.set_mode(screen) 
# returns pygame.Surface object

# main_surface = pygame.display.set_mode((700,500)) - other way to write
is_working = True


while is_working:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
