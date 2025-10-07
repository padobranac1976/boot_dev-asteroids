import pygame
from constants import *
from player import Player

def main():
    print("Starting Asteroids!")   
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player_1 =  Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    clock = pygame.time.Clock()
    dt = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        player_1.draw(screen)
        pygame.display.flip()
        dt = clock.tick(FPS) / MS_TO_S
        
if __name__ == "__main__":
    main()
