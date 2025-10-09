import os
import pygame
from constants import *

def update_high_score(new_score):
    high_score = get_high_score()
    high_score_dir = HIGH_SCORE_LOCATION.split("/")[0]
    if not os.path.exists(high_score_dir):
        os.mkdir(high_score_dir)
    with open(HIGH_SCORE_LOCATION, 'w') as f:
        f.write(str(max(high_score, new_score)))
            
def get_high_score():
    current_high_score = 0
    if os.path.exists(HIGH_SCORE_LOCATION):
        with open(HIGH_SCORE_LOCATION) as f:
            current_high_score = f.read()
    
    return int(current_high_score)

def render_game_over_screen(screen, font):
    end_surface = font.render("GAME OVER !!!", True, "red")
            
    # Calculate position to center the text
    end_rect = end_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(end_surface, end_rect)

    # Optional: Add instruction to quit
    instruction_surface = font.render("Press 'Q' or 'ESC' to quit", True, "white")
    instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(instruction_surface, instruction_rect)
    
def render_high_score_surface(screen, font, current_score, high_score):
    score_surface = font.render(f"SCORE: {current_score}", True, "orange")
    screen.blit(score_surface, (SCORE_POS_X, SCORE_POS_Y))
    
    high_score = max(high_score, current_score)
    high_score_surface = font.render(f"HIGH SCORE: {high_score}", True, "blue")
    screen.blit(high_score_surface, (SCORE_POS_X, SCORE_POS_Y - 50))

def check_exit_conditions(running, game_over):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_q or event.key == pygame.K_ESCAPE) and game_over:
                running = False
    return running