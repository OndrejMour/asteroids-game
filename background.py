import pygame
import random
from constants import *

class Star:
    def __init__(self, x, y, size, brightness):
        self.position = pygame.Vector2(x, y)
        self.size = size
        self.brightness = brightness

class StarBackground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.stars = []
        self.generate_stars()

    def generate_stars(self):
        # Generování 200 hvězd s různou velikostí a jasem
        for _ in range(200):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.uniform(1, 3)
            brightness = random.randint(100, 255)
            self.stars.append(Star(x, y, size, brightness))

    def draw(self, screen):
        for star in self.stars:
            color = (star.brightness, star.brightness, star.brightness)
            pygame.draw.circle(screen, color, star.position, star.size) 