"""
Game manager - central coordinator using Mediator pattern.

Coordinates all game systems and manages game loop.
"""
import pygame
import random
from typing import List

from src.domain.entities.ninja import Ninja
from src.domain.entities.obstacle import Obstacle
from src.domain.entities.collectible import Collectible
from src.domain.entities.coin import Coin
from src.factories.obstacle_factory import ObstacleFactory
from src.factories.collectible_factory import CollectibleFactory
from src.application.physics_engine import PhysicsEngine
from src.application.collision_detector import CollisionDetector
from src.application.physics_constants import BASE_SCROLL_SPEED, SPEED_INCREASE_RATE
from src.infrastructure.input.keyboard_adapter import KeyboardAdapter
from src.infrastructure.input.input_actions import InputAction
from src.application.game_state import GameState


class GameManager:
    """
    Central game coordinator using Mediator pattern.

    Manages game loop, systems integration, and game state.
    Coordinates: Physics, Collision, Input, Rendering, Spawning.
    """

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    GROUND_Y = 600
    TARGET_FPS = 60

    def __init__(self):
        """Initialize game systems and entities."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("🥷 RUNNOBI - Ninja Endless Runner")
        self.clock = pygame.time.Clock()
        self.running = True

        self.physics = PhysicsEngine(self.GROUND_Y)
        self.collision = CollisionDetector()
        self.input = KeyboardAdapter()

        self.ninja = Ninja(
            start_x=200,
            start_y=self.GROUND_Y - Ninja.HEIGHT,
            ground_y=self.GROUND_Y
        )
        self.obstacles: List[Obstacle] = []
        self.collectibles: List[Collectible] = []

        self.scroll_speed = BASE_SCROLL_SPEED
        self.distance_traveled = 0.0
        self.spawn_timer = 0.0
        self.spawn_interval = 2.0

        self.state = GameState.PLAYING

        self.font = pygame.font.Font(None, 36)

    def run(self) -> None:
        """Main game loop - 60 FPS with delta time."""
        while self.running:
            delta_time = self.clock.tick(self.TARGET_FPS) / 1000.0

            self._handle_events()

            if self.state == GameState.PLAYING:
                self._update_playing(delta_time)
            elif self.state == GameState.PAUSED:
                self._update_paused()
            elif self.state == GameState.GAME_OVER:
                self._update_game_over()

            self._render()

        pygame.quit()

    def _handle_events(self) -> None:
        """Handle pygame events and input."""
        for event in pygame.event.get():
            self.input.handle_event(event)

        self.input.update()

        if self.input.is_action_just_pressed(InputAction.QUIT):
            self.running = False

        if self.input.is_action_just_pressed(InputAction.PAUSE):
            if self.state == GameState.PLAYING:
                self.state = GameState.PAUSED
            elif self.state == GameState.PAUSED:
                self.state = GameState.PLAYING

    def _update_playing(self, delta_time: float) -> None:
        """Update game during PLAYING state."""
        self._handle_ninja_input()

        self.physics.update(self.ninja, delta_time)
        self.ninja.update(delta_time)

        for obstacle in self.obstacles[:]:
            obstacle.update(delta_time)
            if not obstacle.is_active():
                self.obstacles.remove(obstacle)

        for collectible in self.collectibles[:]:
            collectible.update(delta_time)
            if not collectible.is_active():
                self.collectibles.remove(collectible)

        self._check_collisions()
        self._update_spawning(delta_time)

        self.scroll_speed += SPEED_INCREASE_RATE * delta_time
        self.distance_traveled += self.scroll_speed * delta_time

        if not self.ninja.is_active():
            self.state = GameState.GAME_OVER

    def _update_paused(self) -> None:
        """Update during PAUSED state."""
        pass

    def _update_game_over(self) -> None:
        """Update during GAME_OVER state."""
        if self.input.is_action_just_pressed(InputAction.JUMP):
            self._restart_game()

    def _handle_ninja_input(self) -> None:
        """Handle player input for ninja actions."""
        if self.input.is_action_just_pressed(InputAction.JUMP):
            self.ninja.jump()

        if self.input.is_action_pressed(InputAction.SLIDE):
            self.ninja.start_slide()
        else:
            self.ninja.stop_slide()

        if self.input.is_action_just_pressed(InputAction.DASH):
            self.ninja.start_dash()

        if self.input.is_action_just_pressed(InputAction.ATTACK):
            self.ninja.start_attack()

    def _check_collisions(self) -> None:
        """Check all collisions and handle responses."""
        hit_obstacles = self.collision.check_ninja_obstacles(self.ninja, self.obstacles)
        for obstacle in hit_obstacles:
            if not self.ninja.is_invincible():
                self.ninja.kill()

        collected = self.collision.check_ninja_collectibles(self.ninja, self.collectibles)
        for collectible in collected:
            if isinstance(collectible, Coin):
                self.ninja.add_score(collectible.get_points())
            collectible.collect()

    def _update_spawning(self, delta_time: float) -> None:
        """Spawn new obstacles and collectibles."""
        self.spawn_timer += delta_time

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0.0

            if random.random() < 0.8:
                obstacle_type = random.choice(['spike', 'barrier', 'low_barrier', 'crate'])
                obstacle = ObstacleFactory.create(
                    obstacle_type,
                    self.SCREEN_WIDTH + 50,
                    self.GROUND_Y,
                    self.scroll_speed
                )
                self.obstacles.append(obstacle)

            if random.random() < 0.5:
                coin = CollectibleFactory.create(
                    'coin',
                    self.SCREEN_WIDTH + 50,
                    self.GROUND_Y - 150,
                    self.scroll_speed
                )
                self.collectibles.append(coin)

    def _render(self) -> None:
        """Render everything to screen."""
        self.screen.fill((135, 206, 235))

        pygame.draw.rect(
            self.screen,
            (139, 69, 19),
            (0, self.GROUND_Y, self.SCREEN_WIDTH, self.SCREEN_HEIGHT - self.GROUND_Y)
        )

        for obstacle in self.obstacles:
            if obstacle.is_active():
                sprite = obstacle.get_sprite()
                pos = obstacle.get_render_position()
                self.screen.blit(sprite, pos.as_tuple())

        for collectible in self.collectibles:
            if collectible.is_active():
                sprite = collectible.get_sprite()
                pos = collectible.get_render_position()
                self.screen.blit(sprite, pos.as_tuple())

        if self.ninja.is_active():
            sprite = self.ninja.get_sprite()
            pos = self.ninja.get_render_position()
            self.screen.blit(sprite, pos.as_tuple())

        self._render_hud()

        if self.state == GameState.PAUSED:
            self._render_pause_overlay()
        elif self.state == GameState.GAME_OVER:
            self._render_game_over_overlay()

        pygame.display.flip()

    def _render_hud(self) -> None:
        """Render HUD (score, distance)."""
        score_text = self.font.render(
            f"Score: {self.ninja.get_score()}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(score_text, (10, 10))

        distance_text = self.font.render(
            f"Distance: {int(self.distance_traveled)}m",
            True,
            (255, 255, 255)
        )
        self.screen.blit(distance_text, (10, 50))

    def _render_pause_overlay(self) -> None:
        """Render pause screen overlay."""
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        pause_text = self.font.render(
            "PAUSED - Press ESC to resume",
            True,
            (255, 255, 255)
        )
        text_rect = pause_text.get_rect(
            center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
        )
        self.screen.blit(pause_text, text_rect)

    def _render_game_over_overlay(self) -> None:
        """Render game over screen."""
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(
            center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50)
        )
        self.screen.blit(game_over_text, text_rect)

        score_text = self.font.render(
            f"Final Score: {self.ninja.get_score()}",
            True,
            (255, 255, 255)
        )
        score_rect = score_text.get_rect(
            center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
        )
        self.screen.blit(score_text, score_rect)

        restart_text = self.font.render(
            "Press SPACE to restart",
            True,
            (255, 255, 255)
        )
        restart_rect = restart_text.get_rect(
            center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50)
        )
        self.screen.blit(restart_text, restart_rect)

    def _restart_game(self) -> None:
        """Restart game from beginning."""
        self.ninja = Ninja(
            start_x=200,
            start_y=self.GROUND_Y - Ninja.HEIGHT,
            ground_y=self.GROUND_Y
        )
        self.obstacles.clear()
        self.collectibles.clear()
        self.scroll_speed = BASE_SCROLL_SPEED
        self.distance_traveled = 0.0
        self.spawn_timer = 0.0
        self.state = GameState.PLAYING
