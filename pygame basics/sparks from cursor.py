import pygame
import random

# Particle class
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.color = (255, 255, 0)
        self.lifespan = 40

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifespan -= 1

    def draw(self, screen):
        rect = pygame.Rect(self.x, self.y, 2, 2)
        pygame.draw.rect(screen, self.color, rect)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Sparks")

# Set up the clock
clock = pygame.time.Clock()

# Set up the list of particles
particles = []

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # Emit particles when the left mouse button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i in range(10):
                particles.append(Particle(event.pos[0], event.pos[1]))

    # Update particles
    for particle in particles:
        particle.update()

        # Remove particles with lifespan <= 0
        if particle.lifespan <= 0:
            particles.remove(particle)

    # Draw particles
    screen.fill((0, 0, 0))
    for particle in particles:
        particle.draw(screen)

    # Update the screen
    pygame.display.flip()

    # Tick the clock
    clock.tick(60)
