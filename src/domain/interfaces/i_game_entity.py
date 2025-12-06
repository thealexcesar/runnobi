"""
IGameEntity interface defining core entity contract.

All game entities (ninja, obstacles, collectibles) must implement this interface
to ensure consistent behavior across the game system.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..value_objects.position import Position
    from ..value_objects.bounds import Bounds


class IGameEntity(ABC):
    """
    Base interface for all game entities.

    Defines the minimal contract that all game objects must fulfill.
    Follows Interface Segregation Principle - entities only implement what they need.
    """

    @abstractmethod
    def get_position(self) -> 'Position':
        """
        Get entity's current position.

        Returns:
            Current Position value object
        """
        pass

    @abstractmethod
    def get_bounds(self) -> 'Bounds':
        """
        Get entity's collision bounds.

        Returns:
            Current Bounds value object for collision detection
        """
        pass

    @abstractmethod
    def is_active(self) -> bool:
        """
        Check if entity is active in the game.

        Inactive entities should be ignored by game systems.

        Returns:
            True if entity is active, False otherwise
        """
        pass

    @abstractmethod
    def deactivate(self) -> None:
        """
        Deactivate this entity.

        Used for object pooling and cleanup. Deactivated entities
        can be reused instead of creating new instances.
        """
        pass
