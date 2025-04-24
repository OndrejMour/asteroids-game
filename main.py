import pygame
import json
import os
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from background import StarBackground

# Konstanty pro bodování
SCORE_PER_SECOND = 1
SCORE_PER_ASTEROID = 10
HIGHSCORE_FILE = "highscore.json"

def load_highscore():
    try:
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return 0

def save_highscore(score):
    try:
        with open(HIGHSCORE_FILE, 'w') as f:
            json.dump(score, f)
    except:
        pass

def main():
    pygame.init()
    
    # Inicializace zvuku s ošetřením chyby
    try:
        pygame.mixer.init()
        sound_enabled = True
    except pygame.error:
        print("Varování: Zvukové zařízení není dostupné. Hra poběží bez zvuku.")
        sound_enabled = False
    
    # Načtení zvuků
    shoot_sound = None
    explosion_sound = None
    if sound_enabled:
        try:
            shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
            explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')
        except:
            print("Varování: Zvukové soubory nebyly nalezeny. Hra poběží bez zvuku.")
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    
    # Inicializace skóre
    score = 0
    highscore = load_highscore()
    game_time = 0
    
    # Inicializace hvězdného pozadí
    background = StarBackground()
    
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    
    # Inicializace fontu pro zobrazení skóre
    font = pygame.font.Font(None, 36)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and shoot_sound:
                    shoot_sound.play()
                elif event.key == pygame.K_ESCAPE:
                    return
        
        screen.fill((0, 0, 0))
        # Vykreslení hvězdného pozadí
        background.draw(screen)
        
        for updatable_object in updatable:
            updatable_object.update(dt)
        for drawable_object in drawable:
            drawable_object.draw(screen)
        
        # Aktualizace skóre za přežití
        game_time += dt
        score = int(game_time * SCORE_PER_SECOND)
        
        # Procházíme kopii seznamu shots, protože během iterace měníme obsah
        for shot in list(shots):
            # Procházíme kopii seznamu asteroids, protože během iterace měníme obsah
            for asteroid in list(asteroids):
                if shot.check_collision(asteroid):
                    shot.kill()
                    asteroid.split()
                    score += SCORE_PER_ASTEROID
                    if explosion_sound:
                        explosion_sound.play()
                    break  # Ukončíme vnitřní smyčku, protože střela už nemůže zasáhnout další asteroid
        
        for asteroid in asteroids:
            if player.check_collision(asteroid):
                if explosion_sound:
                    explosion_sound.play()
                print(f"Game over! Skóre: {score}")
                if score > highscore:
                    highscore = score
                    save_highscore(highscore)
                    print(f"Nové high skóre: {highscore}!")
                return
        
        # Kontrola, zda je hráč stále na obrazovce
        if (player.position.x < 0 or player.position.x > SCREEN_WIDTH or 
            player.position.y < 0 or player.position.y > SCREEN_HEIGHT):
            # Hráč je mimo obrazovku, ale hra pokračuje
            pass
        
        # Zobrazení skóre
        score_text = font.render(f"Skóre: {score}", True, (255, 255, 255))
        highscore_text = font.render(f"High skóre: {highscore}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(highscore_text, (10, 50))
                
        pygame.display.flip()
        clock.tick(60)
        dt = clock.get_time() / 1000

if __name__ == "__main__":
    main()