from constants import *
import pygame
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import sys

def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # Create groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set up containers for Player class
    Player.containers = (updatable, drawable)

    # Set up containers for Asteroid class
    Asteroid.containers = (asteroids, updatable, drawable)

    # Set up containers for AsteroidField class
    AsteroidField.containers = (updatable,)

    # Set up containers for Shot class
    Shot.containers = (shots, updatable, drawable)

    # Create player (it will be automatically added to the groups)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Create AsteroidField
    asteroid_field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update all updatable objects
        for obj in updatable:
            result = obj.update(dt)
            if isinstance(obj, Player) and result:
                shots.add(result)

        # Check for collisions between player and asteroids
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                print("Game over!")
                pygame.quit()
                sys.exit()

        # Check for collisions between bullets and asteroids
        for asteroid in list(asteroids):  # Create a copy of the group to iterate over
            for shot in list(shots):  # Create a copy of the group to iterate over
                if asteroid.collides_with(shot):
                    asteroid.split()
                    shot.kill()
                    break  # Break the inner loop to avoid checking against a destroyed asteroid

        screen.fill("black")

        # Draw all drawable objects
        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()