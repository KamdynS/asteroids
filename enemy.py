import pygame
from asteroid import Asteroid
from constants import *

import random

class Enemy(Asteroid):
    def __init__(self, x, y, radius, color, health=1):
        super().__init__(x, y, radius)
        self.color = color
        self.health = health

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, 2)

    def take_damage(self):
        self.health -= 1
        return self.health <= 0

    def update(self, dt, player_pos=None):
        super().update(dt)

class BlackEnemy(Enemy):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius, "white")  # Using white for visibility

    def update(self, dt, player_pos=None):
        super().update(dt)

class GreenEnemy(Enemy):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius, "green")

    def update(self, dt, player_pos):
        direction = (player_pos - self.position).normalize()
        self.velocity = direction * (ASTEROID_SPEED * 0.9)
        super().update(dt)

class RedEnemy(Enemy):
    spawn_count = 0

    def __init__(self, x, y, radius):
        RedEnemy.spawn_count += 1
        health = 2 ** RedEnemy.spawn_count
        super().__init__(x, y, radius, "red", health=health)
        # Give the boss a random initial velocity
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * (ASTEROID_SPEED * 0.75)

    def update(self, dt, player_pos):
        super().update(dt)
        
        # Bounce off the edges of the screen
        if self.position.x <= self.radius or self.position.x >= SCREEN_WIDTH - self.radius:
            self.velocity.x *= -1
        if self.position.y <= self.radius or self.position.y >= SCREEN_HEIGHT - self.radius:
            self.velocity.y *= -1

        # Slightly adjust velocity towards the player
        direction_to_player = (player_pos - self.position).normalize()
        self.velocity += direction_to_player * (ASTEROID_SPEED * 0.1 * dt)
        
        # Normalize velocity to maintain consistent speed
        self.velocity = self.velocity.normalize() * (ASTEROID_SPEED * 0.75)

        # Keep the boss on screen
        self.position.x = max(self.radius, min(self.position.x, SCREEN_WIDTH - self.radius))
        self.position.y = max(self.radius, min(self.position.y, SCREEN_HEIGHT - self.radius))

    def split(self):
        if self.health > 1:
            self.health //= 2
            self.radius = int(self.radius * 0.8)
            return [self]  # Return a list containing this enemy
        return []  # Return an empty list when the boss is destroyed

class BlueEnemy(Enemy):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius, "blue")

    def update(self, dt, player_pos):
        direction = (self.position - player_pos).normalize()
        self.velocity = direction * ASTEROID_SPEED
        super().update(dt)