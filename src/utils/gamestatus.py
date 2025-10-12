import pygame
from utils.constants import *
from objects.player import Player
from objects.asteroid import Asteroid
from objects.asteroidfield import AsteroidField
from objects.bullet import Shot
from utils.utils import get_high_score

class GameStatus():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.font.init()
        self.font = pygame.font.SysFont(FONT, TEXT_SIZE)

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
        
    def check_exit_conditions(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_q or event.key == pygame.K_ESCAPE) and self.game_over:
                    self.running = False
    
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

        # Optional: Add instruction to quit
        instruction_surface = self.font.render("Press 'Q' or 'ESC' to quit", True, "white")
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + VISU_OFFSET))
        self.screen.blit(instruction_surface, instruction_rect)