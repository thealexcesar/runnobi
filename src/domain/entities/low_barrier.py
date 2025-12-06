"""
Low barrier obstacle - must slide under.

Low horizontal obstacle that ninja must slide under.
"""
import pygame
from .obstacle import Obstacle
from ..interfaces.i_game_entity import IGameEntity


class LowBarrier(Obstacle):
    """
    Low barrier obstacle.

    Ninja must slide to pass under this obstacle.
    """

    WIDTH = 56
    HEIGHT = 40

    def __init__(self, x: float, y: float, scroll_speed: float) -> None:
        """
        Initialize low barrier at position.

        Args:
            x: X position
            y: Y position (elevated above ground)
            scroll_speed: World scroll speed
        """
        super().__init__(x, y, self.WIDTH, self.HEIGHT, scroll_speed)

    def on_collision(self, other: IGameEntity) -> None:
        """
        Kill ninja on collision.

        Args:
            other: Entity that collided
        """
        # Collision handled by game systems
        pass

    def get_sprite(self) -> pygame.Surface:
        """Get low barrier sprite."""
        from ...infrastructure.rendering.sprite_placeholder import PlaceholderSprites
        return PlaceholderSprites.create_obstacle_low_barrier()
