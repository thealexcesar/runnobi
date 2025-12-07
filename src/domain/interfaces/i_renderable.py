"""
IRenderable interface for entities that can be drawn.

Entities that appear on screen implement this interface to provide
rendering information to the rendering system.
"""
from abc import ABC, abstractmethod
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..value_objects.position import Position


class IRenderable(ABC):
    """
    Interface for entities that can be rendered.

    Separates rendering concerns from game logic (ISP).
    Some entities may have logic but no visual representation.
    """

    @abstractmethod
    def get_sprite(self) -> pygame.Surface:
        """
        Get current sprite to render.

        Returns the appropriate sprite based on entity's current state
        (e.g., ninja running vs jumping).

        Returns:
            Pygame Surface containing the sprite image
        """
        pass

    @abstractmethod
    def get_render_position(self) -> 'Position':
        """
        Get position where sprite should be rendered.

        May differ from logical position (e.g., offset for visual effects).

        Returns:
            Position where sprite's top-left corner should be drawn
        """
        pass

    @abstractmethod
    def get_render_layer(self) -> int:
        """
        Get rendering layer for draw order.

        Lower numbers render first (background), higher numbers render
        later (foreground). Ensures correct visual stacking.

        Returns:
            Layer number (0 = furthest back, higher = closer to front)
        """
        pass
