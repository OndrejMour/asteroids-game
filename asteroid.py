from circleshape import *
import pygame
import random
from constants import *

class Asteroid(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        CircleShape.__init__(self, x, y, radius)
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.velocity = pygame.Vector2(0, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius)

    def update(self, dt):
        self.position += self.velocity * dt
        
        # Kontrola hranic obrazovky
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def split(self):
        self.kill()
        if self.radius < ASTEROID_MIN_RADIUS:
            return
        else:
            # Generování náhodného úhlu mezi 20 a 50 stupni
            random_angle = random.uniform(20, 50)
            
            # Vytvoření dvou nových vektorů rychlosti s opačným úhlem
            velocity1 = self.velocity.rotate(random_angle)
            velocity2 = self.velocity.rotate(-random_angle)
            
            # Výpočet nového poloměru
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            
            # Vytvoření dvou nových asteroidů
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            
            # Nastavení rychlostí s 1.2x větší velikostí
            asteroid1.velocity = velocity1 * 1.2
            asteroid2.velocity = velocity2 * 1.2
            
            return [asteroid1, asteroid2]
        

