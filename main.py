import pygame
from constants import *
from player import Player

updatable = pygame.sprite.Group()
drawable = pygame.sprite.Group()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill((0, 0, 0))
        for updatable_object in updatable:
            updatable_object.update(dt)
        for drawable_object in drawable:
            drawable_object.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        dt = clock.get_time() / 1000

if __name__ == "__main__":
    main()