from circleshape import *
import pygame
from constants import *

class Shot(CircleShape, pygame.sprite.Sprite):
    containers = None

    def __init__(self, x, y, radius):
        CircleShape.__init__(self, x, y, radius)
        pygame.sprite.Sprite.__init__(self)
        if self.containers:
            for container in self.containers:
                container.add(self)
        self.velocity = pygame.Vector2(0, 0)

    def update(self, dt):
        self.position += self.velocity * dt

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius)