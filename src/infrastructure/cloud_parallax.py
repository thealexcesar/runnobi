"""
Simple cloud parallax system for background movement.

Creates floating clouds that move at different speeds to simulate depth.
"""
import pygame
import random
from typing import List


class Cloud:
    """Single cloud entity with position and speed."""

    def __init__(self, x: float, y: float, speed: float, scale: float):
        """
        Initialize cloud.

        Args:
            x: Initial x position
            y: Y position (height)
            speed: Horizontal movement speed
            scale: Cloud size scale (0.5 to 1.5)
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.scale = scale

    def update(self, delta_time: float, scroll_speed: float) -> None:
        """
        Move cloud based on parallax speed.

        Args:
            delta_time: Time elapsed since last frame
            scroll_speed: Game scroll speed for parallax effect
        """
        # Move cloud left at fraction of game speed (parallax)
        self.x -= self.speed * scroll_speed * delta_time

    def is_off_screen(self, screen_width: int) -> bool:
        """Check if cloud has moved off-screen."""
        return self.x + 100 < 0

    def reset_position(self, screen_width: int) -> None:
        """Reset cloud to right side of screen."""
        self.x = screen_width + random.randint(50, 400)


class CloudParallax:
    """
    Parallax cloud system for background depth effect.

    Creates multiple layers of clouds moving at different speeds.
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize parallax system.

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clouds: List[Cloud] = []

        # Create initial clouds
        self._spawn_initial_clouds()

    def _spawn_initial_clouds(self) -> None:
        """Spawn initial set of clouds across screen."""
        num_clouds = 8

        for _ in range(num_clouds):
            x = random.randint(0, self.screen_width)
            y = random.randint(100, 300)
            speed = random.uniform(0.05, 0.15)
            scale = random.uniform(0.6, 1.2)

            self.clouds.append(Cloud(x, y, speed, scale))

    def update(self, delta_time: float, scroll_speed: float) -> None:
        """
        Update all clouds.

        Args:
            delta_time: Time elapsed since last frame
            scroll_speed: Game scroll speed
        """
        for cloud in self.clouds:
            cloud.update(delta_time, scroll_speed)

            # Respawn cloud if off-screen
            if cloud.is_off_screen(self.screen_width):
                cloud.reset_position(self.screen_width)
                cloud.y = random.randint(50, 250)
                cloud.speed = random.uniform(0.1, 0.3)
                cloud.scale = random.uniform(0.6, 1.2)

    def render(self, screen: pygame.Surface) -> None:
        """
        Render all clouds.

        Args:
            screen: Pygame surface to render on
        """
        for cloud in self.clouds:
            self._render_cloud(screen, cloud)

    def _render_cloud(self, screen: pygame.Surface, cloud: Cloud) -> None:
        """
        Render single cloud as simple ellipse.

        Args:
            screen: Pygame surface
            cloud: Cloud to render
        """
        # Simple cloud: 3 overlapping white ellipses
        base_width = int(80 * cloud.scale)
        base_height = int(30 * cloud.scale)

        # cloud_color = (100, 100, 100)
        cloud_color = (255, 255, 255)

        # Main cloud body
        pygame.draw.ellipse(
            screen,
            cloud_color,
            (int(cloud.x), int(cloud.y), base_width, base_height)
        )

        # Left puff
        pygame.draw.ellipse(
            screen,
            cloud_color,
            (int(cloud.x - base_width * 0.3), int(cloud.y + base_height * 0.2),
             int(base_width * 0.6), int(base_height * 0.8))
        )

        # Right puff
        pygame.draw.ellipse(
            screen,
            cloud_color,
            (int(cloud.x + base_width * 0.4), int(cloud.y + base_height * 0.2),
             int(base_width * 0.6), int(base_height * 0.8))
        )
