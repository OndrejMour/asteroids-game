import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
def main():
    pygame.init()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill((0, 0, 0))
        for updatable_object in updatable:
            updatable_object.update(dt)
        for drawable_object in drawable:
            drawable_object.draw(screen)
        # Procházíme kopii seznamu shots, protože během iterace měníme obsah
        for shot in list(shots):
            # Procházíme kopii seznamu asteroids, protože během iterace měníme obsah
            for asteroid in list(asteroids):
                if shot.check_collision(asteroid):
                    shot.pygame.sprite.Sprite.kill()
                    asteroid.pygame.sprite.Sprite.kill()
                    break  # Ukončíme vnitřní smyčku, protože střela už nemůže zasáhnout další asteroid
        for asteroid in asteroids:
            if player.check_collision(asteroid):
                print("Game over!")
                return
        pygame.display.flip()
        clock.tick(60)
        dt = clock.get_time() / 1000

if __name__ == "__main__":
    main()