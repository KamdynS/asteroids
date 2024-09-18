import pygame
import random
from enemy import GreenEnemy, BlackEnemy, RedEnemy, BlueEnemy
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.red_enemy_timer = 0.0
        self.red_enemy_active = False
        self.green_enemy_count = 0
        self.blue_enemy_count = 0

    def spawn(self, enemy_class, radius, position, velocity=None):
        enemy = enemy_class(position.x, position.y, radius)
        if velocity:
            enemy.velocity = velocity
        return enemy

    def update(self, dt, player_pos):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            edge = random.choice(self.edges)
            position = edge[1](random.uniform(0, 1))
            
            available_enemies = [BlackEnemy]
            weights = [0.6]

            if self.green_enemy_count < MAX_GREEN_ENEMIES:
                available_enemies.append(GreenEnemy)
                weights.append(0.2)
            
            if self.blue_enemy_count < MAX_BLUE_ENEMIES:
                available_enemies.append(BlueEnemy)
                weights.append(0.2)

            enemy_type = random.choices(available_enemies, weights=weights)[0]
            radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
            
            new_enemy = None
            if enemy_type == BlackEnemy:
                velocity = edge[0] * ASTEROID_SPEED
                velocity = velocity.rotate(random.randint(-30, 30))
                new_enemy = self.spawn(enemy_type, radius, position, velocity)
            else:
                new_enemy = self.spawn(enemy_type, radius, position)

            if new_enemy:
                if isinstance(new_enemy, GreenEnemy):
                    self.green_enemy_count += 1
                    print(f"Green enemy spawned. Total: {self.green_enemy_count}")
                elif isinstance(new_enemy, BlueEnemy):
                    self.blue_enemy_count += 1
                    print(f"Blue enemy spawned. Total: {self.blue_enemy_count}")
                return new_enemy

        if not self.red_enemy_active:
            self.red_enemy_timer += dt
            if self.red_enemy_timer >= RED_ENEMY_COOLDOWN:
                self.red_enemy_timer = 0
                self.red_enemy_active = True
                edge = random.choice(self.edges)
                position = edge[1](random.uniform(0, 1))
                red_enemy = RedEnemy(position.x, position.y, ASTEROID_MAX_RADIUS)
                print("Red enemy (boss) spawned!")
                return red_enemy

        return None

    def enemy_destroyed(self, enemy):
        if isinstance(enemy, GreenEnemy):
            self.green_enemy_count -= 1
            print(f"Green enemy destroyed. Remaining: {self.green_enemy_count}")
        elif isinstance(enemy, BlueEnemy):
            self.blue_enemy_count -= 1
            print(f"Blue enemy destroyed. Remaining: {self.blue_enemy_count}")
        elif isinstance(enemy, RedEnemy):
            self.red_enemy_active = False
            print("Red enemy (boss) destroyed!")
        elif isinstance(enemy, BlackEnemy):
            print("Black enemy destroyed.")
