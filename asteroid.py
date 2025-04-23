from circleshape import *
import pygame
from constants import *

class Asteroid(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        CircleShape.__init__(self, x, y, radius)
        pygame.sprite.Sprite.__init__(self)
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.velocity = pygame.Vector2(0, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius)

    def update(self, dt):
        self.position += self.velocity * dt
