"""
Obstacle base class for all obstacle entities.

Provides common behavior for obstacles that block the ninja's path.
"""
from abc import ABC, abstractmethod
import pygame
from ..interfaces.i_game_entity import IGameEntity
from ..interfaces.i_collidable import ICollidable
from ..interfaces.i_updatable import IUpdatable
from ..interfaces.i_renderable import IRenderable
from ..value_objects.position import Position
from ..value_objects.velocity import Velocity
from ..value_objects.bounds import Bounds


class Obstacle(IGameEntity, ICollidable, IUpdatable, IRenderable, ABC):
    """
    Abstract base class for all obstacles.

    Provides common implementation for obstacle behavior.
    Subclasses define specific dimensions and collision effects.
    """

    def __init__(self, x: float, y: float, width: float, height: float, scroll_speed: float) -> None:
        """
        Initialize obstacle.

        Args:
            x: Initial x position
            y: Initial y position
            width: Obstacle width
            height: Obstacle height
            scroll_speed: How fast obstacle scrolls left (world speed)
        """
        self._position = Position(x, y)
        self._width = width
        self._height = height
        self._scroll_speed = scroll_speed
        self._active = True

    # IGameEntity implementation

    def get_position(self) -> Position:
        """Get obstacle position."""
        return self._position

    def get_bounds(self) -> Bounds:
        """Get obstacle collision bounds."""
        return Bounds(self._position.x, self._position.y, self._width, self._height)

    def is_active(self) -> bool:
        """Check if obstacle is active."""
        return self._active

    def deactivate(self) -> None:
        """Deactivate obstacle (for object pooling)."""
        self._active = False

    # ICollidable implementation

    @abstractmethod
    def on_collision(self, other: IGameEntity) -> None:
        """
        Handle collision with entity.

        Subclasses define specific collision behavior (e.g., kill ninja, get destroyed).

        Args:
            other: Entity that collided with this obstacle
        """
        pass

    def can_collide_with(self, other: IGameEntity) -> bool:
        """
        Check if obstacle can collide.

        Args:
            other: Entity to check

        Returns:
            True if active, False otherwise
        """
        return self._active

    # IUpdatable implementation

    def update(self, delta_time: float) -> None:
        """
        Update obstacle position (scroll left).

        Args:
            delta_time: Time elapsed since last frame
        """
        # Scroll left with world speed
        dx = -self._scroll_speed * delta_time
        self._position = self._position.translate(dx, 0.0)

        # Deactivate if off-screen (left side)
        if self._position.x + self._width < -100:
            self.deactivate()

    # IRenderable implementation

    @abstractmethod
    def get_sprite(self) -> pygame.Surface:
        """
        Get sprite for rendering.

        Subclasses provide specific sprite.

        Returns:
            Pygame surface to render
        """
        pass

    def get_render_position(self) -> Position:
        """Get position for rendering."""
        return self._position

    def get_render_layer(self) -> int:
        """Get render layer (obstacles in middle layer)."""
        return 5
