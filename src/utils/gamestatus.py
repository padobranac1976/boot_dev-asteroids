import pygame
from utils.constants import *
from objects.player import Player
from objects.asteroid import Asteroid
from objects.asteroidfield import AsteroidField
from objects.bullet import Shot
from utils.utils import get_high_score
from utils.utils import update_high_score

class GameStatus():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.font.init()
        self.font = pygame.font.SysFont(FONT, TEXT_SIZE)
        self.reset()        
    
    def reset(self):        
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()

        Player.containers = (self.updatable, self.drawable)
        Asteroid.containers = (self.asteroids, self.drawable, self.updatable)
        AsteroidField.containers = (self.updatable)
        Shot.containers = (self.shots, self.drawable, self.updatable)

        self.player_1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        AsteroidField()

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.current_score = 0
        self.high_score = get_high_score()
        self.game_over = False
        self.running = True
        self.pause = False
        
    def check_exit_conditions(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_q:
                        self.running = False
                    if event.key == pygame.K_p:
                        update_high_score(self.current_score)
                        self.reset()
                        self.game_over = False                
                else:
                    if event.key == pygame.K_ESCAPE:
                        self.pause = True
                    if self.pause:
                        if event.key == pygame.K_q:
                            self.running = False
                        if event.key == pygame.K_c:
                            self.pause = False
    
    def draw(self):
        # Draw the background and all foreground object
        self.screen.fill("black")
        for obj in self.drawable:
            obj.draw(self.screen)
            
    def update(self):
        dt = self.clock.tick(FPS) / MS_TO_S
        self.updatable.update(dt)
        
    def check_collisions(self):
        for asteroid_obj in self.asteroids:
            if asteroid_obj.check_collisions(self.player_1):
                asteroid_obj.kill()
                self.player_1.lives -= 1
                if self.player_1.lives == 0:
                    self.game_over = True                
                    break

            for shot in list(self.shots):
                if asteroid_obj.check_collisions(shot):
                    self.current_score += asteroid_obj.get_score()
                    asteroid_obj.split()
                    shot.kill()
                    break
                
    def render_high_score(self):
        score_surface = self.font.render(f"SCORE: {self.current_score}", True, "orange")
        self.screen.blit(score_surface, (SCORE_POS_X, SCORE_POS_Y))
        
        self.high_score = max(self.high_score, self.current_score)
        high_score_surface = self.font.render(f"HIGH SCORE: {self.high_score}", True, "blue")
        self.screen.blit(high_score_surface, (SCORE_POS_X, SCORE_POS_Y - VISU_OFFSET))
    
    def render_current_lives(self):        
        for factor in range(self.player_1.lives):
            self.screen.blit(self.player_1.life_active_image, (SCORE_POS_X + factor * PLAYER_LIFE_OFFSET, SCORE_POS_Y + VISU_OFFSET))
        
    def render_game_over_screen(self):
        end_surface = self.font.render("GAME OVER !!!", True, "red")
                
        # Calculate position to center the text
        end_rect = end_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(end_surface, end_rect)

        # Add instruction to quit
        quit_surface = self.font.render("Press 'Q' to quit", True, "white")
        quit_rect = quit_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + VISU_OFFSET))
        self.screen.blit(quit_surface, quit_rect)
        
        # Add instruction to start again
        start_surface = self.font.render("Press 'P' to start again", True, "white")
        start_rect = start_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 2 * VISU_OFFSET))
        self.screen.blit(start_surface, start_rect)
        
    def render_game_paused(self):
        pause_surface = self.font.render("PAUSE", True, "white")
                
        # Calculate position to center the text
        pause_rect = pause_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_surface, pause_rect)

        # Add instruction to quit
        quit_surface = self.font.render("Press 'Q' to quit", True, "white")
        quit_rect = quit_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + VISU_OFFSET))
        self.screen.blit(quit_surface, quit_rect)
        
        # Add instruction to start again
        continue_surface = self.font.render("Press 'C' to continue", True, "white")
        continue_rect = continue_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 2 * VISU_OFFSET))
        self.screen.blit(continue_surface, continue_rect)
        