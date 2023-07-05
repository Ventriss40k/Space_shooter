import pygame
from pygame.math import Vector2
import random

# Initialize Pygame
pygame.init()

# Set up the display window
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smoke Effect")

# Set up the clock
clock = pygame.time.Clock()

# Define the smoke particle class
class SmokeParticle:
    def __init__(self, pos):
        self.pos = Vector2(pos)
        self.vel = Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
        self.acc = Vector2(0, 0)
        self.size = random.randint(1, 3)
        self.color = (pygame.color.Color("grey4"))
        self.life = 30
        
    def update(self):
        self.vel += self.acc
        self.pos += self.vel
        self.life -= 1
        
        # If particle has died, remove it from the list
        if self.life <= 0:
            smoke_particles.remove(self)
            
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.size)
        
# Set up the list to hold the smoke particles
smoke_particles = []

# Set up the main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Spawn new particles
    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        for i in range(10):
            smoke_particles.append(SmokeParticle(mouse_pos))
    
    # Update particles
    for particle in smoke_particles:
        particle.update()
    
    # Draw particles
    SCREEN.fill((0, 0, 0))
    for particle in smoke_particles:
        particle.draw(SCREEN)
        
    # Update the display
    pygame.display.update()
    
    # Set the framerate
    clock.tick(60)

# Quit Pygame
pygame.quit()
