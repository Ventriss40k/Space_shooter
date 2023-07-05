import pygame

pygame.init()

# Load the image
image = pygame.image.load(r"sprites\asteroid\asteroid-1.png")

# Get the dimensions of the image
image_width, image_height = image.get_size()

# Define the amount to increase the rectangle size by
padding = 10

# Create a rectangle that spans the entire image
rect = pygame.Rect(0, 0, image_width, image_height)

# Increase the size of the rectangle by the padding amount
rect.inflate_ip(padding*2, padding*2)

# Calculate the difference in size between the original and inflated rectangles
diff_x = rect.width - image_width
diff_y = rect.height - image_height

# Divide the difference by 2 to get the amount to adjust the position of the rectangle
adjust_x = diff_x // 2
adjust_y = diff_y // 2

# Adjust the position of the rectangle to keep the image centered within the new dimensions
rect.move_ip(-adjust_x, -adjust_y)

# Create a surface to blit the image onto
surface = pygame.Surface((rect.width, rect.height))

# Blit the image onto the surface, centered within the inflated rectangle
surface.blit(image, (adjust_x, adjust_y))
pygame.draw.rect(surface, (255, 0, 0), rect)
# Display the surface
screen = pygame.display.set_mode((rect.width, rect.height))
screen.blit(surface, (0, 0))
pygame.display.flip()

# Wait for the user to close the window
while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        pygame.quit()
        break
