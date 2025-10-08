import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    print("Starting Asteroids!")   
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, drawable, updatable)
    AsteroidField.containers = (updatable)
    
    player_1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    
    clock = pygame.time.Clock()
    dt = 0
    
    while True:
        # Allow game to exit gracefully
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        # Draw the background and all foreground object
        screen.fill("black")
        for object in drawable:
            object.draw(screen)
        
        # Move the game clock and update all updatable objects 
        dt = clock.tick(FPS) / MS_TO_S
        updatable.update(dt)
        
        # Render the screen
        pygame.display.flip()
        
if __name__ == "__main__":
    main()
