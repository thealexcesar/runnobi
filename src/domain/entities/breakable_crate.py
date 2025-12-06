"""
Breakable crate obstacle - can be destroyed by attack.

Crate that blocks path but can be destroyed with katana slash.
"""
import pygame
from .obstacle import Obstacle
from ..interfaces.i_game_entity import IGameEntity


class BreakableCrate(Obstacle):
    """
    Breakable crate obstacle.

    Can be destroyed by ninja's katana attack.
    """

    WIDTH = 56
    HEIGHT = 56

    def __init__(self, x: float, y: float, scroll_speed: float) -> None:
        """
        Initialize crate at position.

        Args:
            x: X position
            y: Y position (ground level - HEIGHT)
            scroll_speed: World scroll speed
        """
        super().__init__(x, y, self.WIDTH, self.HEIGHT, scroll_speed)
        self._destroyed = False

    def on_collision(self, other: IGameEntity) -> None:
        """
        Handle collision (can be destroyed by attack).

        Args:
            other: Entity that collided
        """
        # Destruction handled by combat system
        pass

    def destroy(self) -> None:
        """Destroy crate (called by combat system)."""
        self._destroyed = True
        self.deactivate()

    def is_destroyed(self) -> bool:
        """Check if crate is destroyed."""
        return self._destroyed

    def get_sprite(self) -> pygame.Surface:
        """Get crate sprite."""
        from ...infrastructure.rendering.sprite_placeholder import PlaceholderSprites
        return PlaceholderSprites.create_breakable_crate()
