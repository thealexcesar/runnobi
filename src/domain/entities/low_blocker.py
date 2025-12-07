"""
Low blocker obstacle - must slide under.

Solid block from ceiling leaving gap at bottom.
"""
import pygame

from domain.entities import Obstacle
from domain.interfaces import IGameEntity


class LowBlocker(Obstacle):
    """
    Ceiling blocker - solid block from top leaving gap at bottom.

    Ninja must crouch to pass under the gap.
    """

    WIDTH = 80
    HEIGHT = 525

    def __init__(self, x: float, ground_y: float, scroll_speed: float) -> None:
        """
        Initialize ceiling blocker.

        Args:
            x: X position
            ground_y: Ground level (600)
            scroll_speed: World scroll speed
        """
        # Start from top of screen (y=0)
        y = 0
        super().__init__(x, y, self.WIDTH, self.HEIGHT, scroll_speed)

    def on_collision(self, other: IGameEntity) -> None:
        """Kill ninja if hits (not crouching)."""
        pass

    def get_sprite(self) -> pygame.Surface:
        """Get ceiling blocker sprite."""
        from infrastructure.rendering.sprite_placeholder import PlaceholderSprites
        return PlaceholderSprites.create_low_blocker()
