import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from bullet import Shot
from utils import get_high_score, update_high_score

def main():
    print("Starting Asteroids!")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.font.init()
    font = pygame.font.SysFont(FONT, TEXT_SIZE)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, drawable, updatable)
    AsteroidField.containers = (updatable) # Assuming AsteroidField itself is updatable but not drawable
    Shot.containers = (shots, drawable, updatable)

    player_1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()

    clock = pygame.time.Clock()
    dt = 0
    current_score = 0
    high_score = get_high_score()
    game_over = False
    running = True 
    
    while running:
        # Allow game to exit gracefully
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_q or event.key == pygame.K_ESCAPE) and game_over:
                    running = False

        # --- Game Logic (only if not game_over) ---
        if not game_over:
            # Draw the background and all foreground object
            screen.fill("black")
            for obj in drawable:
                obj.draw(screen)

            # Move the game clock and update all updatable objects
            dt = clock.tick(FPS) / MS_TO_S
            updatable.update(dt)

            # Check for collisions
            for asteroid_obj in asteroids:
                if asteroid_obj.check_collisions(player_1):
                    game_over = True
                    break

                for shot in list(shots):
                    if asteroid_obj.check_collisions(shot):
                        current_score += asteroid_obj.get_score()
                        asteroid_obj.split()
                        shot.kill()
                        break                

            score_surface = font.render(f"SCORE: {current_score}", True, "orange")
            screen.blit(score_surface, (SCORE_POS_X, SCORE_POS_Y))
            
            high_score = max(high_score, current_score)
            high_score_surface = font.render(f"HIGH SCORE: {high_score}", True, "blue")
            screen.blit(high_score_surface, (SCORE_POS_X, SCORE_POS_Y - 50))

        # --- Game Over Display (always check, but only draw if game_over) ---
        else:
            end_surface = font.render("GAME OVER !!!", True, "red")
            
            # Calculate position to center the text
            end_rect = end_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(end_surface, end_rect)

            # Optional: Add instruction to quit
            instruction_surface = font.render("Press 'Q' or 'ESC' to quit", True, "white")
            instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(instruction_surface, instruction_rect)

        # Render the screen (this happens every frame, whether game is playing or over)
        pygame.display.flip()

    pygame.quit() # <--- Quit pygame cleanly
    update_high_score(high_score)
    print("Game Finished!")


if __name__ == "__main__":
    main()