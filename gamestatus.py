import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from bullet import Shot
from utils import get_high_score

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