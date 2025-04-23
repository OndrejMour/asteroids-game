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

    def rotate(self, direction, dt):
        self.rotation += PLAYER_ROTATION_SPEED * dt * direction

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-1, dt)
        if keys[pygame.K_d]:
            self.rotate(1, dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot(dt)

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self, dt):
        self.shot_timer += dt
        if self.shot_timer >= SHOT_COOLDOWN:
            shot = Shot(self.position, self.rotation, SHOT_RADIUS)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED
            self.shot_timer = 0