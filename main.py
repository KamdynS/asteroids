from constants import *
import pygame
from player import Player
from enemy import RedEnemy, GreenEnemy, BlueEnemy, BlackEnemy
from asteroidfield import AsteroidField
from shot import Shot
import sys
import random
import pygame_gui

def game_loop(screen, clock, gui_manager):
    # Create groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set up containers
    Player.containers = (updatable, drawable)
    RedEnemy.containers = (enemies, updatable, drawable)
    GreenEnemy.containers = (enemies, updatable, drawable)
    BlueEnemy.containers = (enemies, updatable, drawable)
    BlackEnemy.containers = (enemies, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable,)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    font = pygame.font.Font(None, 36)
    boss_warning_timer = 0
    boss_warning_duration = 2
    red_enemy = None
    score = 0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # Signal to quit the game
            gui_manager.process_events(event)

        gui_manager.update(dt)

        # Update all updatable objects
        for obj in updatable:
            if isinstance(obj, (RedEnemy, GreenEnemy, BlueEnemy)):
                obj.update(dt, player.position)
            elif isinstance(obj, BlackEnemy):
                obj.update(dt)
            elif isinstance(obj, Player):
                result = obj.update(dt)
                if result:
                    shots.add(result)
            elif isinstance(obj, AsteroidField):
                new_enemy = obj.update(dt, player.position)
                if new_enemy:
                    if isinstance(new_enemy, RedEnemy):
                        boss_warning_timer = boss_warning_duration
                        red_enemy = new_enemy
                    enemies.add(new_enemy)
                    updatable.add(new_enemy)
                    drawable.add(new_enemy)
            else:
                obj.update(dt)

        # Check for collisions
        for enemy in enemies:
            if player.collides_with(enemy):
                return score  # Return score when game over

            for shot in shots:
                if enemy.collides_with(shot):
                    if enemy.take_damage():
                        if isinstance(enemy, RedEnemy):
                            score += enemy.health
                            new_enemies = enemy.split()
                            if new_enemies:
                                enemies.add(new_enemies)
                                updatable.add(new_enemies)
                                drawable.add(new_enemies)
                            else:
                                asteroid_field.enemy_destroyed(enemy)
                                red_enemy = None
                                enemy.kill()
                        elif isinstance(enemy, (GreenEnemy, BlueEnemy)):
                            score += 2
                            asteroid_field.enemy_destroyed(enemy)
                            enemy.kill()
                        else:
                            score += 1
                            asteroid_field.enemy_destroyed(enemy)
                            enemy.kill()
                    shot.kill()
                    break

        screen.fill("black")

        # Draw all drawable objects
        for obj in drawable:
            obj.draw(screen)

        # Draw boss warning
        if boss_warning_timer > 0:
            boss_warning_timer -= dt
            warning_text = font.render("Boss incoming", True, (255, 0, 0))
            text_rect = warning_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(warning_text, text_rect)

        # Draw boss health bar
        if red_enemy:
            health_width = SCREEN_WIDTH * 0.8
            health_height = 20
            health_x = (SCREEN_WIDTH - health_width) / 2
            health_y = 20
            health_outline = pygame.Rect(health_x, health_y, health_width, health_height)
            max_health = 2 ** RedEnemy.spawn_count
            health_fill = pygame.Rect(health_x, health_y, health_width * (red_enemy.health / max_health), health_height)
            pygame.draw.rect(screen, (255, 0, 0), health_fill)
            pygame.draw.rect(screen, (255, 255, 255), health_outline, 2)

        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(score_text, score_rect)

        gui_manager.draw_ui(screen)
        pygame.display.flip()

    return score

def main_menu(screen, clock, gui_manager):
    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 25), (200, 50)),
        text='Start Game',
        manager=gui_manager
    )
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 35), (200, 50)),
        text='Quit',
        manager=gui_manager
    )

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    start_button.kill()
                    quit_button.kill()
                    return True
                if event.ui_element == quit_button:
                    return False

            gui_manager.process_events(event)

        gui_manager.update(time_delta)

        screen.fill("black")
        gui_manager.draw_ui(screen)

        pygame.display.flip()

def game_over_menu(screen, clock, gui_manager, score):
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))

    restart_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2), (200, 50)),
        text='Restart',
        manager=gui_manager
    )
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 60), (200, 50)),
        text='Quit',
        manager=gui_manager
    )

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == restart_button:
                    return True
                if event.ui_element == quit_button:
                    return False

            gui_manager.process_events(event)

        gui_manager.update(time_delta)

        screen.fill("black")
        screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100)))
        screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)))
        gui_manager.draw_ui(screen)

        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    gui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    while running:
        if main_menu(screen, clock, gui_manager):
            while True:
                gui_manager.clear_and_reset()  # Clear all UI elements before starting the game
                score = game_loop(screen, clock, gui_manager)
                if score is None:
                    running = False
                    break
                else:
                    gui_manager.clear_and_reset()  # Clear all UI elements before showing game over menu
                    if not game_over_menu(screen, clock, gui_manager, score):
                        running = False
                        break
                    # If game_over_menu returns True, we continue the loop and start a new game
        else:
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()