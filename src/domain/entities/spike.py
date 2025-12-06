"""
Spike obstacle - instant death on contact.

Sharp obstacle that kills ninja immediately on collision.
"""
import pygame
from .obstacle import Obstacle
from ..interfaces.i_game_entity import IGameEntity


class Spike(Obstacle):
    """
    Spike obstacle that kills ninja on contact.

    Cannot be destroyed or avoided except by jumping over.
    """

    WIDTH = 40
    HEIGHT = 50

    def __init__(self, x: float, y: float, scroll_speed: float) -> None:
        """
        Initialize spike at position.

        Args:
            x: X position
            y: Y position (ground level - HEIGHT)
            scroll_speed: World scroll speed
        """
        super().__init__(x, y, self.WIDTH, self.HEIGHT, scroll_speed)

    def on_collision(self, other: IGameEntity) -> None:
        """
        Kill ninja on collision.

        Args:
            other: Entity that collided (should be ninja)
        """
        # Collision handling done by game systems
        # Spike stays active after collision
        pass

    def get_sprite(self) -> pygame.Surface:
        """Get spike sprite."""
        from ...infrastructure.rendering.sprite_placeholder import PlaceholderSprites
        return PlaceholderSprites.create_obstacle_spike()
