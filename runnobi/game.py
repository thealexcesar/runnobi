"""Main game class for Runnobi."""

import pygame
import random
from runnobi.constants import *
from runnobi.player import Player
from runnobi.entities import Obstacle, Enemy, Coin


class Game:
    """Main game controller."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Runnobi - Ninja Endless Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
    
    def reset_game(self):
        """Reset game to initial state."""
        self.player = Player()
        self.obstacles = []
        self.enemies = []
        self.coins = []
        self.game_speed = INITIAL_GAME_SPEED
        self.distance = 0
        self.frames = 0
        self.game_over = False
        self.paused = False
        
        # Spawn initial obstacles
        next_x = SCREEN_WIDTH
        for _ in range(3):
            self.obstacles.append(Obstacle(next_x))
            next_x += random.randint(OBSTACLE_MIN_GAP, OBSTACLE_MAX_GAP)
    
    def handle_input(self):
        """Handle player input."""
        keys = pygame.key.get_pressed()
        
        if not self.game_over:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.jump()
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player.slide()
            if keys[pygame.K_z] or keys[pygame.K_j]:
                self.player.katana_slash()
            if keys[pygame.K_x] or keys[pygame.K_k]:
                self.player.throw_shuriken()
            if keys[pygame.K_c] or keys[pygame.K_LSHIFT]:
                self.player.shadow_dash()
    
    def update(self):
        """Update game state."""
        if self.game_over or self.paused:
            return
        
        self.frames += 1
        
        # Update player
        self.player.update()
        
        # Increase speed over time
        self.game_speed = min(
            MAX_GAME_SPEED,
            INITIAL_GAME_SPEED + (self.frames * SPEED_INCREMENT)
        )
        
        # Update distance/score
        self.distance += self.game_speed
        self.player.score = int(self.distance)
        
        # Update and spawn obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(self.game_speed)
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
        
        # Spawn new obstacles
        if len(self.obstacles) == 0 or self.obstacles[-1].x < SCREEN_WIDTH - OBSTACLE_MIN_GAP:
            next_x = SCREEN_WIDTH if len(self.obstacles) == 0 else self.obstacles[-1].x + random.randint(OBSTACLE_MIN_GAP, OBSTACLE_MAX_GAP)
            self.obstacles.append(Obstacle(next_x))
        
        # Update and spawn enemies
        for enemy in self.enemies[:]:
            enemy.update(self.game_speed)
            if enemy.is_off_screen() or enemy.destroyed:
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
        
        if random.random() < ENEMY_SPAWN_CHANCE:
            self.enemies.append(Enemy(SCREEN_WIDTH))
        
        # Update and spawn coins
        for coin in self.coins[:]:
            coin.update(self.game_speed)
            if coin.is_off_screen() or coin.collected:
                if coin in self.coins:
                    self.coins.remove(coin)
        
        if random.random() < COIN_SPAWN_CHANCE:
            self.coins.append(Coin(SCREEN_WIDTH))
        
        # Collision detection
        self.check_collisions()
    
    def check_collisions(self):
        """Check for collisions between entities."""
        player_rect = self.player.get_rect()
        
        # Check obstacle collisions (only if not invincible from shadow dash)
        if not self.player.shadow_dash_invincible:
            for obstacle in self.obstacles:
                if player_rect.colliderect(obstacle.get_rect()):
                    self.game_over = True
        
        # Check enemy collisions
        if not self.player.shadow_dash_invincible:
            for enemy in self.enemies:
                if not enemy.destroyed and player_rect.colliderect(enemy.get_rect()):
                    self.game_over = True
        
        # Check katana vs enemies
        katana_rect = self.player.get_katana_rect()
        if katana_rect:
            for enemy in self.enemies:
                if not enemy.destroyed and katana_rect.colliderect(enemy.get_rect()):
                    enemy.destroyed = True
                    self.player.score += 50
        
        # Check shuriken vs enemies
        for shuriken in self.player.shurikens[:]:
            shuriken_rect = pygame.Rect(shuriken['x'], shuriken['y'], 
                                        shuriken['size'], shuriken['size'])
            for enemy in self.enemies:
                if not enemy.destroyed and shuriken_rect.colliderect(enemy.get_rect()):
                    enemy.destroyed = True
                    self.player.score += 50
                    if shuriken in self.player.shurikens:
                        self.player.shurikens.remove(shuriken)
                    break
        
        # Check coin collection
        for coin in self.coins:
            if not coin.collected and player_rect.colliderect(coin.get_rect()):
                coin.collected = True
                self.player.coins += 1
                self.player.score += COIN_VALUE
    
    def draw(self):
        """Draw all game elements."""
        # Background
        self.screen.fill((135, 206, 235))  # Sky blue
        
        # Ground
        pygame.draw.rect(self.screen, (101, 67, 33), 
                        (0, GROUND_Y + PLAYER_HEIGHT, SCREEN_WIDTH, 
                         SCREEN_HEIGHT - GROUND_Y - PLAYER_HEIGHT))
        
        # Ground line
        pygame.draw.line(self.screen, BLACK, 
                        (0, GROUND_Y + PLAYER_HEIGHT),
                        (SCREEN_WIDTH, GROUND_Y + PLAYER_HEIGHT), 3)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw coins
        for coin in self.coins:
            coin.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw HUD
        self.draw_hud()
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_hud(self):
        """Draw heads-up display."""
        # Score
        score_text = self.font.render(f"Score: {self.player.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Coins
        coins_text = self.font.render(f"Coins: {self.player.coins}", True, YELLOW)
        self.screen.blit(coins_text, (10, 50))
        
        # Time survived
        time_seconds = self.frames // FPS
        time_text = self.font.render(f"Time: {time_seconds}s", True, BLACK)
        self.screen.blit(time_text, (10, 90))
        
        # Speed
        speed_text = self.small_font.render(f"Speed: {self.game_speed:.1f}", True, BLACK)
        self.screen.blit(speed_text, (10, 130))
        
        # Cooldown indicators on the right side
        x_pos = SCREEN_WIDTH - 200
        
        # Katana cooldown
        if self.player.katana_cooldown_timer > 0:
            cooldown_text = self.small_font.render("Katana: Cooldown", True, RED)
        else:
            cooldown_text = self.small_font.render("Katana: Ready (Z)", True, GREEN)
        self.screen.blit(cooldown_text, (x_pos, 10))
        
        # Shuriken cooldown
        if self.player.shuriken_cooldown_timer > 0:
            cooldown_text = self.small_font.render("Shuriken: Cooldown", True, RED)
        else:
            cooldown_text = self.small_font.render("Shuriken: Ready (X)", True, GREEN)
        self.screen.blit(cooldown_text, (x_pos, 40))
        
        # Shadow dash cooldown
        if self.player.shadow_dash_cooldown_timer > 0:
            secs_left = self.player.shadow_dash_cooldown_timer // FPS
            cooldown_text = self.small_font.render(f"Shadow Dash: {secs_left}s", True, RED)
        else:
            cooldown_text = self.small_font.render("Shadow Dash: Ready (C)", True, GREEN)
        self.screen.blit(cooldown_text, (x_pos, 70))
        
        # Controls reminder at bottom
        controls = [
            "Jump: SPACE/UP/W",
            "Slide: DOWN/S",
            "Katana: Z/J",
            "Shuriken: X/K",
            "Shadow Dash: C/SHIFT"
        ]
        y_offset = SCREEN_HEIGHT - 150
        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, DARK_GRAY)
            self.screen.blit(text, (SCREEN_WIDTH - 220, y_offset + i * 25))
    
    def draw_game_over(self):
        """Draw game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, text_rect)
        
        # Final score
        score_text = self.font.render(f"Final Score: {self.player.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(score_text, score_rect)
        
        # Coins collected
        coins_text = self.font.render(f"Coins: {self.player.coins}", True, YELLOW)
        coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(coins_text, coins_rect)
        
        # Time survived
        time_seconds = self.frames // FPS
        time_text = self.font.render(f"Survived: {time_seconds} seconds", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(time_text, time_rect)
        
        # Restart instruction
        restart_text = self.small_font.render("Press R to restart or ESC to quit", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
            
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
