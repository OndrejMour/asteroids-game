from circleshape import *
from constants import *
import pygame
from shot import Shot

class Player(CircleShape, pygame.sprite.Sprite):
    containers = None  # Bude nastaveno později

    def __init__(self, x, y):
        CircleShape.__init__(self, x, y, PLAYER_RADIUS)
        pygame.sprite.Sprite.__init__(self)
        if self.containers:
            for container in self.containers:
                container.add(self)
        self.rotation = 0
        self.shot_timer = SHOT_COOLDOWN  # Inicializace časovače
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, (0, 255, 0), self.triangle())

    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        # Získání pozice myši a výpočet směru
        mouse_pos = pygame.mouse.get_pos()
        direction = pygame.Vector2(mouse_pos) - self.position
        if direction.length() > 0:
            self.rotation = -direction.angle_to(pygame.Vector2(0, 1))

        # Přímočarý pohyb po osách
        if keys[pygame.K_w]:
            self.position.y -= PLAYER_SPEED * dt
        if keys[pygame.K_s]:
            self.position.y += PLAYER_SPEED * dt
        if keys[pygame.K_a]:
            self.position.x -= PLAYER_SPEED * dt
        if keys[pygame.K_d]:
            self.position.x += PLAYER_SPEED * dt
            
        # Kontrola hranic obrazovky
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
            
        # Střelba pomocí myši nebo mezerníku
        if pygame.mouse.get_pressed()[0] or keys[pygame.K_SPACE]:
            self.shoot(dt)
    
    def shoot(self, dt):
        self.shot_timer += dt
        if self.shot_timer >= SHOT_COOLDOWN:
            shot = Shot(self.position, self.rotation, SHOT_RADIUS)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED
            self.shot_timer -= SHOT_COOLDOWN