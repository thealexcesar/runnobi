"""
Velocity value object representing 2D movement speed.

Immutable value object for velocity components, ensuring physics
calculations remain consistent and traceable.
"""
from typing import Tuple


class Velocity:
    """
    Immutable 2D velocity value object.

    Represents velocity in 2D space with horizontal and vertical components.
    Immutability ensures physics state remains predictable.
    """
    def __init__(self, vx: float, vy: float) -> None:
        """
        Initialize velocity with x and y components.

        Args:
            vx: Horizontal velocity (pixels per second)
            vy: Vertical velocity (pixels per second, positive = downward)
        """
        self._vx = float(vx)
        self._vy = float(vy)

    @property
    def vx(self) -> float:
        """Get horizontal velocity component."""
        return self._vx

    @property
    def vy(self) -> float:
        """Get vertical velocity component."""
        return self._vy

    def as_tuple(self) -> Tuple[float, float]:
        """
        Convert velocity to tuple representation.

        Returns:
            Tuple of (vx, vy) components
        """
        return (self._vx, self._vy)

    def magnitude(self) -> float:
        """
        Calculate velocity magnitude (speed).

        Returns:
            Speed in pixels per second
        """
        return (self._vx ** 2 + self._vy ** 2) ** 0.5

    def scale(self, factor: float) -> 'Velocity':
        """
        Create new velocity scaled by a factor.

        Args:
            factor: Scaling factor

        Returns:
            New Velocity instance with scaled components
        """
        return Velocity(self._vx * factor, self._vy * factor)

    def add(self, other: 'Velocity') -> 'Velocity':
        """
        Create new velocity by adding another velocity.

        Args:
            other: Velocity to add

        Returns:
            New Velocity instance with summed components
        """
        return Velocity(self._vx + other.vx, self._vy + other.vy)

    def apply_gravity(self, gravity: float, delta_time: float) -> 'Velocity':
        """
        Create new velocity with gravity applied.

        Args:
            gravity: Gravity acceleration (pixels per second squared)
            delta_time: Time step in seconds

        Returns:
            New Velocity instance with gravity applied to vy
        """
        return Velocity(self._vx, self._vy + gravity * delta_time)

    def __eq__(self, other: object) -> bool:
        """Check equality with another velocity."""
        if not isinstance(other, Velocity):
            return False
        return self._vx == other.vx and self._vy == other.vy

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Velocity(vx={self._vx}, vy={self._vy})"

    def __hash__(self) -> int:
        """Make Velocity hashable for use in sets/dicts."""
        return hash((self._vx, self._vy))
