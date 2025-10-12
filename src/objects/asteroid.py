import pygame
import random

from objects.circleshape import CircleShape
from utils.constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(surface=screen, color="white", center=self.position, radius=self.radius, width=2)
        
    def update(self, dt):
        self.position += self.velocity * dt        
        
    def split(self):
        self.kill()
        if self.radius == ASTEROID_MIN_RADIUS:
            return
        
        new_angle = random.uniform(NEW_ASTEROID_ANGLE_MIN, NEW_ASTEROID_ANGLE_MAX)
        new_asteroid_1 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
        new_asteroid_1.velocity = self.velocity.rotate(new_angle) * NEW_ASTEROID_VELOCITY_FACTOR
        
        new_asteroid_2 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
        new_asteroid_2.velocity = self.velocity.rotate(-new_angle) * NEW_ASTEROID_VELOCITY_FACTOR
    def get_score(self):
        if self.radius == ASTEROID_MIN_RADIUS:
            return SCORE_SMALL
        elif self.radius == 2 * ASTEROID_MIN_RADIUS:
            return SCORE_MEDIUM
        else:
            return SCORE_LARGE
    