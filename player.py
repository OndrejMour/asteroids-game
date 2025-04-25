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
    
    def draw(self, screen):
        # Kreslení trupu
        self._draw_body(screen)
        # Kreslení motorů
        self._draw_engines(screen)
        # Kreslení kokpitu
        self._draw_cockpit(screen)

    def _draw_body(self, screen):
        # Trup lodi - jednoduchý trojúhelník
        body_length = self.radius * 1.5
        body_width = self.radius * 0.6
        
        # Hlavní část trupu
        body_points = [
            self.position + pygame.Vector2(0, -body_length).rotate(self.rotation),  # Předek
            self.position + pygame.Vector2(-body_width, body_length * 0.5).rotate(self.rotation),  # Levý zadní
            self.position + pygame.Vector2(body_width, body_length * 0.5).rotate(self.rotation),   # Pravý zadní
        ]
        pygame.draw.polygon(screen, (200, 200, 200), body_points)  # Světlejší šedá pro trup
        pygame.draw.polygon(screen, (100, 100, 100), body_points, 2)  # Tmavší obrys

    def _draw_engines(self, screen):
        engine_radius = self.radius * 0.2
        engine_offset = self.radius * 0.4
        
        engine_positions = [
            self.position + pygame.Vector2(-engine_offset, self.radius/4).rotate(self.rotation),
            self.position + pygame.Vector2(engine_offset, self.radius/4).rotate(self.rotation)
        ]
        
        for pos in engine_positions:
            # Vnější kruh motoru
            pygame.draw.circle(screen, (60, 60, 60), (int(pos.x), int(pos.y)), int(engine_radius))
            # Vnitřní kruh motoru - modrá
            pygame.draw.circle(screen, (50, 150, 255), (int(pos.x), int(pos.y)), int(engine_radius * 0.6))

    def _draw_cockpit(self, screen):
        cockpit_length = self.radius * 0.4
        cockpit_width = self.radius * 0.3
        cockpit_pos = self.position + pygame.Vector2(0, -self.radius * 0.5).rotate(self.rotation)
        
        cockpit_points = [
            cockpit_pos + pygame.Vector2(-cockpit_width/2, -cockpit_length/2).rotate(self.rotation),
            cockpit_pos + pygame.Vector2(cockpit_width/2, -cockpit_length/2).rotate(self.rotation),
            cockpit_pos + pygame.Vector2(cockpit_width/2, cockpit_length/2).rotate(self.rotation),
            cockpit_pos + pygame.Vector2(-cockpit_width/2, cockpit_length/2).rotate(self.rotation)
        ]
        
        pygame.draw.polygon(screen, (50, 50, 50), cockpit_points)
        pygame.draw.polygon(screen, (100, 200, 255), cockpit_points, 2)

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

    def check_collision(self, other):
        # Vypočítáme vzdálenost mezi středy
        distance = self.position.distance_to(other.position)
        
        # Zjednodušená hitbox - pouze kruh
        if distance < (self.radius + other.radius):
            return True
                
        return False