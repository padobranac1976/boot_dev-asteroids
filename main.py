import pygame
from constants import FPS, MS_TO_S
from utils import update_high_score, render_game_over_screen, render_high_score_surface, check_exit_conditions
from gamestatus import GameStatus

def main():
    print("Starting Asteroids!")
    game_status = GameStatus() 
    
    while game_status.running:
        game_status.running = check_exit_conditions(game_status.running, game_status.game_over)

        # --- Game Logic (only if not game_over) ---
        if not game_status.game_over:
            # Draw the background and all foreground object
            game_status.screen.fill("black")
            for obj in game_status.drawable:
                obj.draw(game_status.screen)

            # Move the game clock and update all updatable objects
            dt = game_status.clock.tick(FPS) / MS_TO_S
            game_status.updatable.update(dt)

            # Check for collisions
            for asteroid_obj in game_status.asteroids:
                if asteroid_obj.check_collisions(game_status.player_1):
                    game_status.game_over = True
                    break

                for shot in list(game_status.shots):
                    if asteroid_obj.check_collisions(shot):
                        game_status.current_score += asteroid_obj.get_score()
                        asteroid_obj.split()
                        shot.kill()
                        break                

            render_high_score_surface(game_status.screen, game_status.font, game_status.current_score, game_status.high_score)           

        # --- Game Over Display (always check, but only draw if game_over) ---
        else:
            render_game_over_screen(game_status.screen, game_status.font)            

        # Render the screen (this happens every frame, whether game is playing or over)
        pygame.display.flip()

    pygame.quit() # <--- Quit pygame cleanly
    update_high_score(game_status.current_score)
    print("Game Finished!")


if __name__ == "__main__":
    main()