import pygame
import os
from objects.circleshape import CircleShape
from objects.bullet import Shot
from utils.constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180
        self.shoot_cooldown = 0
        self.original_image = pygame.image.load(os.path.join("images/player.png")).convert_alpha()
        self.image = self.original_image.copy()
        self.life_active_image = pygame.image.load(os.path.join("images/life_active.png")).convert_alpha()
        self.radius = PLAYER_RADIUS
        self.lives = PLAYER_LIVES
    
    def draw(self, screen):
        self.image = pygame.transform.rotate(self.original_image, -self.rotation)
        self.rect = self.image.get_rect(center=self.position)
        screen.blit(self.image, self.rect)
        
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        self.rotation %= 360
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)    
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)
            
        if keys[pygame.K_SPACE] or keys[pygame.K_z]:
            if not self.shoot_cooldown > 0:
                self.shoot()
                self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        
        self.shoot_cooldown -= dt
            
    def shoot(self):        
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = shot.velocity.rotate(self.rotation)
        