import pygame

from pygame.constants import QUIT

pygame.init()

screen = width, height = 1000, 800
main_surface = pygame.display.set_mode(screen)
is_working = True

# Draw rectangle 
rect = pygame.Rect(100, 100, 200, 100)
color = (125, 125, 125)
pygame.draw.rect(main_surface, color,rect)

# Draw a circle 
center = (300, 300)
radius = 50
color = (100,0,255)
pygame.draw.circle(main_surface, color, center, radius)

# Draw a line
start = (50,400)
end = (300, 450)
color = (120, 210, 120)
pygame.draw.line(main_surface, color, start, end)

#render text 
font = pygame.font.Font(None, 36)
text = font.render("Hello there!", True, (120, 210, 120))
text_rect = text.get_rect(center = (width//2, height//2))
main_surface.blit(text, text_rect)










pygame.display.flip() # update display

while is_working:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
    
    