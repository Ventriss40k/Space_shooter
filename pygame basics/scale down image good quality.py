import pygame
from PIL import Image

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Load the original image using Pillow
original_image = Image.open("sprites\player\miner_up.png")

# Resize the image using Lanczos resampling
resized_image = original_image.resize((original_image.width // 10, original_image.height // 10), resample=Image.LANCZOS)

# Convert the resized image to a Pygame surface
pygame_image = pygame.image.fromstring(resized_image.tobytes(), resized_image.size, resized_image.mode)

# Display the resized image
screen.blit(pygame_image, (0, 0))
pygame.display.flip()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
