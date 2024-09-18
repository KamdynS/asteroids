import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()  # Always destroy the current asteroid

        if self.radius <= ASTEROID_MIN_RADIUS:
            return  # Small asteroid, no splitting

        # Generate random angle for splitting
        random_angle = random.uniform(20, 50)

        # Create two new velocity vectors
        new_velocity1 = self.velocity.rotate(random_angle)
        new_velocity2 = self.velocity.rotate(-random_angle)

        # Calculate new radius
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Create two new asteroids
        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        # Set velocities for new asteroids (1.2 times faster)
        new_asteroid1.velocity = new_velocity1 * 1.2
        new_asteroid2.velocity = new_velocity2 * 1.2

        # Add new asteroids to the game
        if hasattr(self, 'containers'):
            for container in self.containers:
                container.add(new_asteroid1)
                container.add(new_asteroid2)

        return [new_asteroid1, new_asteroid2]
