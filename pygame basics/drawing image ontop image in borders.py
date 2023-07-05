import pygame

pygame.init()
screen = pygame.display.set_mode((800, 800))

# Load the first image
image1 = pygame.image.load(r"sprites\player\miner_default.png")
image1_rect = image1.get_rect()

# Load the second image
image2 = pygame.image.load(r"sprites\player\miner_default.png")
image2 =pygame.transform.scale(image2, [image1.get_width(), image1.get_height()])
image2_rect = image2.get_rect()

# Set the position of the second image within the borders of the first image
image2_rect.center = image1_rect.center

# Create a temporary surface with an alpha channel to hold the combined images
temp_surface = pygame.Surface(image1_rect.size, pygame.SRCALPHA)
temp_surface.blit(image1, (0, 0))  # Draw the first image onto the temporary surface
temp_surface.blit(image2, image2_rect, special_flags=pygame.BLEND_RGBA_MIN)  # Draw the second image on top

# Draw the combined image on the screen
screen.blit(temp_surface, (0, 0))
pygame.display.flip()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
