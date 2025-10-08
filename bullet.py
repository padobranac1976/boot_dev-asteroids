import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(0, 1)  * PLAYER_SHOOT_SPEED
        
    def draw(self, screen):
        pygame.draw.circle(surface=screen, color="green", center=self.position, radius=self.radius, width=2)
        
    def update(self, dt):
        self.position += self.velocity * dt 