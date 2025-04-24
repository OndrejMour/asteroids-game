from circleshape import *
import pygame
import random
import math
from constants import *

class Asteroid(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        CircleShape.__init__(self, x, y, radius)
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.velocity = pygame.Vector2(0, 0)
        # Generování bodů pro nepravidelný tvar při inicializaci
        self.points = self._generate_points()
        # Směr světla (normalizovaný vektor)
        self.light_direction = pygame.Vector2(1, -1).normalize()

    def _generate_points(self):
        points = []
        num_points = 8  # Počet vrcholů asteroidu
        for i in range(num_points):
            angle = (2 * math.pi * i) / num_points
            # Přidání náhodné variace k poloměru pro nepravidelný tvar
            radius_variation = random.uniform(0.8, 1.2)
            x = self.position.x + math.cos(angle) * self.radius * radius_variation
            y = self.position.y + math.sin(angle) * self.radius * radius_variation
            points.append((x, y))
        return points

    def _calculate_shading(self, point):
        # Výpočet normálového vektoru pro daný bod
        center = pygame.Vector2(self.position)
        point_vec = pygame.Vector2(point)
        direction = point_vec - center
        
        # Kontrola na nulovou délku vektoru
        if direction.length() == 0:
            return (150, 150, 150)  # Vrátíme základní barvu pro středový bod
            
        normal = direction.normalize()
        
        # Výpočet intenzity stínování (dot product)
        intensity = max(0.3, normal.dot(self.light_direction))
        
        # Aplikace intenzity na základní barvu
        base_color = (150, 150, 150)
        shaded_color = tuple(int(c * intensity) for c in base_color)
        return shaded_color

    def draw(self, screen):
        # Vytvoření povrchu pro stínování
        surface = pygame.Surface((self.radius * 2.5, self.radius * 2.5), pygame.SRCALPHA)
        
        # Kreslení polygonu s gradientním stínováním
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            p3 = self.position
            
            # Výpočet stínování pro každý bod
            color1 = self._calculate_shading(p1)
            color2 = self._calculate_shading(p2)
            color3 = self._calculate_shading(p3)
            
            # Kreslení trojúhelníku s gradientním stínováním
            pygame.draw.polygon(surface, color1, [
                (p1[0] - self.position.x + self.radius * 1.25, p1[1] - self.position.y + self.radius * 1.25),
                (p2[0] - self.position.x + self.radius * 1.25, p2[1] - self.position.y + self.radius * 1.25),
                (p3[0] - self.position.x + self.radius * 1.25, p3[1] - self.position.y + self.radius * 1.25)
            ])
        
        # Přidání tmavšího okraje
        pygame.draw.polygon(surface, (100, 100, 100), [
            (p[0] - self.position.x + self.radius * 1.25, p[1] - self.position.y + self.radius * 1.25)
            for p in self.points
        ], 2)
        
        # Vykreslení povrchu na obrazovku
        screen.blit(surface, (self.position.x - self.radius * 1.25, self.position.y - self.radius * 1.25))

    def update(self, dt):
        self.position += self.velocity * dt
        
        # Aktualizace bodů polygonu podle nové pozice
        self.points = self._generate_points()
        
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
        

