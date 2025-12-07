"""
Collectible base class for all collectible items.

Provides common behavior for items that ninja can collect.
"""
from abc import ABC, abstractmethod
import pygame

from domain.interfaces import IGameEntity, ICollidable, IUpdatable, IRenderable
from domain.value_objects import Position, Bounds


class Collectible(IGameEntity, ICollidable, IUpdatable, IRenderable, ABC):
    """
    Abstract base class for all collectibles.

    Provides common implementation for collectible behavior.
    Subclasses define specific collection effects.
    """

    def __init__(self, x: float, y: float, width: float, height: float, scroll_speed: float) -> None:
        """
        Initialize collectible.

        Args:
            x: Initial x position
            y: Initial y position
            width: Collectible width
            height: Collectible height
            scroll_speed: World scroll speed
        """
        self._position = Position(x, y)
        self._width = width
        self._height = height
        self._scroll_speed = scroll_speed
        self._active = True
        self._collected = False

    # IGameEntity implementation

    def get_position(self) -> Position:
        """Get collectible position."""
        return self._position

    def get_bounds(self) -> Bounds:
        """Get collectible collision bounds."""
        return Bounds(self._position.x, self._position.y, self._width, self._height)

    def is_active(self) -> bool:
        """Check if collectible is active."""
        return self._active and not self._collected

    def deactivate(self) -> None:
        """Deactivate collectible."""
        self._active = False

    # ICollidable implementation

    @abstractmethod
    def on_collision(self, other: IGameEntity) -> None:
        """
        Handle collection by ninja.

        Subclasses define specific collection effects.

        Args:
            other: Entity that collected this (should be ninja)
        """
        pass

    def can_collide_with(self, other: IGameEntity) -> bool:
        """
        Check if collectible can be collected.

        Args:
            other: Entity to check

        Returns:
            True if active and not collected
        """
        return self.is_active()

    # IUpdatable implementation

    def update(self, delta_time: float) -> None:
        """
        Update collectible position (scroll left).

        Args:
            delta_time: Time elapsed since last frame
        """
        # Scroll left with world speed
        dx = -self._scroll_speed * delta_time
        self._position = self._position.translate(dx, 0.0)

        # Deactivate if off-screen
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
        """Get render layer (collectibles above obstacles)."""
        return 6

    # Collection helpers

    def collect(self) -> None:
        """Mark collectible as collected."""
        self._collected = True
        self.deactivate()

    def is_collected(self) -> bool:
        """Check if collectible was collected."""
        return self._collected
