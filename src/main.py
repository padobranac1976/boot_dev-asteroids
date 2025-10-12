import pygame
from utils.utils import update_high_score
from utils.gamestatus import GameStatus

def main():
    print("Starting Asteroids!")
    game_status = GameStatus() 
    
    while game_status.running:
        game_status.check_exit_conditions()

        # --- Game Logic (only if not game_over) ---
        if not game_status.game_over:
            game_status.draw()
            game_status.update()
            game_status.check_collisions()
            game_status.render_high_score()
            game_status.render_current_lives()

        # --- Game Over Display (always check, but only draw if game_over) ---
        else:
            game_status.render_game_over_screen()

        # Render the screen (this happens every frame, whether game is playing or over)
        pygame.display.flip()

    pygame.quit() # <--- Quit pygame cleanly
    update_high_score(game_status.current_score)
    print("Game Finished!")


if __name__ == "__main__":
    main()