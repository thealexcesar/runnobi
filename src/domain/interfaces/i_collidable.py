"""
ICollidable interface for entities with collision behavior.

Entities that can collide with other objects implement this interface
to handle collision detection and response.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .i_game_entity import IGameEntity


class ICollidable(ABC):
    """
    Interface for entities that participate in collision detection.

    Separates collision concerns from base entity behavior (ISP).
    Not all entities need collision - some are purely visual.
    """

    @abstractmethod
    def on_collision(self, other: 'IGameEntity') -> None:
        """
        Handle collision with another entity.

        Called by collision system when this entity collides with another.
        Implementations should define specific collision behavior.

        Args:
            other: The entity this object collided with
        """
        pass

    @abstractmethod
    def can_collide_with(self, other: 'IGameEntity') -> bool:
        """
        Check if this entity can collide with another entity.

        Used to filter collision checks (e.g., coins don't collide with obstacles).

        Args:
            other: The entity to check collision possibility with

        Returns:
            True if collision should be checked, False otherwise
        """
        pass
