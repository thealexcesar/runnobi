"""
IUpdatable interface for entities with time-based behavior.

Entities that need to update their state each frame implement this interface.
"""
from abc import ABC, abstractmethod


class IUpdatable(ABC):
    """
    Interface for entities that update each frame.

    Separates update logic from entity definition (ISP).
    Static entities don't need to implement this.
    """

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """
        Update entity state based on elapsed time.

        Called once per frame by the game loop. Delta time ensures
        frame-rate independent behavior.

        Args:
            delta_time: Time elapsed since last frame (seconds)
        """
        pass
