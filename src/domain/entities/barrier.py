"""
Barrier obstacle - must jump over.

High vertical obstacle that blocks ninja path.
"""
import pygame
from .obstacle import Obstacle
from ..interfaces.i_game_entity import IGameEntity


class Barrier(Obstacle):
    """
    High barrier obstacle.

    Ninja must jump to clear this obstacle.
    """

    WIDTH = 56
    HEIGHT = 100

    def __init__(self, x: float, y: float, scroll_speed: float) -> None:
        """
        Initialize barrier at position.

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
            other: Entity that collided
        """
        # Collision handled by game systems
        pass

    def get_sprite(self) -> pygame.Surface:
        """Get barrier sprite."""
        from ...infrastructure.rendering.sprite_placeholder import PlaceholderSprites
        return PlaceholderSprites.create_obstacle_barrier()
